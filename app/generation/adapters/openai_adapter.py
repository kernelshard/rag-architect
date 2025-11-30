import asyncio

from app.core.interfaces import BaseGenerator
from app.core.logging import get_logger


logger = get_logger(__name__)


class OpenAIGenerator(BaseGenerator):
    """
    Async adapter for OpenAI-style LLMs.
    """

    def __init__(self, model_name: str = "gpt-4-turbo"):
        self.model_name = model_name

    async def generate(self, prompt: str) -> str:
        logger.debug(f"[OpenAIGenerator] would call model={self.model_name}")
        await asyncio.sleep(0.5)  # simulate network delay
        return f"[Simulated OpenAI: {self.model_name} for prompt: {prompt[:60]}...]"
