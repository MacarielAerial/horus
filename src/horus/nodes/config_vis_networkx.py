from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from dataclasses_json import dataclass_json


class VisNetworkXLayout(Enum):
    spring_layout: str = "spring_layout"
    graphviz_layout: str = "graphviz_layout"


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


@dataclass_json
@dataclass
class ConfigVisNetworkX:
    nfeat_ntype: str = "ntype"
    efeat_etype: str = "etype"
    layout: VisNetworkXLayout = VisNetworkXLayout.graphviz_layout
    node_size: int = 200  # netowkrx library's default is 300
    width: float = 0.3  # default line width of edges is 1.0
    node_label_font_size: int = 4  # networkx library's default is 12
    edge_label_font_size: int = 4  # networkx library's default is 12
    figsize: Tuple[int, int] = (64, 64)  # This is already quite large
    dpi: int = 500  # High fidelity setting
    scale: float = 1  # Default is 1
