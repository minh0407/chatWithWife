from dataclasses import dataclass

from agent.models.message_burst import MessageBurst
from agent.models.message_source import MessageSource


@dataclass 
class ConversationTurn:
    bursts:list[MessageBurst]
    source:MessageSource
    start_timestamp_ms: int 
    end_timestamp_ms: int 
    combined_text: str
    