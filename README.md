# Knowledge Graph

A local knowledge management system that automatically creates connections between Markdown notes using semantic embeddings.

The goal is to transform a collection of separate notes into a connected knowledge graph.


## Features

- Automatically monitors a Markdown notes folder
- Parses Markdown files into structured JSON data
- Generates semantic embeddings using Sentence Transformers
- Calculates similarity between notes using cosine similarity
- Creates relationships between semantically similar notes
- Stores the knowledge graph locally as JSON
- Generates structured templates for algorithm and data structure notes


## How It Works

The system follows this pipeline:

Markdown Note -> Markdown Parser -> JSON Note -> Embedding Generation -> Similarity Comparison -> Knowledge Graph


When a new note is created, the system:

1. Parses the Markdown file.
2. Extracts the title and content.
3. Generates a semantic embedding.
4. Compares it with existing notes.
5. Creates graph connections when similarity exceeds the threshold.


## Technologies

- Python
- Sentence Transformers
- Scikit-learn
- Watchdog
- JSON


## Project Structure

main.py              - application entry point and folder monitoring  
parser.py            - Markdown parsing and JSON conversion  
embedding.py         - semantic embedding generation  
similarity.py        - cosine similarity calculation  
knowledge_graph.py   - graph data structure and persistence  
methods.py           - Markdown note templates


## Installation

Clone the repository:

git clone https://github.com/Nathan1342/Knowledge-Graph


Install dependencies:

pip install -r requirements.txt


Run:

python main.py


## Future Improvements

- Store embeddings permanently instead of recalculating them
- Add graph visualization
- Improve note update handling
- Add semantic search functionality
- Optimize performance for larger knowledge bases


## Learning Goals

This project explores:

- Natural language processing fundamentals
- Text embeddings and vector similarity
- Graph data structures
- File system monitoring
- Data persistence
- Software architecture design
