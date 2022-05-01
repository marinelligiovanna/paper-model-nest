import typing as tp
from pynest.elements.rect import Rect

class Bin:

    def __init__(self, width:float, height:float) -> None:
        self.width = width
        self.height = height
        self.rects: tp.List[Rect] = []
        self.free_rects: tp.List[Rect] = [Rect(0, 0, width, height)]
        self.available_area = width * height

        self.prev = None
        self.next = None

    def __repr__(self) -> str:
        return f"Bin({self.width}, {self.height})"

    def __next__(self):
        return self.next

    def _BL_criteria(self, free_rect:Rect, rect: Rect):
        return free_rect.y + rect.height, free_rect.x

    def _find_best_free_rect(self, rect: Rect) -> Rect:
        """Finds the best place to put the rectangle by using
        the bottom-left criteria

        Args:
            rect (Rect): The rectangle to insert

        Returns:
            Rect: The best free rect to put the rect
        """
        rects = []
        
        for free_rect in self.free_rects:
            if rect.fit_into(free_rect):
                criteria = self._BL_criteria(free_rect, rect)
                rects.append((criteria, free_rect))

        if len(rects) == 0:
            return None

        _, best_rect = min(rects, key = lambda x: x[0])

        return best_rect

    def _split_free_rect(self, free_rect:Rect, rect: Rect):
        parts = []

        # Horizontal split
        if rect.width < free_rect.width:
            x = free_rect.x + rect.width
            y = free_rect.y
            width = free_rect.width - rect.width
            height = free_rect.height

            parts.append(Rect(x, y, width, height))

        # Vertical split
        if rect.height < free_rect.height:
            x = free_rect.x
            y = free_rect.y + rect.height
            width = free_rect.width
            height = free_rect.height - rect.height

            parts.append(Rect(x, y, width, height))

        return parts

    def insert(self, rect: Rect):
        
        # It is not possible to insert the current
        # rectangle, since its area is greater than the
        # available area inside the bin
        if rect.area() > self.available_area:
            return False

        bfr = self._find_best_free_rect(rect)

        if bfr is not None:
            # Translate the rectangle to the x,y coordinates of the
            # free rectangle that it fits
            x, y = bfr.x, bfr.y
            rect.translate_to(x, y)

            # Decrement the available area inside the bin
            self.available_area -= rect.area()

            # Append the rectangle to the rectangles list
            self.rects.append(rect)
            
            # Add the new split parts to the free rectangles
            # and remove the best fit free rectangle
            parts = self._split_free_rect(bfr, rect)
            self.free_rects = self.free_rects + parts
            self.free_rects.remove(bfr)

            # Remove intersections


            return True

        return False
            