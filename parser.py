import json
from pathlib import Path

def parse_markdown(md_file_path: str, output_folder: Path):
    """
    Parses a markdown note:
    - title = first line starting with #
    - text = everything else

    Saves result as JSON in output folder.
    """

    md_file_path = Path(md_file_path)

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

def parser_algorithm(md_file_path: str, output_folder: Path):
    pass

def parser_data_structures(md_file_path: str, output_folder: Path):
    pass