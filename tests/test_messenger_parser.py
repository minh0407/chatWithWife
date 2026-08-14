from agent.history.messenger_parser import MessengerParser
from agent.models.message_source import MessageSource
from agent.models.message_type import MessageType


def test_parse_messenger_json():

    parser = MessengerParser(
        owner_name="Minh",
        target_name="Girlfriend"
    )

    messages = parser.parse(
        "tests/fixtures/sample_conversation.json"
    )

    assert len(messages) == 3

    # Message đầu tiên
    assert messages[0].timestamp_ms == 1000
    assert messages[0].source == MessageSource.TARGET
    assert messages[0].message_type == MessageType.TEXT
    assert messages[0].text == "ăn chưa"

    # Message thứ hai
    assert messages[1].timestamp_ms == 2000
    assert messages[1].source == MessageSource.OWNER
    assert messages[1].message_type == MessageType.TEXT
    assert messages[1].text == "chưa :))"

    # Message thứ ba
    assert messages[2].timestamp_ms == 3000
    assert messages[2].source == MessageSource.TARGET
    assert messages[2].message_type == MessageType.IMAGE