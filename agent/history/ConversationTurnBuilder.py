from agent.models.message_burst import MessageBurst
from agent.models.conversation_turn import ConversationTurn


class ConversationTurnBuilder:

    def _combine_text(
        self,
        bursts: list[MessageBurst]
    ) -> str:

        text_parts = []

        for burst in bursts:

            if burst.combined_text:
                text_parts.append(
                    burst.combined_text.strip()
                )

        return " ".join(text_parts)

    def _create_turn(
        self,
        bursts: list[MessageBurst]
    ) -> ConversationTurn:

        return ConversationTurn(
            bursts=bursts,
            source=bursts[0].source,
            start_timestamp_ms=bursts[0].start_timestamp_ms,
            end_timestamp_ms=bursts[-1].end_timestamp_ms,
            combined_text=self._combine_text(
                bursts
            )
        )

    def build(
        self,
        bursts: list[MessageBurst]
    ) -> list[ConversationTurn]:

        if not bursts:
            return []

        turns = []

        current_bursts = [
            bursts[0]
        ]

        for burst in bursts[1:]:

            previous_burst = current_bursts[-1]

            same_source = (
                burst.source
                == previous_burst.source
            )

            if same_source:

                current_bursts.append(
                    burst
                )

            else:

                turn = self._create_turn(
                    current_bursts
                )

                turns.append(
                    turn
                )

                current_bursts = [
                    burst
                ]

        # Sau khi vòng for kết thúc
        # phải lưu turn cuối cùng
        final_turn = self._create_turn(
            current_bursts
        )

        turns.append(
            final_turn
        )

        return turns