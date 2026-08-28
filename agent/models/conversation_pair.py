from dataclasses import dataclass
from agent.models.message_burst import MessageBurst

@dataclass
class ConversationPair:
    target_burst:   MessageBurst
    owner_burst:    MessageBurst