from app.evaluation.quality_gate import run_quality_gate


def test_quality_gate_fails_on_low_faithfulness(monkeypatch):
    # Mock aggregate_traces to return low faithfulness
    def mock_aggregate_traces():
        return {
            "runs": 10,
            "avg_recall_k": 0.8,
            "avg_faithfulness": 0.3,
        }

    monkeypatch.setattr(
        "app.evaluation.quality_gate.aggregate_traces", mock_aggregate_traces
    )
    monkeypatch.setenv("MIN_FAITHFULNESS", "0.5")

    exit_code = run_quality_gate()
    assert exit_code == 1, "Quality gate should fail on low faithfulness"
