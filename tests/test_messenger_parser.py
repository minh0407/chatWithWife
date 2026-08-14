from agent.history.messenger_parser import MessengerParser
from agent.models.message_source import MessageSource
from agent.models.message_type import MessageType


def test_parse_messenger_json():

    parser = MessengerParser(
        owner_name="Minh",
     
    )

    messages = parser.parse(
        "tests/fixtures/sample_conversation.json"
    )

    assert len(messages) == 3
    assert parser.target_name == "Girlfriend"

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

def test_filter_last_365_days():

    parser = MessengerParser(
        owner_name="Minh",
        days_to_import=365
    )

    messages = parser.parse(
        "tests/fixtures/sample_conversation_365.json"
    )

    assert len(messages) == 2

    assert messages[0].text == "tin cách đây 300 ngày"
    assert messages[1].text == "tin mới nhất"