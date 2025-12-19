from typing import Iterable, Set


def recall_at_k(retrieved_ids: Iterable[str], relevant_ids: Set[str], k: int) -> float:
    """
    Calculate Recall@K for a set of retrieved document IDs against relevant document IDs.

    Args:
        retrieved_ids (Iterable[str]): An iterable of retrieved document IDs.
        relevant_ids (Set[str]): A set of relevant document IDs.
        k (int): The cutoff rank K.

    Returns:
        float: The Recall@K value.
    """
    if k <= 0:
        raise ValueError("k must be a positive integer")

    relevant_ids_set = set(relevant_ids)

    # Limit retrieved IDs to top K
    if not relevant_ids_set:
        return 0.0

    # chunk retrieved_ids to top k
    top_k_retrieved_ids_set = set(list(retrieved_ids)[:k])

    return round(
        len(relevant_ids_set & top_k_retrieved_ids_set) / len(relevant_ids_set), 4
    )
