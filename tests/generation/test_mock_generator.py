import pytest

from app.generation.mock_generator import MockGenerator


@pytest.mark.asyncio
async def test_mock_generator_returns_expected_text():
    generator = MockGenerator(delay_seconds=0)  # No delay for testing
    prompt = "Context\nI am writin\nQuestion\nWhat is python?\nAnswer: Python is\n"

    result = await generator.generate(prompt)
    assert "Mock answer" in result
    assert result.endswith("Python is")


@pytest.mark.asyncio
async def test_mock_generator_handles_empty_prompt():
    generator = MockGenerator(delay_seconds=0)
    prompt = ""

    result = await generator.generate(prompt)
    assert "[empty]" in result
