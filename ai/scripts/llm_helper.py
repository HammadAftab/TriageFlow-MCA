import os

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_resolution(subject, body, retrieved_tickets):

    context = ""

    for i, ticket in enumerate(retrieved_tickets, start=1):

        context += (
            f"\nSimilar Ticket {i}\n"
            f"Problem:\n{ticket['ticket']}\n\n"
            f"Resolution:\n{ticket['resolution']}\n\n"
        )

    prompt = f"""
You are an IT support assistant.

A customer has submitted the following ticket.

Subject:
{subject}

Description:
{body}

Below are similar resolved tickets.

{context}

Using only the information above, write:

1. Most likely issue.
2. Step-by-step resolution.
3. If uncertain, mention that the ticket should be escalated.

Keep the answer professional and under 200 words.
"""

    response = model.generate_content(prompt)

    return response.text