import logging
from typing import List

from networkx import Graph

logger = logging.getLogger(__name__)


def parse_node_hover_text(  # type: ignore[no-any-unimported]
    nx_g: Graph, ntype: str
) -> List[str]:
    node_text: List[str] = []
    for _, attrs in nx_g.nodes.data():
        if attrs["ntype"] == ntype:
            # Determine hover text based on the node type
            len_limit = 40

            # Only display short attributes
            corto_attrs = {}
            for k, v in attrs.items():
                if v is not None:
                    v_str = str(v)
                    if len(v_str) <= len_limit:
                        corto_attrs.update({k: v_str})

            hover_text = "<br>".join(f"{k}: {v}" for k, v in corto_attrs.items())

            node_text.append(hover_text)

    return node_text


def parse_edge_hover_text(  # type: ignore[no-any-unimported]
    nx_g: Graph, etype: str
) -> List[str]:
    edge_text: List[str] = []
    for _, _, attrs in nx_g.edges.data():
        if attrs["etype"] == etype:
            # Determine hover text based on the node type
            len_limit = 40

            # Only display short attributes
            corto_attrs = {}
            for k, v in attrs.items():
                if v is not None:
                    v_str = str(v)
                    if len(v_str) <= len_limit:
                        corto_attrs.update({k: v_str})

            hover_text = "<br>".join(f"{k}: {v}" for k, v in corto_attrs.items())

            edge_text.append(hover_text)

    return edge_text
