import json
import time
from pathlib import Path
from typing import Iterable


TRACE_DIR = Path(__file__).parent.parent.parent / "var/traces"
TRACE_DIR.mkdir(parents=True, exist_ok=True)
TRACE_FILE = TRACE_DIR / "rage_trace.jsonl"


def write_trace(
    query: str,
    retrieved_ids: Iterable[str],
    answer_text: str,
    recall_k: float | None = None,
    faithfulness: float | None = None,
):
    """
    write trace of each generation to a JSONL file.

    :param query: Description
    :type query: str
    :param retrieved_ids: Description
    :type retrieved_ids: Iterable[str]
    :param answer_text: Description
    :type answer_text: str
    :param recall_k: Description
    :type recall_k: float | None
    :param faithfulness: Description
    :type faithfulness: float | None
    """
    record = {
        "ts": time.time(),
        "query": query,
        "retrieved_ids": list(retrieved_ids),
        "answer": answer_text,
        "recall_k": recall_k,
        "faithfulness": faithfulness,
    }

    with TRACE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
