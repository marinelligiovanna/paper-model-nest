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

    def plot(self, show_names: bool=True, show_rects:bool=True):
        plt.figure(figsize=(9,6))
        
        for rect in self.rects:
            rect.plot(color="r", show_names=show_names, show_rect=show_rects)

        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

    def save(self, fname:str, format:str="svg", **kwargs) -> None:
        self.plot(**kwargs)
        name = f"{fname}.{format}"
        plt.axis('off')
        plt.savefig(name, format=format, bbox_inches='tight', pad_inches=0)
        plt.close(name)