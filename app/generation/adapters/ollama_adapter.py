import asyncio
from app.core.interfaces import BaseGenerator
from app.core.logging import get_logger


logger = get_logger(__name__)


class OllamaGenerator(BaseGenerator):
    """
    Async adapter for Ollama-style LLMs.
    """

    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name

    async def generate(self, prompt: str) -> str:
        logger.debug(f"[OllamaGenerator] Would call model={self.model_name}")
        await asyncio.sleep(0.5)  # simulate network delay
        # Placeholder for actual Ollama API call
        return f"[Simulated Ollama: {self.model_name} for prompt: {prompt[:60]}...]"
