from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in the debate_engine directory
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path)

api_key = os.getenv("Groq_API_key")
if not api_key:
    # Fallback to GROQ_API_KEY if Groq_API_key is not set
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-120b"

def call_llm(messages, temperature=0.7, max_output_tokens=1000):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        max_tokens=max_output_tokens
    )

    return response.choices[0].message.content