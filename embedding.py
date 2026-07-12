def compute_embedding(note_json: dict, model):
    """
    Computes an embedding for a parsed note.

    Parameters
    ----------
    note_json : dict
        Dictionary containing:
        - title
        - text

    Returns
    -------
    list
        Embedding represented as a list of floats.
    """

    if not isinstance(note_json, dict):
        raise TypeError("note_json must be a dictionary.")

    title = note_json.get("title", "")
    text = note_json.get("text", "")

    if title == "" and text == "":
        raise ValueError("Note is empty.")

    # Combine title and body into one text
    full_text = f"{title}\n{text}"

    embedding = model.encode(full_text)

    # Convert NumPy array to normal Python list
    return embedding.tolist()