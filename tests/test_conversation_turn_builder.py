from agent.history.ConversationTurnBuilder import (
    ConversationTurnBuilder
)

from agent.models.message_burst import MessageBurst
from agent.models.message_source import MessageSource


def create_burst(
    source: MessageSource,
    start: int,
    end: int,
    text: str
) -> MessageBurst:

    return MessageBurst(
        messages=[],
        source=source,
        start_timestamp_ms=start,
        end_timestamp_ms=end,
        combined_text=text
    )


def test_same_source_becomes_one_turn():

    bursts = [
        create_burst(
            MessageSource.TARGET,
            1000,
            2000,
            "Anh ơi"
        ),
        create_burst(
            MessageSource.TARGET,
            10000,
            11000,
            "Anh đang đâu"
        )
    ]

    builder = ConversationTurnBuilder()

    turns = builder.build(bursts)

    assert len(turns) == 1

    assert (
        turns[0].combined_text
        == "Anh ơi Anh đang đâu"
    )

    assert len(turns[0].bursts) == 2


def test_change_source_creates_new_turn():

    bursts = [
        create_burst(
            MessageSource.TARGET,
            1000,
            2000,
            "Anh ơi"
        ),
        create_burst(
            MessageSource.OWNER,
            3000,
            4000,
            "Anh đây"
        )
    ]

    builder = ConversationTurnBuilder()

    turns = builder.build(bursts)

    assert len(turns) == 2

    assert (
        turns[0].source
        == MessageSource.TARGET
    )

    assert (
        turns[1].source
        == MessageSource.OWNER
    )


def test_target_target_owner():

    bursts = [
        create_burst(
            MessageSource.TARGET,
            1000,
            2000,
            "Anh ơi"
        ),
        create_burst(
            MessageSource.TARGET,
            10000,
            11000,
            "Anh đang đâu"
        ),
        create_burst(
            MessageSource.OWNER,
            12000,
            13000,
            "Anh đang ở nhà"
        )
    ]

    builder = ConversationTurnBuilder()

    turns = builder.build(bursts)

    assert len(turns) == 2

    assert (
        turns[0].combined_text
        == "Anh ơi Anh đang đâu"
    )

    assert (
        turns[1].combined_text
        == "Anh đang ở nhà"
    )