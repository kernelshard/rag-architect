import re
from typing import Iterable


def _tokens(text: str) -> set[str]:
    """
    Tokenize the input text into a set of normalized words.
    """
    return set(re.findall(r"\b\w+\b", text.lower()))


def faithfulness_overlap(answer: str, contexts: Iterable[str]) -> float:
    """
    Calculate the faithfulness overlap score between the answer and provided contexts.
    The score is the ratio of overlapping words to total words in the answer.

    Args:
        answer (str): The generated answer text.
        contexts (Iterable[str]): A list of context strings.

    Returns:
        float: The faithfulness overlap score (0.0 to 1.0).
    """
    # Normalize and tokenize the answer
    answer_tokens = _tokens(answer)
    # means it has no tokens, e.g., empty strings
    if not answer_tokens:
        return 0.0

    # Normalize and tokenize all contexts
    context_tokens = set()
    for context in contexts:
        context_tokens.update(_tokens(context))

    # Calculate overlap score
    # intersection over answer tokens
    return round(len(answer_tokens & context_tokens) / len(answer_tokens), 4)
