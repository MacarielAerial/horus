import logging
from pathlib import Path

import networkx as nx
import orjson
from networkx import Graph

logger = logging.getLogger(__name__)


class NetworkXGraphDataInterface:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    def save(self, data: Graph) -> None:  # type: ignore[no-any-unimported]
        self._save(filepath=self.filepath, data=data)

    @staticmethod
    def _save(filepath: Path, data: Graph) -> None:  # type: ignore[no-any-unimported]
        with open(filepath, "wb") as f:
            serialised = nx.node_link_data(G=data)
            f.write(orjson.dumps(serialised))

            logger.info(f"Saved a {type(data)} object to {filepath}")

    def load(self) -> Graph:  # type: ignore[no-any-unimported]
        return self._load(filepath=self.filepath)

    @staticmethod
    def _load(filepath: Path) -> Graph:  # type: ignore[no-any-unimported]
        with open(filepath, "rb") as f:
            serialised = orjson.loads(f.read())
            data = nx.node_link_graph(data=serialised)

            logger.info(f"Loaded a {type(data)} object from {filepath}")

            return data
