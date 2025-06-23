from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
from app.utils.logger import get_logger

load_dotenv(override=True)
logger = get_logger()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")

if not OPEN_AI_API_KEY:
    logger.error("OpenAI API key is not set in environment variables.")
    raise ValueError("OpenAI API key is not set in environment variables.")

if not OPEN_AI_MODEL:
    logger.error("OpenAI model is not set in environment variables.")
    raise ValueError("OpenAI model is not set in environment variables.")

LLM = ChatOpenAI(
    model=OPEN_AI_MODEL,
    openai_api_key=OPEN_AI_API_KEY
)
