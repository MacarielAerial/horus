import dataclasses
import json
from logging import Logger
from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure
from networkx import DiGraph, Graph

from ..nodes.config_vis_networkx import (
    ConfigVisNetworkX,
    NodeFeatureKeyAsLabel,
    VisNetworkXLayout,
)
from ..nodes.matplotlib_vis_networkx import (
    double_quote_double_colon_edge_attrs,
    double_quote_double_colon_node_attrs,
    layout_and_g_to_pos,
    list_etype_to_dict_etype_colour,
    list_ntype_to_dict_ntype_colour,
    node_labels_raw_to_node_labels,
    nx_g_to_dict_etype_list_eid,
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
            nx_g=nx_g,
            list_nfeat=[
                config_vis_networkx.nfeat_ntype,
                config_vis_networkx.nfeat_as_node_label.value,
            ],
            logger=logger,
        )
        nx_g = double_quote_double_colon_edge_attrs(
            g=nx_g, efeat=config_vis_networkx.efeat_etype, logger=logger
        )
        nx_g = double_quote_double_colon_node_attrs(
            g=nx_g, nfeat=config_vis_networkx.nfeat_ntype, logger=logger
        )
        nx_g = double_quote_double_colon_node_attrs(
            g=nx_g, nfeat=config_vis_networkx.nfeat_text, logger=logger
        )

    logger.info(f"Using {config_vis_networkx.layout} layout to plot matplotlib graph")

    #
    # Prepare interim data structures before generating drawing specific variables
    #

    # Node colour
    dict_ntype_list_nid = nx_g_to_dict_ntype_list_nid(
        nx_g=nx_g, nfeat_ntype=config_vis_networkx.nfeat_ntype, logger=logger
    )
    dict_ntype_colour = list_ntype_to_dict_ntype_colour(
        list_ntype=list(dict_ntype_list_nid.keys()), logger=logger
    )

    # Edge colour
    dict_etype_list_eid = nx_g_to_dict_etype_list_eid(
        nx_g=nx_g, efeat_etype=config_vis_networkx.efeat_etype, logger=logger
    )
    dict_etype_colour = list_etype_to_dict_etype_colour(
        list_etype=list(dict_etype_list_eid.keys()), logger=logger
    )

    # Layout
    pos = layout_and_g_to_pos(
        g=nx_g, vis_networkx_layout=config_vis_networkx.layout, logger=logger
    )
    pos = nx.rescale_layout_dict(pos=pos, scale=config_vis_networkx.scale)

    # Labels
    node_labels_raw = nx.get_node_attributes(
        G=nx_g, name=config_vis_networkx.nfeat_as_node_label.value
    )
    node_labels = node_labels_raw_to_node_labels(
        node_labels_raw=node_labels_raw,
        nfeat_as_node_label=config_vis_networkx.nfeat_as_node_label,
        max_node_lab_len=config_vis_networkx.max_node_lab_len,
        null_node_label=config_vis_networkx.null_node_label,
        logger=logger,
    )
    edge_labels = nx.get_edge_attributes(G=nx_g, name=config_vis_networkx.efeat_etype)

    # Initiate a matplotlib Figure object
    fig = plt.figure(figsize=config_vis_networkx.figsize, dpi=config_vis_networkx.dpi)
    ax = fig.add_subplot(111)

    #
    # Plot respective objects based on data structures parsed
    #

    logger.info("Drawing elements onto a matplotlib figure...")

    # Draw nodes of different types
    for ntype, list_nid in dict_ntype_list_nid.items():
        nx.draw_networkx_nodes(
            G=nx_g,
            pos=pos,
            ax=ax,
            nodelist=list_nid,
            node_color=dict_ntype_colour[ntype].value,
            node_size=config_vis_networkx.node_size,
            label=ntype,
        )

    # Draw labels of nodes of different types
    nx.draw_networkx_labels(
        G=nx_g,
        pos=pos,
        labels=node_labels,
        font_family=config_vis_networkx.font_family,
        font_size=config_vis_networkx.node_label_font_size,
    )

    # Draw edges of different types
    for etype, list_eid in dict_etype_list_eid.items():
        nx.draw_networkx_edges(
            G=nx_g,
            pos=pos,
            ax=ax,
            edgelist=list_eid,
            edge_color=dict_etype_colour[etype].value,
            width=config_vis_networkx.width,
            arrowsize=10 * config_vis_networkx.width,  # 10 is default
            label=etype,
        )

    # Draw labels of edges of different types
    if config_vis_networkx.with_edge_label:
        nx.draw_networkx_edge_labels(
            G=nx_g,
            pos=pos,
            ax=ax,
            edge_labels=edge_labels,
            font_family=config_vis_networkx.font_family,
            font_size=config_vis_networkx.edge_label_font_size,
        )

    # Draw legend
    plt.legend(scatterpoints=1)

    return fig


def matplotlib_vis_networkx_pipeline(
    path_nx_g: Path, path_vis_nx_g: Path, logger: Logger, **kwargs: Any
) -> None:
    # Data Access - Input
    with open(path_nx_g, "r") as f:
        data = json.load(f)
        nx_g = nx.node_link_graph(data)

    logger.info(f"Loaded a networkx graph from {path_nx_g}")

    config_vis_networkx = ConfigVisNetworkX.from_nx_g(nx_g=nx_g)
    if len(kwargs) > 0:
        logger.info(
            f"Overwriting default values with the following dictionary:\n" f"{kwargs}"
        )
    # Overwrites default with supplied parameters
    config_vis_networkx = dataclasses.replace(config_vis_networkx, **kwargs)

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
        "-nanl",
        "--nfeat_as_node_label",
        type=NodeFeatureKeyAsLabel,
        default=NodeFeatureKeyAsLabel.ntype,
        required=False,
        help="Key to access a node feature used as node labels",
    )
    parser.add_argument(
        "--edge-label",
        action=argparse.BooleanOptionalAction,
        default=True,
        required=False,
        help="Whether to draw edge labels",
    )

    args = parser.parse_args()

    kwargs: Dict[str, Any] = {
        "with_edge_label": args.edge_label,
        "nfeat_as_node_label": args.nfeat_as_node_label,
    }

    matplotlib_vis_networkx_pipeline(
        path_nx_g=args.path_nx_g,
        path_vis_nx_g=args.path_vis_nx_g,
        logger=logger,
        **kwargs,
    )
