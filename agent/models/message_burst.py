from dataclasses import dataclass
from typing import List

from agent.models.message import Message
from agent.models.message_source import MessageSource

@dataclass
class MessageBurst:
    messages: List[Message]
    source: MessageSource
    start_timestamp_ms: int
    end_timestamp_ms:int 
    combined_text: str