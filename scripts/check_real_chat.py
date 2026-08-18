from collections import Counter
from agent.history.messenger_parser import MessengerParser
from agent.models.message_source import MessageSource
from agent.config.config_loader import ConfigLoader
def main():
    print("==== check real mess history")

    config_loader = ConfigLoader("config/agent.toml")
    config = config_loader.load()

    owner_name = config["agent"]["owner_name"]

    days_to_import = config["history"]["days_to_import"]
    print("OWNER", owner_name)

    parser = MessengerParser(owner_name=owner_name, days_to_import=days_to_import)

    messages = parser.parse("data/raw/Linh Đan_90.json")

    print()
    print("TARGET:" , parser.target_name)
    print("MESSAGES trong 365 ngay ", len(messages))

    owner_count = sum( 1 for message in messages if message.source == MessageSource.OWNER)

    target_count= sum(1 for message in messages if message.source == MessageSource.TARGET)

    print (" OWNEER messages:" , owner_count)
    print("TARGET messages:", target_count)

    message_types = Counter(
        message.message_type.value
        for message in messages
    )

    print()
    print("Message types:")
    for message_type, count in message_types.items():
        print(f"{message_type}: {count}")

if __name__ == "__main__":
    main()