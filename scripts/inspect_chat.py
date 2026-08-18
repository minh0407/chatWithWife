import json 
from pathlib import Path

file_path = Path("data/raw/chat.json")

if not file_path.exists():
    print(f"File {file_path} does not exist.")
    exit()

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print ("===== chat json info =====")

print("top _level type:")
print(type(data).__name__)
if isinstance(data,dict):

    print("\nTop-level keys:")
    print(list(data.keys()))

    participants = data.get("participants", [])
    print("\n Participants count:")
    print(len(participants))

    messages = data.get("messages",[])

    print("\n messages count: ")
    print(len(messages))

    if messages:
        first_messages= messages[0]
        last_messages= messages[-1]

        print("\n message keys")
        print(list(first_messages.keys()))
        print("\nFirst timestamp:")
        print(first_messages.get("timestamp_ms"))

        print("\nLast timestamp:")
        print(last_messages.get("timestamp_ms"))