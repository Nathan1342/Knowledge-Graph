from templates import create_md_template
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("output_path", help="Path to notes' folder")
parser.add_argument("type", help="Type of note [alg/ds]")
parser.add_argument("title", help="Title of the note")

args = parser.parse_args()

create_md_template(Path(args.output_path), args.type, args.title)
