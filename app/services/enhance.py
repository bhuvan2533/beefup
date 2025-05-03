from app.ai.service import extract_profile_and_format
from app.ai.service import enhance_profile_with_jd
from app.utils.logger import get_logger

logger = get_logger()

async def extractFromProfile(profile_content):
    logger.info("Extracting profile content to structured format")
    
    extracted_content = await extract_profile_and_format(profile_text=profile_content)
    
    logger.info("Profile extraction completed")
    return extracted_content.model_dump()


async def enhanceProfileWithJd(jd_content, structured_profile):
    logger.info("Enhancing profile content with job description")
    
    enhanced_content = await enhance_profile_with_jd(jd=jd_content, structured_profile=structured_profile)
    
    logger.info("Profile enhancement completed")
    return enhanced_content.model_dump()