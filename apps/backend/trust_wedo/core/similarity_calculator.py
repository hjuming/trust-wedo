"""Similarity calculator module for Trust WEDO."""

from difflib import SequenceMatcher


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two strings (0-1)."""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1, text2).ratio()


def get_text_differences(text1: str, text2: str) -> list[str]:
    """Identify key differences between two strings (MVP version)."""
    # In a real version, this might use NLP to identify semantic differences.
    # For MVP, we'll return a simple message if they are different.
    if text1 == text2:
        return []
    
    similarity = calculate_similarity(text1, text2)
    if similarity > 0.95:
        return ["微小用詞差異"]
    elif similarity > 0.8:
        return ["部分描述差異"]
    else:
        return ["內容存在顯著差異"]
