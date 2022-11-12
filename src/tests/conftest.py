from __future__ import annotations

import logging
from logging import Logger
from pathlib import Path

from networkx import Graph
from pytest import fixture

from horus.nodes.project_logging import default_logging


@fixture
def test_logger() -> Logger:
    default_logging()

    logger = logging.getLogger(__name__)

    return logger


@fixture
def test_fixture() -> TestFixture:
    return TestFixture()


@fixture
def example_networkx_graph() -> Graph:  # type: ignore[no-any-unimported]
    nx_g = Graph()
    nx_g.add_nodes_from(
        [
            (0, {"ntype": "NTYPE1", "attr_key_1": "attr_val_1"}),
            (1, {"ntype": "NTYPE2", "attr_key_1": "attr_val_2"}),
        ]
    )
    nx_g.add_edges_from([(0, 1, {"etype": "ETYPE1"})])

    return nx_g


class TestFixture:
    @property
    def path_own_file(self) -> Path:
        return Path(__file__)

    @property
    def path_dir_test(self) -> Path:
        return self.path_own_file.parent
