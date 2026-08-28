from collections import Counter 

from agent.config.config_loader import ConfigLoader
from agent.history.messenger_parser import MessengerParser
from agent.history.message_burst_builder import MessageBurstBuilder
from agent.models.message_source import MessageSource

def main():
    print("===== Check Real MESSAGE BURTS")

    config_loader = ConfigLoader("config/agent.toml")

    config = config_loader.load()

    owner_name = config["agent"]["owner_name"]

    days_to_import = config["history"]["days_to_import"]

    buffer_seconds = config["conversation"]["message_buffer_seconds"]

    parser = MessengerParser(
        owner_name= owner_name,
        days_to_import= days_to_import
    )

    messages = parser.parse("data/raw/Linh Đan_90.json")

    builder = MessageBurstBuilder(buffer_seconds=buffer_seconds)
    bursts = builder.build(messages)


  # 4. Thống kê
    owner_bursts = sum(
        1
        for burst in bursts
        if burst.source == MessageSource.OWNER
    )

    target_bursts = sum(
        1
        for burst in bursts
        if burst.source == MessageSource.TARGET
    )

    burst_size_counter = Counter(
        len(burst.messages)
        for burst in bursts
    )

    print()
    print("OWNER:", owner_name)
    print("TARGET:", parser.target_name)

    print()
    print("Raw messages:", len(messages))
    print("Total bursts:", len(bursts))

    print()
    print("OWNER bursts:", owner_bursts)
    print("TARGET bursts:", target_bursts)

    print()
    print("===== BURST SIZE =====")

    for size, count in sorted(
        burst_size_counter.items()
    ):
        print(
            f"{size} message(s): {count} bursts"
        )


if __name__ == "__main__":
    main()   