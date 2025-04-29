import os
import json
import openai
from app.utils.logger import get_logger
from app.exception_handlers import InternalServerError
from openai.types.chat.completion_create_params import ResponseFormat

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Get logger
logger = get_logger()

def generate_ai_completion(messages, model="gpt-3.5-turbo", temperature=0.5, max_tokens=4000):
    try:
        logger.info(f"Sending request to OpenAI API using {model}")
        # Updated API call (openai.Chat.completions.create)
        # response = openai.chat.completions.create(
        #     model=model,
        #     messages=messages,
        #     temperature=temperature,
        #     max_tokens=max_tokens,
        # )

        response = openai.types.chat.chat_completion.ChatCompletion(
            id='chatcmpl-123456789abcdef',
            choices=[
                openai.types.chat.chat_completion.Choice(
                    finish_reason='stop',
                    index=0,
                    logprobs=None,
                    content='ENHANCED RESUME:\n\nName: Jane Smith\n\nSoftware Engineer\n\nSummary:\nDedicated software engineer with 6+ years of experience in building web applications using JavaScript, TypeScript, and Node.js. Skilled in creating RESTful APIs and scalable backend systems.\n\nSkills:\n- JavaScript, TypeScript\n- Node.js, Express.js\n- MongoDB, PostgreSQL\n- GraphQL, REST APIs\n- Git, Docker, Jenkins\n\nWork Experience:\n\nBackend Engineer - FinTech Inc (2021-Present)\n- Built and maintained financial transaction APIs with Node.js\n- Implemented caching using Redis to reduce response times\n- Led CI/CD pipeline setup and improved deployment efficiency\n\nFull Stack Developer - DevWorks (2017-2021)\n- Developed internal tools using MERN stack\n- Built user authentication and authorization systems\n- Worked closely with UX designers to improve usability',
                    message=openai.types.chat.chat_completion.ChatCompletionMessage(
                        role='assistant',
                        function_call=None,
                        tool_calls=None
                    )
                )
            ],
            created=1682375123,
            model='gpt-3.5-turbo',
            object='chat.completion',
            system_fingerprint='fp_44455566',
            usage=openai.types.completion_usage.CompletionUsage(
                completion_tokens=350,
                prompt_tokens=520,
                total_tokens=870
            )
        )
        # content='ENHANCED RESUME:\n\nName: John Doe\n\nSoftware Engineer\n\nSummary:\nExperienced software developer with 5+ years specializing in Python, Django, and React. Proven track record of building scalable web applications and implementing efficient backend solutions.\n\nSkills:\n- Python, Django, Django REST Framework\n- JavaScript, React, Next.js\n- SQL (PostgreSQL, MySQL)\n- Docker, AWS, CI/CD\n- Git, Agile methodologies\n\nWork Experience:\n\nSenior Developer - ABC Tech (2022-Present)\n- Led development of microservices architecture using Django and FastAPI\n- Implemented authentication system with JWT and OAuth 2.0\n- Reduced database query times by 40% through optimization\n\nFull Stack Developer - XYZ Solutions (2019-2022)\n- Developed and maintained e-commerce platform using Django and React\n- Integrated payment gateways and third-party APIs\n- Implemented responsive design principles and accessibility features',

        logger.info(f"Response type: {type(response)}")
        
        if hasattr(response, 'choices'):
            generated_text = response.choices[0].message.content
        elif isinstance(response, dict) and 'choices' in response:
            generated_text = response['choices'][0]['message']['content']
        else:
            logger.info(f"Unexpected response format: {response}")
            generated_text = str(response)
            
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
