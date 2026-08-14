import re 
from agent.models.message_type import MessageType


class MessageTypeDetector:
    URL_PATTERN = re.compile(
        r"(https?://\S+|www\.\S+)",
        re.IGNORECASE
)


    @staticmethod
    def is_emoji_only(text: str) -> bool:
        if not text:
            return False

        stripped = text.strip()
        if not stripped:
            return False    

        has_letters_or_numbers = any(char.isalnum() for char in stripped)
        if has_letters_or_numbers:
            return False
        return any(ord(char)>127 for char in stripped)

    @classmethod
    def detect(cls,raw_message: dict) -> MessageType:
        if raw_message.get("is_view_once"):
            return MessageType.VIEW_ONCE

        if raw_message.get("photos"):
            return MessageType.IMAGE

        if raw_message.get("videos"):
            return MessageType.VIDEO

        if raw_message.get("audio_files"):
            return MessageType.VOICE

        if raw_message.get("sticker"):
            return MessageType.STICKER

        if raw_message.get("gifs"):
            return MessageType.GIF

        text = raw_message.get("content")

        if isinstance(text, str):

            if cls.URL_PATTERN.search(text):
                return MessageType.LINK

            if cls.is_emoji_only(text):
                return MessageType.EMOJI_ONLY

            if text.strip():
                return MessageType.TEXT

        return MessageType.UNKNOWN_MEDIA