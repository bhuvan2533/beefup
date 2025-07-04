from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import json
import app.ai.setup as setup
from app.ai.prompts import EXTRACTION_PROMPT, JD_ENHANCEMENT_PROMPT
from app.ai.models import EnhancedProfile
from app.utils.helpers import preprocess_llm_output, extract_text_from_llm_output, count_tokens
from app.utils.logger import get_logger

llm = setup.LLM
logger = get_logger()

parser = PydanticOutputParser(pydantic_object=EnhancedProfile)

async def extract_profile_and_format(profile_text: str) -> EnhancedProfile:
    prompt = PromptTemplate(
        template=EXTRACTION_PROMPT,
        input_variables=["profile"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm

    prompt_text = prompt.format(profile=profile_text)
    input_tokens = count_tokens(prompt_text)

    raw_output = await chain.ainvoke({"profile": profile_text})

    raw_output_text = extract_text_from_llm_output(raw_output)
    output_tokens = count_tokens(raw_output_text)
    cleaned_output = preprocess_llm_output(raw_output_text)
    result = parser.parse(cleaned_output)

    logger.info(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
    return result


async def enhance_profile_with_jd(jd: str, structured_profile: EnhancedProfile) -> EnhancedProfile:
    prompt = PromptTemplate(
        template=JD_ENHANCEMENT_PROMPT,
        input_variables=["jd", "profile"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm

    prompt_text = prompt.format(jd=jd, profile=json.dumps(structured_profile))
    input_tokens = count_tokens(prompt_text)

    raw_output = await chain.ainvoke({
        "jd": jd,
        "profile": json.dumps(structured_profile)
    })

    raw_output_text = extract_text_from_llm_output(raw_output)
    output_tokens = count_tokens(raw_output_text)
    cleaned_output = preprocess_llm_output(raw_output_text)
    result = parser.parse(cleaned_output)

    logger.info(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
    return result