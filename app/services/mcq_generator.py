from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import json
from app.config import OPENAI_API_KEY, LLM_MODEL
from app.core.pricing import calculate_cost
from app.schemas import MCQ_JSON_SCHEMA, MCQList

client = OpenAI(api_key=OPENAI_API_KEY)

    
parser = PydanticOutputParser(pydantic_object=MCQList)

# 3. Setup the Model
llm = ChatOpenAI(
    model=LLM_MODEL, 
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
    model_kwargs={"response_format": {"type": "json_object"}} # ✅ FORCES JSON MODE
)

# --- 3. Define Chain 1: Generator ---
# This chain focuses purely on creating questions from context
generate_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert teacher. Generate {num_questions} MCQs in {language} with {difficulty} difficulty."),
    ("user", "Context:\n{context}\n\n{format_instructions}")
])

# This creates a runnable chain: Prompt -> Model
generation_chain = generate_prompt | llm

# --- 4. Define Chain 2: Refiner/Validator ---
# This chain takes the questions and improves them
refine_prompt = ChatPromptTemplate.from_messages([
        ("system",  """ You are a senior exam reviewer. 
                        Your job is to review the provided MCQs and ensure:
                        1. Remove tautologies: If the answer is stated in the question, rewrite the question.
                        2. The explanations are clear and concise.
                        3. The questions are unambiguous.
                        4. Improve Distractors: Make wrong options look plausible, not obviously wrong.
                        5. The output is valid JSON matching the schema.

                        Return the improved MCQs in the same JSON format.
                    """),
            ("user", "Here are the draft MCQs:\n{mcq_draft}\n\n{format_instructions}")
    ])

refinement_chain = refine_prompt | llm


def generate_mcqs(context: str, num_questions: int = 10, difficulty: str = "medium", language: str = "Bengali"):
    
    # STEP A: Generate Draft
    # We pass the context to the first chain
    draft_response = generation_chain.invoke({
        "context": context,
        "num_questions": num_questions,
        "difficulty": difficulty,
        "language": language,
        "format_instructions": parser.get_format_instructions()
    })

     # STEP B: Refine Draft
    # We pass the OUTPUT of Chain A into Chain B
    final_response = refinement_chain.invoke({
        "mcq_draft": draft_response.content, # Output from previous step becomes input here
        "format_instructions": parser.get_format_instructions()
    })
    
    # Calculate Costs (Sum of both chains)
    total_prompt_tokens = draft_response.response_metadata["token_usage"]["prompt_tokens"] + \
                          final_response.response_metadata["token_usage"]["prompt_tokens"]
    
    total_completion_tokens = draft_response.response_metadata["token_usage"]["completion_tokens"] + \
                              final_response.response_metadata["token_usage"]["completion_tokens"]

    cost = calculate_cost(LLM_MODEL, total_prompt_tokens, total_completion_tokens)
    
    try:
        parsed_content = parser.parse(final_response.content)
        # Success: It's a Pydantic model, so we convert to dict
        final_content = parsed_content.model_dump()
    except Exception as e:
        # Failure: It's a fallback dictionary already
        # We capture the error and the raw text for debugging
        print(f"PARSING ERROR: {e}")
        final_content = {
            "error": "Failed to parse MCQ response",
            "raw_text": final_response.content
        }

    return {
        "usage": {
            "input_tokens": total_prompt_tokens,
            "output_tokens": total_completion_tokens,
            "total_tokens": total_prompt_tokens + total_completion_tokens
        },
        "cost": cost,
        "content": final_content # Return the processed dictionary directly
    }