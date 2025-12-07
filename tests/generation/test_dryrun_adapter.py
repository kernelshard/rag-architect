import pytest

from app.generation.adapters.dryrun_adapter import DryRunGenerator


@pytest.mark.asyncio
async def test_dryrun_generator_basic():
    gen = DryRunGenerator(delay=0.0, fail_rate=0.0)
    out = await gen.generate("This is a test prompt for the DryRunGenerator.")
    assert out.startswith("[DryRun:")
    assert "This is a test prompt for the DryRunGenerator." in out
