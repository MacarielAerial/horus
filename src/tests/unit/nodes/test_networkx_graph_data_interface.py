from logging import Logger
from pathlib import Path

from networkx import Graph

from horus.data_interaces.networkx_graph_data_interface import (
    NetworkXGraphDataInterface,
)


def test_networkx_graph_data_interface_save(  # type: ignore[no-any-unimported]
    test_logger: Logger, example_networkx_graph: Graph, tmp_path: Path
) -> None:
    filepath = tmp_path / "networkx_graph.json"

    networkx_graph_data_interface = NetworkXGraphDataInterface(filepath=filepath)
    networkx_graph_data_interface.save(data=example_networkx_graph)

    assert filepath.is_file()
