import pytest
from app.generation.adapters.openai_adapter import OpenAIGenerator
from app.generation.deps import get_generator
from app.core.constants import GeneratorBackend


@pytest.mark.asyncio
async def test_get_generator_openai_selected():
    """
    Test that the OPENAI backend returns an OpenAIGenerator instance.
    """
    gen = await anext(get_generator(use_real=True, backend=GeneratorBackend.OPENAI))
    assert isinstance(gen, OpenAIGenerator)
