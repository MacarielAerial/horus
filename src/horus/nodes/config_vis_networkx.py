from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from dataclasses_json import dataclass_json


class VisNetworkXLayout(Enum):
    spring_layout: str = "spring_layout"


class HexColourCode(Enum):
    blue_violet: str = "#8931EF"
    jonquil: str = "#F2CA19"
    shocking_pink: str = "#FF00BD"
    ryb_blue: str = "#0057E9"
    alien_armpit: str = "#87E911"


@dataclass_json
@dataclass
class ConfigVisNetworkX:
    nfeat_ntype: str = "ntype"
    nfeat_etype: str = "etype"
    layout: VisNetworkXLayout = VisNetworkXLayout.spring_layout
    node_size: int = 200  # netowkrx library's default is 300
    node_label_font_size: int = 8  # networkx library's default is 12
    edge_label_font_size: int = 4  # networkx library's default is 12
    figsize: Tuple[int, int] = (24, 24)  # This is already quite large
    dpi: int = 500  # High fidelity setting
