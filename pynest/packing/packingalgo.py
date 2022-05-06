from pynest.elements.rect import Rect
from pynest.packing import Bin
import typing as tp

class PackingAlgorithm:

    def __init__(self, bin_width:float, bin_height:float, rects:tp.List[Rect]) -> None:
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.rects: tp.List[Rect] = rects
        self.bins: tp.List[Bin] = []

    def pack(self):
        raise NotImplementedError