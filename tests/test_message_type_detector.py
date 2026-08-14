from agent.history.message_type_detector import MessageTypeDetector
from agent.models.message_type import MessageType


def test_text():
    message = {
        "content": "ăn chưa"
    }

    assert MessageTypeDetector.detect(message) == MessageType.TEXT


def test_link():
    message = {
        "content": "xem này https://example.com"
    }

    assert MessageTypeDetector.detect(message) == MessageType.LINK


def test_image():
    message = {
        "photos": [
            {"uri": "photo.jpg"}
        ]
    }

    assert MessageTypeDetector.detect(message) == MessageType.IMAGE


def test_voice():
    message = {
        "audio_files": [
            {"uri": "voice.mp4"}
        ]
    }

    assert MessageTypeDetector.detect(message) == MessageType.VOICE


def test_emoji_only():
    message = {
        "content": "😂😂😂"
    }

    assert MessageTypeDetector.detect(message) == MessageType.EMOJI_ONLY