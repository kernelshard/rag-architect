from app.evaludation.recall import recall_at_k


def test_recall_at_k_basic():
    """
    Test basic functionality of recall_at_k.
    it should return correct recall value for simple cases.
    """
    retrieved_ids = ["doc1", "doc2", "doc3"]
    relevant_ids = {
        "doc2",
    }
    k = 3
    # it shall be 1/1 = 1.0
    # explaination:
    # relevant_ids has one document "doc2"
    # retrieved_ids has "doc2" within top 3
    #
    assert recall_at_k(retrieved_ids, relevant_ids, k) == 1.0
