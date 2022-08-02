from logging import Logger

from src.horus.pipelines.matplotlib_vis_networkx_pipeline import (
    matplotlib_vis_networkx_pipeline,
)
from tests.conftest import TestFixture


def test_matplotlib_vis_networkx_pipeline(
    test_logger: Logger, test_fixture: TestFixture
) -> None:
    if test_fixture.path_matplotlib_vis_networkx.is_file():
        test_fixture.path_matplotlib_vis_networkx.unlink()

    matplotlib_vis_networkx_pipeline(
        path_nx_g=test_fixture.path_example_graph,
        path_vis_nx_g=test_fixture.path_matplotlib_vis_networkx,
        logger=test_logger,
    )

    assert test_fixture.path_matplotlib_vis_networkx.is_file()
