import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.1-flash-lite"


def generate_resolution(ticket, similar_tickets):

    similar_text = ""

    for i, t in enumerate(similar_tickets, start=1):
        similar_text += f"""
Reference Ticket {i}
--------------------
Original Issue:
{t["ticket"]}

Resolution:
{t["resolution"]}

"""

    prompt = f"""
You are an experienced IT support engineer.

A customer has raised the following ticket.

Customer Ticket
----------------
{ticket}

Below are the 3 most similar previously resolved tickets.

{similar_text}

Your task is to write ONE improved professional resolution.

Use the previous tickets only as reference.
Do NOT copy any one resolution exactly.
Analyze all reference tickets before answering. 
If multiple reference tickets contain useful troubleshooting steps, combine them into one coherent resolution. 
Do not ignore a relevant reference unless it is clearly unrelated or redundant.
Only include steps that are relevant to the customer's issue.

Rules:
- Maximum 6 bullet points.
- Use simple English.
- Avoid technical jargon like "network adapter", "firmware", "DNS", "driver" unless absolutely necessary.
- Start with the easiest troubleshooting steps.
- Keep the response short unless additional detail is absolutely necessary.
- Be as relevant to the ticket as possible.
- If additional information is required to diagnose the issue, end with exactly one sentence asking the user to raise a new ticket and include the specific information needed.
- Do not ask the user to reply because tickets are closed after the resolution is provided.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text