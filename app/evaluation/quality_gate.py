import sys
from pathlib import Path

# Ensure project root is importable when running as a script
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.evaluation.aggregate import aggregate_traces  # noqa: E402

MIN_RECALL_K = 0.5
MIN_FAITHFULNESS = None


def run_quality_gate() -> int:
    s = aggregate_traces()

    # No data -> don't fail the quality gate
    if s["runs"] == 0:
        print("No evaluation runs found. Quality gate passed.")
        return 0

    print(f"Evaluation results (n={s['runs']}):")
    if s["avg_recall_k"] is not None:
        print(f"  Recall@K: {s['avg_recall_k']:.3f} (threshold: {MIN_RECALL_K:.3f})")
    if s["avg_faithfulness"] is not None:
        threshold_str = (
            f"{MIN_FAITHFULNESS:.3f}" if MIN_FAITHFULNESS is not None else "N/A"
        )
        print(
            f"  Faithfulness: {s['avg_faithfulness']:.3f} (threshold: {threshold_str})"
        )

    if s["avg_recall_k"] is not None and s["avg_recall_k"] < MIN_RECALL_K:
        print(
            f"\n Quality gate FAILED: average Recall@K {s['avg_recall_k']:.3f} < {MIN_RECALL_K:.3f}"
        )
        return 1
    if MIN_FAITHFULNESS is not None and s["avg_faithfulness"] is not None:
        if s["avg_faithfulness"] < MIN_FAITHFULNESS:
            print(
                f"\n Quality gate FAILED: average Faithfulness {s['avg_faithfulness']:.3f} < {MIN_FAITHFULNESS:.3f}"
            )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_quality_gate())
