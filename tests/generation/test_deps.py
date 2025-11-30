from app.core.constants import GeneratorBackend
from app.generation.adapters.ollama_adapter import OllamaGenerator
from app.generation.deps import get_generator
from app.generation.mock_generator import MockGenerator


import pytest


@pytest.mark.asyncio
async def test_get_generator_returns_mock_when_use_real_false_but_backend_not_provided():
    """
    When use_real is False and no backend is provided, should return MockGenerator.
    """
    gen = await anext(get_generator(use_real=False))
    assert isinstance(gen, MockGenerator)


@pytest.mark.asyncio
async def test_get_generator_returns_mock_when_use_real_true_and_backend_mock():
    """
    When use_real is True and backend is Mock, should return MockGenerator.
    """
    gen = await anext(get_generator(use_real=True, backend=GeneratorBackend.Mock))
    assert isinstance(gen, MockGenerator)


@pytest.mark.asyncio
async def test_get_generator_returns_ollama_when_use_real_false_and_backend_ollama():
    """
    When use_real is True and backend is Ollama, should return OllamaGenerator.
    """
    gen = await anext(get_generator(use_real=True, backend=GeneratorBackend.Ollama))
    assert isinstance(gen, OllamaGenerator)
