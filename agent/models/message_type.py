from enum import Enum


class MessageType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    VOICE = "VOICE"
    LINK = "LINK"
    STICKER = "STICKER"
    GIF = "GIF"
    EMOJI_ONLY = "EMOJI_ONLY"
    VIEW_ONCE = "VIEW_ONCE"
    UNKNOWN_MEDIA = "UNKNOWN_MEDIA"