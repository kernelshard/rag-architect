from app.evaluation.faithfulness import faithfulness_overlap


def test_failthfulness_basic():
    """
    Test the basic functionality of faithfulness overlap calculation.
    """
    answer = "RAG combines retrieval and generation"
    contexts = ["retrieval augmented generation uses retrieval"]
    assert faithfulness_overlap(answer, contexts) == 0.4
