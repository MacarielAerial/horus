from logging import Logger

from src.horus.nodes.matplotlib_vis_networkx import list_etype_to_dict_etype_colour
from tests.conftest import TestFixture


def test_list_etype_to_dict_etype_colour(
    test_fixture: TestFixture, test_logger: Logger
) -> None:
    dict_etype_colour = list_etype_to_dict_etype_colour(
        list_etype=test_fixture.example_list_etype, logger=test_logger
    )

    assert len(dict_etype_colour) > 0
