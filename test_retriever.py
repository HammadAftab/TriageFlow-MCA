from ai.scripts.ticket_retriever import retrieve_similar_tickets

results = retrieve_similar_tickets(
    "Internet not working",
    "My broadband connection disconnects every few minutes."
)

for i, result in enumerate(results, start=1):
    print("=" * 80)
    print(f"Result {i}")
    print("-" * 80)
    print("Similar Ticket:")
    print(result["ticket"])
    print()
    print("Resolution:")
    print(result["resolution"])
    print()
    print("Distance:", result["distance"])