import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


# ----------------------------
# Node
# ----------------------------

@dataclass
class Node:
    name: str # equal to title
    filename: str


# ----------------------------
# Edge
# ----------------------------

@dataclass
class Edge:
    start: str   # store node names instead of objects (simplifies JSON)
    end: str
    cosine: float


# ----------------------------
# Knowledge Graph
# ----------------------------

class KnowledgeGraph:
    def __init__(self, path: str):
        self.path = path

        # main storage (nested dict style as you wanted)
        self.graph = {
            "nodes": {},   # name -> Node dict
            "edges": []    # list of Edge dicts
        }

        self.load()

    # ----------------------------
    # Persistence
    # ----------------------------

    def save(self):
        """Save graph to JSON."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, indent=2)

    def load(self):
        """Load graph from JSON if exists."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.graph = json.load(f)
        except FileNotFoundError:
            self.graph = {"nodes": {}, "edges": []}

    # ----------------------------
    # Node logic
    # ----------------------------

    def create_node(self, title: str, filename: str):
        """
        Creates and adds a new node.
        """

        if title in self.graph["nodes"]:
            raise ValueError(f"Node '{title}' already exists")

        node = Node(
            name=title,
            filename=filename
        )

        self.graph["nodes"][node.name] = asdict(node)

        self.save()

    def get_node(self, name: str) -> Optional[dict]:
        return self.graph["nodes"].get(name)

    # ----------------------------
    # Edge logic
    # ----------------------------

    def create_edge(self, start: str, end: str, cosine: float):
        """
        Creates and adds an edge between two existing nodes.
        """

        if start not in self.graph["nodes"]:
            raise ValueError(f"Start node '{start}' does not exist")

        if end not in self.graph["nodes"]:
            raise ValueError(f"End node '{end}' does not exist")

        if start == end:
            raise ValueError("Cannot create edge to itself")

        # prevent duplicate edges
        for e in self.graph["edges"]:
            if e["start"] == start and e["end"] == end:
                return

        edge = Edge(
            start=start,
            end=end,
            cosine=cosine
        )

        self.graph["edges"].append(asdict(edge))

        self.save()

    def delete_node(self, node_name: str):
        """
        Deletes a node and all edges connected to it.
        """

        if node_name not in self.graph["nodes"]:
            raise ValueError(f"Node '{node_name}' does not exist.")

        # Remove the node
        del self.graph["nodes"][node_name]

        # Remove every edge connected to the node
        self.graph["edges"] = [
            edge for edge in self.graph["edges"]
            if edge["start"] != node_name and edge["end"] != node_name
        ]

        self.save()

    # ----------------------------
    # Relations helper
    # ----------------------------

    def read_relations(self, node_name: str) -> List[str]:
        """Return all nodes connected FROM given node."""
        return [
            e["end"]
            for e in self.graph["edges"]
            if e["start"] == node_name
        ]