import itertools
import typing as tp
from pynest.elements.rect import Rect

class Bin:

    def __init__(self, width:float, height:float) -> None:
        self.width = width
        self.height = height
        self.rects: tp.List[Rect] = []
        self.free_rects: tp.List[Rect] = [Rect(0, 0, width, height)]

        self.prev = None
        self.next = None

    def __repr__(self) -> str:
        return f"Bin({self.width}, {self.height})"

    def __next__(self):
        return self.next

    def _update_free_rects(self):
        pass

    def _add_rect(self, rect):
        pass

    def insert(self, rect:Rect):
        if rect.width > self.width or rect.height > self.height:
            raise Exception("The rectangle is greater than the bin dimensions!")

        for free_rect in self.free_rects:
            if free_rect.fits(rect):
                rect.translate_to(free_rect.x, free_rect.y)
                self.rects.append(rect)
                self._update_free_rects()

                return True

        return False