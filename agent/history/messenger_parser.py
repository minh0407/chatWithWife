import json 
from pathlib import Path

from agent.history.message_type_detector import MessageTypeDetector
from agent.models.message import Message
from agent.models.message_source import MessageSource


class MessengerParser:
    def __init__(self,owner_name: str, target_name:str):
        self.owner_name = owner_name
        self.target_name= target_name

    def _detect_source(self, sender_name:str) -> MessageSource:
        if sender_name == self.owner_name:
            return MessageSource.OWNER
        elif sender_name == self.target_name:
            return MessageSource.TARGET
        else:
            return MessageSource.UNKNOWN

    def parse(self, file_path: str) -> list[Message]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(path,"r", encoding="utf-8") as file:
            raw_data = json.load(file)
        raw_messages = raw_data.get("messages", [])
        messages = []

        for index, raw_message in enumerate(raw_messages):
            sender_name = raw_message.get("sender_name")
            timestamp_ms = raw_message.get("timestamp_ms",0)
            source = self._detect_source(sender_name)
            message_type = MessageTypeDetector.detect(raw_message)
            text = raw_message.get("content", None)

            if not sender_name or not timestamp_ms:
                continue

            source = self._detect_source(sender_name)
            message_type = MessageTypeDetector.detect(raw_message)

            message = Message(
                message_id=f"msg_{timestamp_ms}_{index}",
                sender_name=sender_name,
                source=source,
                message_type=message_type,
                timestamp_ms=timestamp_ms,
                text=text
            )
            messages.append(message)
        messages.sort(key=lambda msg: msg.timestamp_ms)
        return messages    