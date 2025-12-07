import asyncio
import time
from app.core.interfaces import BaseGenerator
from app.core.logging import get_logger


logger = get_logger(__name__)


class DryRunGenerator(BaseGenerator):
    """
    Pretend to be a real language model: give back a shortened prompt, run slow, and sometimes fail.
    """

    def __init__(
        self, delay: float = 0.02, fail_rate: float = 0.0, max_chars: int = 1000
    ):
        self.delay = delay
        self.fail_rate = fail_rate
        self.max_chars = max_chars

    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(self.delay)

        # Simulate failure
        # formula simplified - faile when fractional part of time is less than fail_rate
        # means it
        if self.fail_rate > 0 and (time.time() % 1) < self.fail_rate:
            logger.debug(
                f"[DryRunGenerator] Simulated failure for prompt: {prompt[:60]}..."
            )
            raise RuntimeError("Simulated trnsient generator failure")

        # return predictable summary
        short = prompt[: self.max_chars].strip()
        return f"[DryRun:{len(short)}] {short[-200:]}"
