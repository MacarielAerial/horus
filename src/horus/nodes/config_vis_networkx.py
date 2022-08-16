from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Type

from dataclasses_json import dataclass_json
from networkx import Graph


class VisNetworkXLayout(Enum):
    spring_layout: str = "spring_layout"
    graphviz_layout: str = "graphviz_layout"


class NodeFeatureKeyAsLabel(Enum):
    text: str = "text"
    ntype: str = "ntype"


@dataclass_json
@dataclass
class ConfigVisNetworkX:
    nfeat_ntype: str = "ntype"
    efeat_etype: str = "etype"
    nfeat_text: str = "text"
    nfeat_as_node_label: NodeFeatureKeyAsLabel = NodeFeatureKeyAsLabel.ntype
    with_edge_label: bool = True
    font_family: str = "SimHei"
    layout: VisNetworkXLayout = VisNetworkXLayout.graphviz_layout
    node_size: int = 75  # netowkrx library's default is 300
    width: float = 0.2  # default line width of edges is 1.0
    node_label_font_size: int = 1  # networkx library's default is 12
    edge_label_font_size: int = 1  # networkx library's default is 12
    figsize: Tuple[int, int] = (84, 84)  # This is already quite large
    dpi: int = 500  # High fidelity setting
    scale: float = 1  # Default is 1
    max_node_lab_len: int = 25
    null_node_label: str = "NULL"

    @classmethod
    def from_nx_g(  # type: ignore[no-any-unimported]
        cls, nx_g: Graph
    ) -> ConfigVisNetworkX:
        """Configures visualisation parameters based on those of a networkx graph"""
        n_nodes = int(nx_g.number_of_nodes())
        if n_nodes <= 200:
            return ConfigVisNetworkX(
                node_size=400,
                width=0.5,
                node_label_font_size=4,
                edge_label_font_size=2,
                figsize=(48, 48),
            )
        else:
            return ConfigVisNetworkX()


class HighContrastColourCode(Enum):
    blue_violet: str = "#8931EF"
    jonquil: str = "#F2CA19"
    shocking_pink: str = "#FF00BD"
    ryb_blue: str = "#0057E9"
    alien_armpit: str = "#87E911"


class RainbowColourCode(Enum):
    ryb_blue: str = "#0141F3"
    vivid_sky_blue: str = "#00D2EA"
    electric_green: str = "#02FB13"
    middle_yellow: str = "#FEE907"
    spanish_orange: str = "#EF6305"
    electric_red: str = "#E20806"


class Distinct25Colour(Enum):
    black: str = "#000000"
    dimgray: str = "#696969"
    saddlebrown: str = "#8b4513"
    midnightblue: str = "#191970"
    olive: str = "#808000"
    green: str = "#008000"
    yellowgreen: str = "#9acd32"
    darkorchid: str = "#9932cc"
    orangered: str = "#ff4500"
    orange: str = "#ffa500"
    yellow: str = "#ffff00"
    turquoise: str = "#40e0d0"
    chartreuse: str = "#7fff00"
    mediumspringgreen: str = "#00fa9a"
    royalblue: str = "#4169e1"
    crimson: str = "#dc143c"
    deepskyblue: str = "#00bfff"
    blue: str = "#0000ff"
    thistle: str = "#d8bfd8"
    fuchsia: str = "#ff00ff"
    palevioletred: str = "#db7093"
    khaki: str = "#f0e68c"
    deeppink: str = "#ff1493"
    lightsalmon: str = "#ffa07a"
    violet: str = "#ee82ee"


class ColourPaletteChoice(Enum):
    high_contrast_colour_code: Type[HighContrastColourCode] = HighContrastColourCode
    rainbow_colour_code: Type[RainbowColourCode] = RainbowColourCode
    distinct_25_colour: Type[Distinct25Colour] = Distinct25Colour
