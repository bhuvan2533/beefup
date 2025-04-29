from app.utils.openai_helper import enhance_profile_with_ai, enhance_profile_with_custom_prompt
from app.utils.logger import get_logger

logger = get_logger()

def enhance_profile(profile_content, jd_content):

    logger.info("Enhancing profile with job description")
    
    # Use OpenAI helper to enhance the profile
    enhanced_content = enhance_profile_with_ai(profile_content, jd_content)
    
    logger.info("Profile enhancement completed: " + enhanced_content)
    return enhanced_content

def enhance_profile_with_prompt(profile_content, jd_content, prompt):

    logger.info("Enhancing profile with job description using custom prompt")
    
    # Use OpenAI helper with custom prompt to enhance the profile
    enhanced_content = enhance_profile_with_custom_prompt(profile_content, jd_content, prompt)
    
    logger.info("Profile enhancement with custom prompt completed")
    return enhanced_content
