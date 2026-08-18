import json 
from pathlib import Path

from agent.history.message_type_detector import MessageTypeDetector
from agent.models.message import Message
from agent.models.message_source import MessageSource


class MessengerParser:
    def __init__(self,owner_name: str, days_to_import: int = 365):
        self.owner_name = owner_name
        self.target_name= None
        self.days_to_import = days_to_import

    def get_participants(self , raw_data: dict) -> list[str]:
        participants = raw_data.get("participants", [])
        names = []

        for participant in participants:
           if isinstance(participant,str):
            name = participant.strip()

            if name: names.append(name)

           elif isinstance(participant,dict):
               name = participant.get("name") 
               if name: names.append(name)   

        return names

    def _detect_target_name(self, participants: list[str]) -> str:
        other_people = [name for name in participants if name != self.owner_name]
        if len(other_people) !=1:
            raise ValueError("Expected exactly one other participant in the conversation.")

        return other_people[0]

    def _detect_source(self, sender_name:str) -> MessageSource:
        if sender_name == self.owner_name:
            return MessageSource.OWNER
        elif sender_name == self.target_name:
            return MessageSource.TARGET
        else:
            return MessageSource.UNKNOWN


    def _filter_recent_messages(self , messages: list[Message]) -> list[Message]:
        if not messages: 
            return []

        latest_timestamp = max(msg.timestamp_ms for msg in messages)
        cutoff_timestamp = latest_timestamp - (self.days_to_import * 24 * 60 * 60 * 1000)

        recent_messages = [msg for msg in messages if msg.timestamp_ms >= cutoff_timestamp]
        return recent_messages
    
        

    def parse(self, file_path: str) -> list[Message]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(path,"r", encoding="utf-8") as file:
            raw_data = json.load(file)


        participants = self.get_participants(raw_data)
        self.target_name = self._detect_target_name(participants)     


        raw_messages = raw_data.get("messages", [])
        messages = []

        for index, raw_message in enumerate(raw_messages):
            sender_name = (raw_message.get("sender_name") or raw_message.get("senderName"))
            timestamp_ms = raw_message.get("timestamp_ms")
            if timestamp_ms is None:
                 timestamp_ms = raw_message.get("timestamp")
           
            normalized_message = raw_message.copy()

            text = raw_message.get("content")
            if text is None:
                text = raw_message.get("text")
            if text is not None:
                normalized_message["content"] = text
            message_type = MessageTypeDetector.detect(normalized_message)
            
        

            if not sender_name or not timestamp_ms:
                continue

            source = self._detect_source(sender_name)
            
            
            
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
        messages=self._filter_recent_messages(messages)
        return messages    