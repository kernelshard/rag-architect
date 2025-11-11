import asyncio

from app.core.interfaces import BaseGenerator
from app.core.logging import get_logger

logger = get_logger(__name__)


class MockGenerator(BaseGenerator):
    """
    Pedicitable, latency-simulating mock text generator for dev/test.
    """

    def __init__(self, delay_seconds: float = 0.01):
        self.delay_seconds = delay_seconds

    async def generate(self, prompt: str) -> str:
        """
        Simulates text geneeration with a delay and returns a mock response.
        """
        await asyncio.sleep(self.delay_seconds)
        logger.debug(f"MockGenerator.generate received prompt: {prompt}")
        last_line = prompt.strip().splitlines()[-1] if prompt.strip() else ""
        return f"Mock answer -> {last_line or '[empty]'}"
