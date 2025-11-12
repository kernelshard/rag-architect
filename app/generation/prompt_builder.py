def build_prompt(query: str, contexts: list[dict]) -> str:
    """
    Assembles a prompt text from retrieved contexts and the input query.

    Expects contexts as list of dicts, e.g.:
    [
        {"doc_id": "1", "score": 0.8, "metadata": {"text": "FastAPI is async..."}},
        ...
    ]
    """
    if not contexts:
        joined_contexts = "[No relevant context found.]"

    else:
        context_texts = []
        for c in contexts:
            meta = c.get("metadata", {})
            text = meta.get("text")
            if text:
                context_texts.append(text.strip())
            else:
                context_texts.append(f"[Doc:{c.get('doc_id', 'unknown')}]")

        joined_contexts = "\n\n".join(context_texts)
    return (
        f"### Contexts:\n{joined_contexts}\n\n"
        f"### Question:\n{query.strip()}\n\n"
        "### Answer:\n"
    )
