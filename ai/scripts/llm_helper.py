import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_resolution(ticket, similar_resolutions):

    prompt = f"""
You are an experienced IT support engineer.

Customer ticket:
{ticket}

Previous successful resolutions from similar support tickets:
{similar_resolutions}

You are an experienced IT support engineer.

Write a professional resolution that can be understood by a non-technical user.

Your task is to generate the best possible resolution for the current ticket.

Rules:
- Use the previous resolutions only as guidance.
- Do not copy them word for word.
- Combine the most relevant ideas if appropriate.
- Write for a non-technical customer.
- Use simple English.
- Maximum 6 bullet points.
- Start with the easiest troubleshooting steps.
- Avoid technical terms unless absolutely necessary.
- Be specific to the customer's issue.
- Keep the response concise.
- If additional information is needed, politely ask for it at the end.
"""

    response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=prompt
    )

    return response.text