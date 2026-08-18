from agent.models.message import Message
from agent.models.message_burst import MessageBurst
from agent.models.message_type import MessageType


class MessageBurstBuilder:

    def __init__(
        self,
        buffer_seconds: int = 4
    ):
        self.buffer_ms = buffer_seconds * 1000

    def _combine_text(
        self,
        messages: list[Message]
    ) -> str:

        text_parts = []

        for message in messages:

            if (
                message.message_type
                in [
                    MessageType.TEXT,
                    MessageType.LINK,
                    MessageType.EMOJI_ONLY
                ]
                and message.text
            ):
                text_parts.append(
                    message.text.strip()
                )

        return " ".join(text_parts)

    def _create_burst(
        self,
        messages: list[Message]
    ) -> MessageBurst:

        return MessageBurst(
            messages=messages,
            source=messages[0].source,
            start_timestamp_ms=messages[0].timestamp_ms,
            end_timestamp_ms=messages[-1].timestamp_ms,
            combined_text=self._combine_text(
                messages
            )
        )

    def build(
        self,
        messages: list[Message]
    ) -> list[MessageBurst]:

        if not messages:
            return []

        bursts = []

        current_messages = [
            messages[0]
        ]

        for message in messages[1:]:

            previous_message = current_messages[-1]

            time_difference = (
                message.timestamp_ms
                - previous_message.timestamp_ms
            )

            same_sender = (
                message.source
                == previous_message.source
            )

            within_buffer = (
                time_difference
                <= self.buffer_ms
            )

            # Cùng người gửi và cách nhau <= 4 giây
            # thì thêm vào burst hiện tại
            if same_sender and within_buffer:

                current_messages.append(
                    message
                )

            else:

                # Kết thúc burst cũ
                burst = self._create_burst(
                    current_messages
                )

                bursts.append(
                    burst
                )

                # Bắt đầu burst mới bằng message hiện tại
                current_messages = [
                    message
                ]

        # QUAN TRỌNG:
        # Sau khi vòng for kết thúc,
        # phải lưu burst cuối cùng.
        final_burst = self._create_burst(
            current_messages
        )

        bursts.append(
            final_burst
        )

        return bursts