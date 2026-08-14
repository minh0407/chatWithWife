from agent.config.config_loader import ConfigLoader


def main():
    print("=" * 50)
    print("chat with wife ")
    print("=" * 50)
    print(" agent starting ...")

    policy_loader= ConfigLoader("config/policies.toml")
    policies = policy_loader.load_()

    agent_loader =ConfigLoader("config/agentt.example.toml")
    agent_config = agent_loader.load_()

    print(f"Agent name: {agent_config['agent']['name']}")
    print(f"Mode: {agent_config['agent']['default_mode']}")

    print(
        f"Manual timeout: "
        f"{agent_config['conversation']['manual_timeout_minutes']} minutes"
    )

    print(
        f"Strong similarity: "
        f"{agent_config['similarity']['strong_threshold']}"
    )

    print(
        f"LM Studio URL: "
        f"{agent_config['llm']['base_url']}"
    )

    print(
        f"Image policy: "
        f"{policies['message_types']['IMAGE']['action']}"
    )

    print(
        f"Money policy: "
        f"{policies['intents']['MONEY']['action']}"
    )


if __name__ == "__main__":
    main()