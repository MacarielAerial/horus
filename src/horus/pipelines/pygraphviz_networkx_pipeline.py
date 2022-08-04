import json
from logging import Logger
from pathlib import Path

import networkx as nx


def pygraphviz_networkx_pipeline(
    path_nx_g: Path, path_vis_nx_g: Path, logger: Logger
) -> None:
    # Data Access - Input
    with open(path_nx_g, "r") as f:
        data = json.load(f)
        nx_g = nx.node_link_graph(data)

    logger.info(f"Loaded a networkx graph from {path_nx_g}")

    # Task Processing
    A = nx.nx_agraph.to_agraph(nx_g)
    A.layout()

    # Data Acess - Output
    A.draw(path_vis_nx_g.resolve())

    logger.info(f"Exported visualisation of {nx_g} to {path_vis_nx_g}")


if __name__ == "__main__":
    import argparse

    from ..nodes.base_logger import get_base_logger

    logger = get_base_logger()

    parser = argparse.ArgumentParser(
        description="Plot a networkx graph visualisation with pygraphviz "
        "and save it to a path"
    )
    parser.add_argument(
        "-png",
        "--path_nx_g",
        type=Path,
        required=True,
        help="Path to a networkx graph json object",
    )
    parser.add_argument(
        "-pvng",
        "--path_vis_nx_g",
        type=Path,
        required=True,
        help="Path to a png format networkx graph visualisation",
    )

    args = parser.parse_args()

    pygraphviz_networkx_pipeline(
        path_nx_g=args.path_nx_g, path_vis_nx_g=args.path_vis_nx_g, logger=logger
    )
