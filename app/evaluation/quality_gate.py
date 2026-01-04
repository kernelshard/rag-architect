import os
import sys
from pathlib import Path

# Ensure project root is importable when running as a script
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.evaluation.aggregate import aggregate_traces  # noqa: E402


def run_quality_gate() -> int:
    min_recall_k = float(os.getenv("MIN_RECALL_K", "0.5"))
    min_faithfulness_env = os.getenv("MIN_FAITHFULNESS")
    min_faithfulness = (
        float(min_faithfulness_env) if min_faithfulness_env is not None else None
    )

    s = aggregate_traces()

    # No data → don’t fail CI
    if s["runs"] == 0:
        return 0

    if s["avg_recall_k"] is not None and s["avg_recall_k"] < min_recall_k:
        print(f"Quality gate failed: avg_recall_k={s['avg_recall_k']} < {min_recall_k}")
        return 1

    if (
        min_faithfulness is not None
        and s["avg_faithfulness"] is not None
        and s["avg_faithfulness"] < min_faithfulness
    ):
        print(
            f"Quality gate failed: avg_faithfulness={s['avg_faithfulness']} < {min_faithfulness}"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_quality_gate())
