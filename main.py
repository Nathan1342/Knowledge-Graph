import os
import json
import time

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from sentence_transformers import SentenceTransformer

from parser import parse_markdown
from embedding import compute_embedding
from similarity import compare_embeddings
from knowledge_graph import KnowledgeGraph


# ======================================================
# CONFIGURATION
# ======================================================

MAIN_FOLDER = Path("D:\Projects\Aktualne\knowledge_grapgh")

NOTES_MD = MAIN_FOLDER / "notes_md"
NOTES_JSON = MAIN_FOLDER / "notes_json"
GRAPH_FILE = MAIN_FOLDER / "graph.json"

SIMILARITY_THRESHOLD = 0.75


# ======================================================
# INITIALIZATION
# ======================================================

def initialize_folders():

    MAIN_FOLDER.mkdir(exist_ok=True)

    NOTES_MD.mkdir(exist_ok=True)

    NOTES_JSON.mkdir(exist_ok=True)

    if not GRAPH_FILE.exists():
        with open(GRAPH_FILE, "w") as f:
            json.dump(
                {
                    "nodes": {},
                    "edges": []
                },
                f,
                indent=2
            )


# ======================================================
# GLOBAL OBJECTS
# ======================================================

graph = None
model = None


def load_model():
    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return model



# ======================================================
# NOTE PROCESSING
# ======================================================

def process_new_or_changed_note(filepath):

    model = load_model()


    # -------------------------
    # Parse markdown
    # -------------------------

    note, json_path = parse_markdown(
        filepath, # filepath to md
        NOTES_JSON
    )


    # -------------------------
    # Compute embedding
    # -------------------------

    new_embedding = compute_embedding(
        note,
        model
    )


    filename = note["filename"]

    title = note["title"]


    # -------------------------
    # Add node if new
    # -------------------------

    if title not in graph.graph["nodes"]:

        graph.add_node(
            title,
            filename
        )


    # -------------------------
    # Compare with other notes
    # -------------------------

    for file in NOTES_JSON.iterdir():

        if file.name == json_path.name:
            continue


        with open(file, "r", encoding="utf-8") as f:
            other_note = json.load(f)


        other_embedding = compute_embedding(
            other_note,
            model
        )


        similarity = compare_embeddings(
            new_embedding,
            other_embedding
        )


        other_title = other_note["title"]


        if similarity >= SIMILARITY_THRESHOLD:

            graph.add_edge(
                title,
                other_title,
                similarity
            )


        else:

            graph.delete_edge(
                title,
                other_title
            )



# ======================================================
# DELETE NOTE
# ======================================================

def process_deleted_note(filepath):

    filename = Path(filepath).name


    for node_name, node in list(
        graph.graph["nodes"].items()
    ):

        if node["filename"] == filename:

            graph.delete_node(node_name)


    json_file = NOTES_JSON / (
        Path(filepath).stem + ".json"
    )


    if json_file.exists():
        json_file.unlink()



# ======================================================
# WATCHDOG
# ======================================================


class NotesHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if event.src_path.endswith(".md"):

            process_new_or_changed_note(
                event.src_path
            )


    def on_modified(self, event):

        if event.is_directory:
            return

        if event.src_path.endswith(".md"):

            process_new_or_changed_note(
                event.src_path
            )


    def on_deleted(self, event):

        if event.is_directory:
            return

        if event.src_path.endswith(".md"):

            process_deleted_note(
                event.src_path
            )



# ======================================================
# MAIN
# ======================================================


if __name__ == "__main__":


    initialize_folders()


    graph = KnowledgeGraph(
        GRAPH_FILE
    )


    load_model()


    observer = Observer()

    observer.schedule(
        NotesHandler(),
        NOTES_MD,
        recursive=False
    )


    observer.start()


    print("Knowledge graph running...")


    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()


    observer.join()