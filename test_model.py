import pytest
from model import extract_keywords, generate_framework_string, chat_with_gpt

def test_extract_keywords():
    sentence = "The quick brown fox jumps over the lazy dog"
    keywords = extract_keywords(sentence)
    assert keywords == "fox jumps dog"

def test_generate_framework_string():
    business_phase = "growth"
    framework_string = generate_framework_string(business_phase)
    assert isinstance(framework_string, str)
    assert len(framework_string) > 0

def test_chat_with_gpt(mocker):
    prompt = "What is the future of AI?"
    model = "gpt-3.5-turbo"
    country = "USA"
    business_phase = "growth"
    mock_response = {
        "choices": [
            {"message": {"content": "AI will continue to evolve."}}
        ]
    }
    mocker.patch("requests.post", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))
    response = chat_with_gpt(prompt, model, country, business_phase)
    assert "choices" in response
    assert response["choices"][0]["message"]["content"] == "AI will continue to evolve."