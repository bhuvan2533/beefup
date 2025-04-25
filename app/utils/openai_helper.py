import os
import json
import openai
from app.utils.logger import get_logger
from app.exception_handlers import InternalServerError

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Get logger
logger = get_logger()

def generate_ai_completion(messages, model="gpt-4-turbo-preview", temperature=0.5, max_tokens=4000):
    try:
        logger.info(f"Sending request to OpenAI API using {model}")
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        generated_text = response.choices[0].message.content
        logger.info("Successfully received response from OpenAI")
        
        return generated_text
        
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise InternalServerError(f"Failed to generate AI completion: {str(e)}")

def format_text(text):
    #Format text with escape characters for frontend display.
    return json.dumps(text)[1:-1]

def enhance_profile_with_ai(profile_content, jd_content):
    try:
        # Default system prompt for profile enhancement
        system_prompt = """
        You are an expert resume enhancer. Your task is to improve the provided resume 
        to better align with the job description. Make the following improvements:
        
        1. Highlight relevant skills and experiences that match the job description
        2. Reword achievements to better reflect the requirements
        3. Reformat and organize content for better readability
        4. Add industry-specific keywords from the job description
        5. Maintain the original core facts and experiences
        
        Return the enhanced resume as a well-formatted string with appropriate escape characters 
        for proper display in documents. Maintain proper formatting with newlines (\\n) and 
        other formatting characters as needed and try to keep the enhanced profile in the same size
        that of the profile
        """
        
        # Prepare messages for OpenAI API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"JOB DESCRIPTION:\n{jd_content}\n\nORIGINAL RESUME:\n{profile_content}"}
        ]
        
        enhanced_content = generate_ai_completion(messages)
        
        enhanced_content_escaped = format_text(enhanced_content)
        
        return enhanced_content_escaped
        
    except Exception as e:
        logger.error(f"Error enhancing profile with OpenAI: {str(e)}")
        raise InternalServerError(f"Failed to enhance profile: {str(e)}")

def enhance_profile_with_custom_prompt(profile_content, jd_content, custom_prompt):
    try:
        # Base system prompt with custom instructions
        system_prompt = """
        You are an expert resume enhancer. Your task is to improve the provided resume 
        to better align with the job description, following the specific instructions below.
        
        Return the enhanced resume as a well-formatted string with appropriate escape characters 
        for proper display in documents. Maintain proper formatting with newlines (\\n) and 
        other formatting characters as needed.
        
        CUSTOM INSTRUCTIONS:
        """
        
        # Combine system prompt with custom prompt
        full_system_prompt = f"{system_prompt}\n{custom_prompt}"
        
        # Prepare messages for OpenAI API
        messages = [
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": f"JOB DESCRIPTION:\n{jd_content}\n\nORIGINAL RESUME:\n{profile_content}"}
        ]
        
        enhanced_content = generate_ai_completion(messages)
        
        enhanced_content_escaped = format_text(enhanced_content)
        
        return enhanced_content_escaped
        
    except Exception as e:
        logger.error(f"Error enhancing profile with custom prompt: {str(e)}")
        raise InternalServerError(f"Failed to enhance profile with custom prompt: {str(e)}")