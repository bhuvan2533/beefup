from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import json
import app.ai.setup as setup
from app.ai.prompts import EXTRACTION_PROMPT, JD_ENHANCEMENT_PROMPT
from app.ai.models import EnhancedProfile

llm = setup.LLM

parser = PydanticOutputParser(pydantic_object=EnhancedProfile)

async def extract_profile_and_format(profile_text: str) -> EnhancedProfile:
    prompt = PromptTemplate(
        template=EXTRACTION_PROMPT,
        input_variables=["profile"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    result = await chain.ainvoke({"profile": profile_text})
    return result


async def enhance_profile_with_jd(jd: str, structured_profile: EnhancedProfile) -> EnhancedProfile:
    prompt = PromptTemplate(
        template=JD_ENHANCEMENT_PROMPT,
        input_variables=["jd", "profile"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    result = await chain.ainvoke({
        "jd": jd,
        "profile": json.dumps(structured_profile)
    })
    return result