from dataclasses import dataclass
from typing import Optional

from agent.models.message_source import MessageSource
from agent.models.message_type import MessageType

@dataclass
class Message:
    message_id: str
    sender_name: str
    source: MessageSource
    message_type: MessageType
    timestamp_ms: int
    text: Optional[str] = None