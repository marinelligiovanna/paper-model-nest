from pynest.packing import PackingAlgorithm
from pynest.packing.bottomleft import BLBin
from pynest.elements.rect import Rect
import typing as tp
import os
from pynest.elements.papermodel import PaperModel
from pynest.elements.boundingrect import MinBoundingRect

class BLPacker(PackingAlgorithm):

    def __init__(self, bin_width: float, bin_height: float, rects: tp.List[Rect]) -> None:
        super().__init__(bin_width, bin_height, rects)
        self.bins = []
        self.n_bins = 0
        self._add_bin()
        
    def _add_bin(self):
        print("Creating new bin!")
        bin = BLBin(self.bin_width, self.bin_height)
        self.bins.append(bin)
        self.n_bins += 1

    def pack(self):
        
        j = 0
        for rect in self.rects:
            i = 0
            inserted = False

            while not inserted:
                inserted = self.bins[i].insert(rect)

                if not inserted and i == self.n_bins - 1:
                    self._add_bin()
                
                i += 1
            j += 1

if __name__ == "__main__":
    data_path = f"{os.getcwd()}/pynest/data/svgs"
    model = PaperModel(f'{data_path}/harry-potter.svg')

    rects = []

    for piece in model.pieces:
        br = MinBoundingRect(piece)
        rects.append(br)

    rects.pop(21)
    rects.pop(28)
    rects.pop(30)
    rects.pop(30)
    packer = BLPacker(297,210, rects)
    packer.pack()
