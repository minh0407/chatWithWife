from agent.history.message_burst_builder import (
    MessageBurstBuilder
)

from agent.models.message import Message
from agent.models.message_source import MessageSource
from agent.models.message_type import MessageType


def create_message(
    message_id: str,
    source: MessageSource,
    timestamp_ms: int,
    text: str
):

    return Message(
        message_id=message_id,
        sender_name=source.value,
        source=source,
        message_type=MessageType.TEXT,
        timestamp_ms=timestamp_ms,
        text=text
    )


def test_combine_three_messages():

    messages = [
        create_message(
            "1",
            MessageSource.TARGET,
            1000,
            "Em"
        ),
        create_message(
            "2",
            MessageSource.TARGET,
            2000,
            "Yêu"
        ),
        create_message(
            "3",
            MessageSource.TARGET,
            3000,
            "Anh"
        )
    ]

    builder = MessageBurstBuilder(
        buffer_seconds=4
    )

    bursts = builder.build(
        messages
    )

    assert len(bursts) == 1

    assert (
        bursts[0].combined_text
        == "Em Yêu Anh"
    )

    assert len(
        bursts[0].messages
    ) == 3


def test_different_sender_creates_new_burst():

    messages = [
        create_message(
            "1",
            MessageSource.TARGET,
            1000,
            "Em"
        ),
        create_message(
            "2",
            MessageSource.OWNER,
            2000,
            "Anh đây"
        )
    ]

    builder = MessageBurstBuilder(
        buffer_seconds=4
    )

    bursts = builder.build(
        messages
    )

    assert len(bursts) == 2


def test_message_outside_buffer_creates_new_burst():

    messages = [
        create_message(
            "1",
            MessageSource.TARGET,
            1000,
            "Em"
        ),
        create_message(
            "2",
            MessageSource.TARGET,
            7000,
            "Anh ơi"
        )
    ]

    builder = MessageBurstBuilder(
        buffer_seconds=4
    )

    bursts = builder.build(
        messages
    )

    assert len(bursts) == 2