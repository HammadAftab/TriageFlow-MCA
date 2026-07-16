from ai.scripts.ticket_retriever import retrieve_similar_tickets
from ai.scripts.llm_helper import generate_resolution


subject = "Internet disconnects frequently"

body = """
My internet connection disconnects every 10-15 minutes.
I have restarted the router but the issue still exists.
"""

print("Searching similar tickets...\n")

results = retrieve_similar_tickets(subject, body, top_k=3)

print("=" * 80)
print("SIMILAR TICKETS")
print("=" * 80)

for i, r in enumerate(results, start=1):
    print(f"\nTicket {i}")
    print("-" * 50)
    print("Distance:", round(r["distance"], 4))

    print("\nOriginal Ticket:")
    print(r["ticket"])

    print("\nResolution:")
    print(r["resolution"])

ticket_text = f"""
Subject:
{subject}

Body:
{body}
"""

print("\n")
print("=" * 80)
print("GENERATING FINAL RESOLUTION...")
print("=" * 80)

# Passing the entire results list
final_resolution = generate_resolution(
    ticket_text,
    results
)

print("\nFINAL AI RESOLUTION\n")
print(final_resolution)