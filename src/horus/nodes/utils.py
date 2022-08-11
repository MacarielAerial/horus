from typing import Dict


# TODO: strengthen type hints
def combine_hex_values(d: Dict[str, float]) -> str:
    """
    >>> combine_hex_values({"ffffff": 1.0, "0000ff": 0.5, "000000": 0.05})
    'a4a4f6'
    >>> combine_hex_values({"ffffff": 1.0, "0000ff": 0.5, "000000": 0.5})
    '7f7fbf'
    >>> combine_hex_values({"ffffff": 0.05, "0000ff": 1.0, "000000": 0.05})
    '0b0bf3'
    """
    d_items = sorted(d.items())
    tot_weight = sum(d.values())
    red = int(sum([int(k[:2], 16) * v for k, v in d_items]) / tot_weight)
    green = int(sum([int(k[2:4], 16) * v for k, v in d_items]) / tot_weight)
    blue = int(sum([int(k[4:6], 16) * v for k, v in d_items]) / tot_weight)
    zpad = lambda x: x if len(x) == 2 else "0" + x  # noqa

    return (  # type: ignore
        zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])
    )
