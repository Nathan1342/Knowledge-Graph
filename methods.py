import os
from sklearn.metrics.pairwise import cosine_similarity


def parse_markdown(md_file_path: str, output_folder: str):
    """
    Parses a markdown note:
    - title = first line starting with #
    - text = everything else

    Saves result as JSON in output folder.
    """

    md_file_path = Path(md_file_path)
    output_folder = Path(output_folder)

    if not md_file_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_file_path}")

    output_folder.mkdir(parents=True, exist_ok=True)

    with open(md_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    title = None
    content_lines = []

    for line in lines:
        stripped = line.strip()

        # detect title
        if title is None and stripped.startswith("#"):
            # remove leading "#"
            title = stripped.lstrip("#").strip()
            continue

        content_lines.append(line.rstrip("\n"))

    if title is None:
        raise ValueError("No title found (missing '# Title' line)")

    note_text = "\n".join(content_lines).strip()

    result = {
        "title": title,
        "text": note_text,
        "filename": md_file_path.name
    }

    output_path = output_folder / f"{md_file_path.stem}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result, output_path


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

def compare_embeddings(embedding1: list, embedding2: list) -> float:
    """
    Computes cosine similarity between two embeddings.

    Returns a value between -1 and 1.
    """

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return float(similarity)