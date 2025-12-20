import json
from pathlib import Path


TRACE_FILE = Path(__file__).parent.parent.parent / "var/traces" / "rage_trace.jsonl"


def aggregate_traces() -> dict:
    """
    Aggregate traces from the JSONL trace file.
    Read the file line by line, parse each JSON record, and compute
    average metrics like recall_k and faithfulness.

    :return: Aggregated trace records.
    :rtype: dict
    """

    total = 0
    recall_k_sum = 0.0
    recall_n = 0  # recall_k_count
    faithfulness_sum = 0.0
    faithfulness_n = 0  # faithfulness_count

    if not TRACE_FILE.exists():
        return {
            "runs": 0,
            "avg_recall_k": None,
            "avg_faithfulness": None,
        }

    with TRACE_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            total += 1
            r = json.loads(line)
            if r.get("recall_k") is not None:
                recall_k_sum += r["recall_k"]
                recall_n += 1
            if r.get("faithfulness") is not None:
                faithfulness_sum += r["faithfulness"]
                faithfulness_n += 1

    return {
        "runs": total,
        "avg_recall_k": round(recall_k_sum / recall_n, 4) if recall_n > 0 else None,
        "avg_faithfulness": round(faithfulness_sum / faithfulness_n, 4)
        if faithfulness_n > 0
        else None,
    }
