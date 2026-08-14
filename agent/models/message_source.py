from enum import Enum

class MessageSource(str, Enum):
    OWNER = "OWNER"
    TARGET = "TARGET"
    UNKNOWN = "UNKNOWN"
    