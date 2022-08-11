import random
from logging import Logger
from pprint import pformat
from typing import Dict, List, Tuple

from networkx import Graph, spring_layout
from networkx.drawing.nx_pydot import graphviz_layout
from numpy import ndarray

from .config_vis_networkx import (
    HighContrastColourCode,
    RainbowColourCode,
    VisNetworkXLayout,
)


def layout_and_g_to_pos(  # type: ignore[no-any-unimported]
    vis_networkx_layout: VisNetworkXLayout, g: Graph, logger: Logger
) -> Dict[int, ndarray]:
    if vis_networkx_layout is VisNetworkXLayout.spring_layout:
        pos: Dict[int, ndarray] = spring_layout(g)
    elif vis_networkx_layout is VisNetworkXLayout.graphviz_layout:
        pos = graphviz_layout(g)
    else:
        raise NotImplementedError(
            f"{vis_networkx_layout} is not implemented for visualisation"
        )

    logger.debug(f"Collected nid-position dictionary for {len(pos)} nodes")

    return pos


def nx_g_to_dict_ntype_list_nid(  # type: ignore[no-any-unimported]
    g: Graph, nfeat_ntype: str, logger: Logger
) -> Dict[str, List[int]]:
    # Initiate result variable
    dict_ntype_list_nid: Dict[str, List[int]] = {}

    logger.debug(
        f"Grouping nodes of {g} by their node type through node attribute "
        f"{nfeat_ntype}"
    )

    # Iterate over every node to determine its node type group membership
    for nid, ntype in g.nodes.data(nfeat_ntype):
        if ntype not in dict_ntype_list_nid.keys():
            dict_ntype_list_nid.update({ntype: [nid]})
        else:
            dict_ntype_list_nid[ntype].append(nid)

    return dict_ntype_list_nid


def count_n_nodes_by_ntype(
    dict_ntype_list_nid: Dict[str, List[int]], logger: Logger
) -> Dict[str, int]:
    # Collect a dictionary of numbers of nodes by node types
    dict_ntype_n_nodes: Dict[str, int] = {
        ntype: len(list_nid) for ntype, list_nid in dict_ntype_list_nid.items()
    }

    logger.info(
        "Collect the following numbers of nodes by their node types:\n"
        f"{pformat(dict_ntype_n_nodes)}"
    )

    return dict_ntype_n_nodes


def dict_ntype_list_nid_to_dict_nid_colour(
    dict_ntype_colour: Dict[str, HighContrastColourCode],
    dict_ntype_list_nid: Dict[str, List[int]],
    logger: Logger,
) -> Dict[int, str]:
    # Assign each node of every type a non-unique colour
    dict_nid_colour: Dict[int, str] = {}
    for ntype, list_nid in dict_ntype_list_nid.items():
        for nid in list_nid:
            colour = dict_ntype_colour[ntype]
            colour_str: str = colour.value
            dict_nid_colour.update({nid: colour_str})

    logger.debug(f"Assigned HEX colour code to {len(dict_nid_colour)} nodes")

    return dict_nid_colour


def list_ntype_to_dict_ntype_colour(
    list_ntype: List[str], logger: Logger
) -> Dict[str, HighContrastColourCode]:
    # Randomly assign one colour to each node type
    list_colour: List[HighContrastColourCode] = random.sample(
        list(HighContrastColourCode), k=len(list_ntype)
    )
    dict_ntype_colour: Dict[str, HighContrastColourCode] = dict(
        zip(list_ntype, list_colour)
    )

    logger.info(
        "Assigned colours to each node type with the following mapping:\n"
        f"{pformat(dict_ntype_colour)}"
    )

    return dict_ntype_colour


def nx_g_to_dict_eid_colour(  # type: ignore[no-any-unimported]
    nx_g: Graph, efeat_etype: str, logger: Logger
) -> Dict[Tuple[int, int], str]:
    # Initiate result object
    # e.g. {(0, 1): "#0141F3"}
    dict_eid_colour: Dict[Tuple[int, int], str] = {}

    # Gather all edge types
    list_etype: List[str] = []
    for _, _, etype in nx_g.edges.data(efeat_etype):
        if etype not in list_etype:
            list_etype.append(etype)

    # Assign one colour per edge type
    list_colour: List[RainbowColourCode] = random.sample(
        list(RainbowColourCode), k=len(list_etype)
    )
    dict_etype_colour: Dict[str, RainbowColourCode] = dict(zip(list_etype, list_colour))

    logger.info(
        "Assigned colours to each edge type with the following mapping:\n"
        f"{pformat(dict_etype_colour)}"
    )

    # Assign one colour (with duplicate) per edge id
    for u, v, etype in nx_g.edges.data(efeat_etype):
        colour = dict_etype_colour[etype]
        colour_str = colour.value
        dict_eid_colour.update({(u, v): colour_str})

    logger.info(f"Assigned colours to {len(dict_eid_colour)} edges")

    return dict_eid_colour


def double_quote_double_colon_edge_attrs(  # type: ignore[no-any-unimported]
    g: Graph, efeat: str, logger: Logger
) -> Graph:
    n_double_colon_edges: int = 0

    for src, dst, val in g.edges.data(efeat):
        has_double_colon: bool = False
        if isinstance(val, str):
            if ":" in val:
                g.edges[src, dst][efeat] = '"{}"'.format(val)
                has_double_colon = True
            else:
                continue
        else:
            raise TypeError(f"Edge attribute key {efeat} is not of type string")
        if has_double_colon:
            n_double_colon_edges += 1

    logger.debug(
        f"{n_double_colon_edges} edges' {efeat} attribute have double colons "
        "and are therefore double quoted"
    )

    return g


def double_quote_double_colon_node_attrs(  # type: ignore[no-any-unimported]
    g: Graph, nfeat: str, logger: Logger
) -> Graph:
    n_double_colon_nodes: int = 0

    for nid, val in g.nodes.data(nfeat):
        has_double_colon: bool = False
        if isinstance(val, str):
            if ":" in val:
                g.nodes[nid][nfeat] = '"{}"'.format(val)
                has_double_colon = True
            else:
                continue
        if has_double_colon:
            n_double_colon_nodes += 1

    logger.debug(
        f"{n_double_colon_nodes} nodes' {nfeat} attribute have double colons "
        "and are therefore double quoted"
    )

    return g


def remove_all_node_attrs_except(  # type: ignore[no-any-unimported]
    nx_g: Graph, list_nfeat: List[str], logger: Logger
) -> Graph:
    logger.info(
        f"Removing all node attributes except {list_nfeat} from "
        f"{nx_g.__class__} with {nx_g.number_of_nodes()} nodes"
    )

    # Initiate a logging variable
    dict_freq_nfeat_removed: Dict[str, int] = {}

    # Iteratively remove all node attributes unless
    # they are within the exception list
    for nid, attrs in nx_g.nodes.data():
        for k in list(attrs.keys()):
            if k not in list_nfeat:
                del nx_g.nodes[nid][k]
                if k not in dict_freq_nfeat_removed.keys():
                    dict_freq_nfeat_removed[k] = 1
                else:
                    dict_freq_nfeat_removed[k] += 1

    logger.info(
        "The frequency distribution of removed node attributes is:\n"
        f"{pformat(dict_freq_nfeat_removed)}"
    )

    return nx_g
