from __future__ import annotations

from logging import Logger
from pathlib import Path

import matplotlib.pyplot as plt
from pytest import fixture

from src.horus.nodes.base_logger import get_base_logger

plt.set_loglevel("error")


@fixture
def test_logger() -> Logger:
    return get_base_logger()


@fixture
def test_fixture() -> TestFixture:
    return TestFixture()


class TestFixture:
    @property
    def path_own_file(self) -> Path:
        return Path(__file__)

    @property
    def path_dir_test(self) -> Path:
        return self.path_own_file.parent

    @property
    def path_dir_data(self) -> Path:
        return self.path_dir_test / "data"

    @property
    def path_example_graph(self) -> Path:
        return self.path_dir_data / "example_graph.json"

    @property
    def path_dir_data_output(self) -> Path:
        return self.path_dir_data / "output"

    @property
    def path_matplotlib_vis_networkx(self) -> Path:
        return self.path_dir_data_output / "matplotlib_vis_networkx.png"
