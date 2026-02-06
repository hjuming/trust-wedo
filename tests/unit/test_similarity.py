import pytest
from trust_wedo.core.similarity_calculator import calculate_similarity, get_text_differences

def test_calculate_similarity_identical():
    text = "Trust WEDO is a trust infrastructure."
    assert calculate_similarity(text, text) == 1.0

def test_calculate_similarity_different():
    text1 = "Trust WEDO is good."
    text2 = "Trust WEDO is bad."
    score = calculate_similarity(text1, text2)
    assert 0.5 < score < 1.0

def test_get_text_differences_identical():
    text = "Same content."
    assert get_text_differences(text, text) == []

def test_get_text_differences_minor():
    text1 = "Trust WEDO is a trust infrastructure system."
    text2 = "Trust WEDO is the trust infrastructure system."
    diffs = get_text_differences(text1, text2)
    assert "微小用詞差異" in diffs

def test_get_text_differences_significant():
    text1 = "Trust WEDO is a trust system."
    text2 = "Something completely different."
    diffs = get_text_differences(text1, text2)
    assert "內容存在顯著差異" in diffs
