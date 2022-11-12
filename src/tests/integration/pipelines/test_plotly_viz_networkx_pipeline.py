from logging import Logger

from networkx import Graph
from plotly.graph_objects import Figure

from horus.pipelines.plotly_viz_networkx_pipeline import _plotly_viz_networkx_pipeline


def test_plotly_viz_networkx_pipeline(  # type: ignore[no-any-unimported]
    test_logger: Logger, example_networkx_graph: Graph
) -> None:
    fig = _plotly_viz_networkx_pipeline(nx_g=example_networkx_graph)

    assert isinstance(fig, Figure)
