import pytest
from GTI.genai.genai import GenAI

def test_genai():
    genai = GenAI()
    response = genai.generate_text("Hello, world!")
    assert response is not None
