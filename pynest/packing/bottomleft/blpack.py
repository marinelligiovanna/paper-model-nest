from packing.sorter import SortMethod
from pynest.packing import PackingAlgorithm
from pynest.packing.bottomleft import BLBin
from pynest.elements.rect import Rect
import typing as tp
from pynest.packing.sorter import sort_rects
class BLPacker(PackingAlgorithm):

    def __init__(self, bin_width: float, bin_height: float, rects: tp.List[Rect]) -> None:
        super().__init__(bin_width, bin_height, rects)
        self.bins = []
        self.n_bins = 0
        self.max_bins = 10
        self._add_bin()

    def free_area(self):
        fa = 0.0

        for bin in self.bins:
            fa += bin.free_area

        return fa
        
        
    def _add_bin(self):
        bin = BLBin(self.bin_width, self.bin_height)
        self.bins.append(bin)
        self.n_bins += 1

    def pack(self, allow_rotation:bool=True, sort_by: str = None):
        # Sort the rectangles before inserting into bins
        rects = sort_rects(self.rects, by=sort_by)
        
        for rect in rects:
            i = 0
            inserted = False

            while not inserted:
                inserted = self.bins[i].insert(rect, allow_rotation=allow_rotation)

                if not inserted and i == self.n_bins - 1:
                    self._add_bin()
                
                i += 1

