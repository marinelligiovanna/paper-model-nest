from pynest.elements.rect import Rect
import typing as tp
import matplotlib.pyplot as plt

class Bin:
    """This class defines a bin of 
    a bin packing algorithm.
    """

    def __init__(self, width:float, height:float) -> None:
        self.width = width
        self.height = height
        self.available_area = width * height
        self.rects: tp.List[Rect] = []
        self.next = None
        self.prev = None


    def __repr__(self) -> str:
        return f"Bin({self.width}, {self.height})"

    def __next__(self):
        return self.next

    def insert(rect: Rect) -> bool:
        raise NotImplementedError()

    def plot(self):
        plt.figure(figsize=(9,6))
        for rect in self.rects:
            rect.plot(color="r")

        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
