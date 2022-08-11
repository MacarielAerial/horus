import json
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure
from networkx import DiGraph, Graph

from ..nodes.config_vis_networkx import ConfigVisNetworkX, VisNetworkXLayout
from ..nodes.matplotlib_vis_networkx import (
    dict_ntype_list_nid_to_dict_nid_colour,
    double_quote_double_colon_edge_attrs,
    double_quote_double_colon_node_attrs,
    layout_and_g_to_pos,
    list_ntype_to_dict_ntype_colour,
    nx_g_to_dict_eid_colour,
    nx_g_to_dict_ntype_list_nid,
    remove_all_node_attrs_except,
)


def _matplotlib_vis_networkx_pipeline(  # type: ignore[no-any-unimported]
    nx_g: Graph, config_vis_networkx: ConfigVisNetworkX, logger: Logger
) -> Figure:
    plt.set_loglevel("error")

    if nx_g.is_multigraph:
        logger.error(
            f"{nx_g} is multigraph which is not supported. "
            "converting multigraph to graph"
        )
        nx_g = DiGraph(nx_g)
        logger.info(f"Converted graph has {nx_g.number_of_edges()} edges")

    if config_vis_networkx.layout is VisNetworkXLayout.graphviz_layout:
        logger.info(
            f"Layout is chosen to be {config_vis_networkx.layout} "
            "which necessitates edge feature double colon check "
            "and alterations"
        )
        nx_g = remove_all_node_attrs_except(
            nx_g=nx_g, list_nfeat=[config_vis_networkx.nfeat_ntype], logger=logger
        )
        nx_g = double_quote_double_colon_edge_attrs(
            g=nx_g, efeat=config_vis_networkx.efeat_etype, logger=logger
        )
        nx_g = double_quote_double_colon_node_attrs(
            g=nx_g, nfeat=config_vis_networkx.nfeat_ntype, logger=logger
        )

    logger.info(f"Using {config_vis_networkx.layout} layout to plot matplotlib graph")

    # Prepare interim data structures before generating drawing specific variables
    dict_ntype_list_nid = nx_g_to_dict_ntype_list_nid(
        g=nx_g, nfeat_ntype=config_vis_networkx.nfeat_ntype, logger=logger
    )
    dict_ntype_colour = list_ntype_to_dict_ntype_colour(
        list_ntype=list(dict_ntype_list_nid.keys()), logger=logger
    )
    dict_nid_colour = dict_ntype_list_nid_to_dict_nid_colour(
        dict_ntype_colour=dict_ntype_colour,
        dict_ntype_list_nid=dict_ntype_list_nid,
        logger=logger,
    )
    dict_eid_colour = nx_g_to_dict_eid_colour(
        nx_g=nx_g, efeat_etype=config_vis_networkx.efeat_etype, logger=logger
    )

    # Parse data structures used to generate drawing
    pos = layout_and_g_to_pos(
        g=nx_g, vis_networkx_layout=config_vis_networkx.layout, logger=logger
    )
    pos = nx.rescale_layout_dict(pos=pos, scale=config_vis_networkx.scale)
    node_labels = nx.get_node_attributes(G=nx_g, name=config_vis_networkx.nfeat_ntype)
    edge_labels = nx.get_edge_attributes(G=nx_g, name=config_vis_networkx.efeat_etype)
    list_node_colour: List[str] = [dict_nid_colour[nid] for nid in list(nx_g.nodes)]
    list_edge_colour: List[str] = [dict_eid_colour[(u, v)] for u, v in list(nx_g.edges)]

    # Initiate a matplotlib Figure object
    fig = plt.figure(figsize=config_vis_networkx.figsize, dpi=config_vis_networkx.dpi)
    ax = fig.add_subplot(111)

    # Plot respective objects based on data structures parsed
    nx.draw_networkx_nodes(
        G=nx_g,
        pos=pos,
        ax=ax,
        node_color=list_node_colour,
        node_size=config_vis_networkx.node_size,
        label="This is where legend should be",
    )
    nx.draw_networkx_labels(
        G=nx_g,
        pos=pos,
        labels=node_labels,
        font_size=config_vis_networkx.node_label_font_size,
    )
    nx.draw_networkx_edges(
        G=nx_g,
        pos=pos,
        ax=ax,
        edge_color=list_edge_colour,
        width=config_vis_networkx.width,
        arrowsize=10 * config_vis_networkx.width,  # 10 is default
        label="This is edge legend",
    )
    if config_vis_networkx.with_edge_label:
        nx.draw_networkx_edge_labels(
            G=nx_g,
            pos=pos,
            ax=ax,
            edge_labels=edge_labels,
            font_size=config_vis_networkx.edge_label_font_size,
        )

    return fig


def matplotlib_vis_networkx_pipeline(
    path_nx_g: Path, path_vis_nx_g: Path, logger: Logger, **kwargs: Any
) -> None:
    # Data Access - Input
    with open(path_nx_g, "r") as f:
        data = json.load(f)
        nx_g = nx.node_link_graph(data)

    logger.info(f"Loaded a networkx graph from {path_nx_g}")

    config_vis_networkx = ConfigVisNetworkX(**kwargs)

    logger.info(
        "The visualisation run is configured as followed:\n" f"{config_vis_networkx}"
    )

    # Task Processing
    fig = _matplotlib_vis_networkx_pipeline(
        nx_g=nx_g, config_vis_networkx=config_vis_networkx, logger=logger
    )

    # Data Acess - Output
    if not path_vis_nx_g.parent.exists():
        path_vis_nx_g.parent.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"Parent directory of {path_vis_nx_g} does not exist. "
            f"Creating directory tree to {path_vis_nx_g.parent}"
        )

    fig.savefig(path_vis_nx_g)

    logger.info(f"Exported visualisation of {nx_g} to {path_vis_nx_g}")


if __name__ == "__main__":
    import argparse

    from ..nodes.base_logger import get_base_logger

    logger = get_base_logger()

    parser = argparse.ArgumentParser(
        description="Plot a networkx graph visualisation and save it to a path"
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
    parser.add_argument(
        "--edge-label",
        action=argparse.BooleanOptionalAction,
        default=True,
        required=False,
        help="Whether to draw edge labels",
    )

    args = parser.parse_args()

    kwargs: Dict[str, Any] = {"with_edge_label": args.edge_label}

    matplotlib_vis_networkx_pipeline(
        path_nx_g=args.path_nx_g,
        path_vis_nx_g=args.path_vis_nx_g,
        logger=logger,
        **kwargs,
    )
