import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.1-flash-lite"

print("Using model:", MODEL)

response = client.models.generate_content(
    model=MODEL,
    contents="Say Hello"
)

print(response.text)