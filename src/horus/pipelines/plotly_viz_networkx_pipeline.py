import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import plotly.graph_objects as go
from networkx import Graph
from networkx.drawing.nx_agraph import graphviz_layout
from plotly.colors import DEFAULT_PLOTLY_COLORS
from plotly.graph_objects import Figure, Scatter

from horus.data_interaces.networkx_graph_data_interface import (
    NetworkXGraphDataInterface,
)
from horus.nodes.plotly_utils import parse_edge_hover_text, parse_node_hover_text

logger = logging.getLogger(__name__)


def _plotly_viz_networkx_pipeline(  # type: ignore[no-any-unimported] # noqa: C901
    nx_g: Graph, title_text: Optional[str] = None
) -> Figure:
    pos: Dict[int, Tuple[float, float]] = graphviz_layout(nx_g)

    #
    # Assign colour mapping to elements of different types
    #

    ntype_to_colour: Dict[str, str] = {}
    # Gather all node types that exist
    list_ntype: List[str] = []
    for _, ntype in nx_g.nodes.data("ntype"):
        if ntype not in list_ntype:
            list_ntype.append(ntype)
    for i, ntype in enumerate(list_ntype):
        ntype_to_colour.update({ntype: DEFAULT_PLOTLY_COLORS[i]})

    logger.debug(
        f"Node Type colour schema is designated as followed:\n{ntype_to_colour}"
    )

    etype_to_colour: Dict[str, str] = {}
    # Gather all edge types that exist
    list_etype: List[str] = []
    for _, _, etype in nx_g.edges.data("etype"):
        if etype not in list_etype:
            list_etype.append(etype)
    for i, etype in enumerate(list_etype):
        etype_to_colour.update({etype: DEFAULT_PLOTLY_COLORS[i + len(ntype_to_colour)]})

    logger.debug(
        f"Edge Type colour schema is designated as followed:\n{etype_to_colour}"
    )
    #
    # Prepare and define edge trace data
    #

    edge_traces: List[Scatter] = []  # type: ignore[no-any-unimported]
    for etype in etype_to_colour.keys():
        #
        # Prepare edge trace data
        #

        edge_x: List[Optional[float]] = []
        edge_y: List[Optional[float]] = []
        for src_nid, dst_nid, attrs in nx_g.edges.data():
            if attrs["etype"] == etype:
                edge_x.append(pos[src_nid][0])
                edge_x.append(pos[dst_nid][0])
                edge_x.append(None)

                edge_y.append(pos[src_nid][1])
                edge_y.append(pos[dst_nid][1])
                edge_y.append(None)

        edge_text = parse_edge_hover_text(nx_g=nx_g, etype=etype)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color=etype_to_colour[etype]),
            name=etype,
            text=edge_text,
            hovertemplate="<b>%{text}</b><extra></extra>",
            mode="lines",
            showlegend=True,
        )

        edge_traces.append(edge_trace)

    #
    # Prepare and define node traces
    #

    node_traces: List[Scatter] = []  # type: ignore[no-any-unimported]
    for ntype in ntype_to_colour.keys():
        #
        # Prepare node trace data
        #

        node_x: List[float] = []
        node_y: List[float] = []
        for nid, attrs in nx_g.nodes.data():
            if attrs["ntype"] == ntype:
                node_x.append(pos[nid][0])
                node_y.append(pos[nid][1])

        node_text = parse_node_hover_text(nx_g=nx_g, ntype=ntype)

        #
        # Define node trace
        #

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            marker=dict(
                color=ntype_to_colour[ntype],
                size=7,
                line=dict(width=2, color="DarkSlateGrey"),
            ),
            hovertemplate="<b>%{text}</b><extra></extra>",
            text=node_text,
            line_width=2,
            name=ntype,
            showlegend=True,
        )

        node_traces.append(node_trace)

    #
    # Initialise a plotly graph object
    #

    # Calculate an appropriate size based on the number of nodes
    width_to_n_node_prop = 1024 / 900
    height_to_n_node_prop = 768 / 900

    width = width_to_n_node_prop * len(nx_g)
    height = height_to_n_node_prop * len(nx_g)

    # Width and height cannot be smaller than a certain number
    if width < 10.0:
        width = 10.0
    if height < 10.0:
        height = 10.0

    title = f"<b>{title_text}</b>" if title_text else title_text

    fig = go.Figure(
        data=[*edge_traces, *node_traces],
        layout=go.Layout(
            autosize=False,
            width=width,
            height=height,
            title=title,
            titlefont_size=14,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig


def plotly_viz_networkx_pipeline(
    path_input_nx_g: Path, path_output_html: Path, title_text: Optional[str] = None
) -> None:
    # Data Access - Input
    networkx_graph_data_interface = NetworkXGraphDataInterface(filepath=path_input_nx_g)
    nx_g = networkx_graph_data_interface.load()

    # Task Processing
    fig = _plotly_viz_networkx_pipeline(nx_g=nx_g, title_text=title_text)

    # Data Access - Output
    fig.write_html(file=path_output_html)

    logger.info(f"A {type(fig)} object is saved to {path_output_html}")
