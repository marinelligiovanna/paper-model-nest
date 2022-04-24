import itertools
import typing as tp
from pynest.elements.rect import Rect

class Bin:

    def __init__(self, width:float, height:float) -> None:
        self.width = width
        self.height = height
        self.rects: tp.List[Rect] = []

        self.next = None

    def __repr__(self) -> str:
        return f"Bin({self.width}, {self.height})"

    def __next__(self):
        return self.next

    def add_next(self, next):
        self.next = next