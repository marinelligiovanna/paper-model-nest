from pynest.elements.bin import Bin
from pynest.elements.rect import Rect
import typing as tp

class PackingAlgorithm:

    def __init__(self, bin_width:float, bin_height:float, rects:tp.List[Rect]) -> None:
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.rects: tp.List[Rect] = rects
