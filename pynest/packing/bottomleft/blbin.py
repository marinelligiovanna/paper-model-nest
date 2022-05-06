import typing as tp
from pynest.elements.rect import Rect
from pynest.packing.bin import Bin

class BLBin(Bin):

    def __init__(self, width:float, height:float) -> None:
        super().__init__(width, height)
        self.free_rects: tp.List[Rect] = [Rect(0, 0, width, height)]

    def _BL_criteria(self, free_rect:Rect, rect: Rect):
        """The Bottom-Left (BL) criteria consists in finding the 
        mininum height to put the rectangle and the minimum x axis value.
        The x-axis position is the second criteria to be considered

        Args:
            free_rect (Rect): The free rectangle to fit the rectangle.
            rect (Rect): The rectangle to be fitted
        """
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

    def _split_free_rect(self, free_rect:Rect, rect: Rect) -> tp.List[Rect]:
        """Given a free rectangle, split it into two
        parts to be the new free rectangles.

        Args:
            free_rect (Rect): The free rectangle to be splitted
            rect (Rect): The rectangle that created the split.

        Returns:
            tp.List[Rect]: The new free rectangles made from this one.
        """
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

    def _remove_intersection_from_rect(self, free_rect:Rect, intersection:Rect) -> tp.List[Rect]:
        """Give a free rectangle, remove an intersection rectangle, breaking
        the free_rectangle into multiple pieces.

        Args:
            free_rect (Rect): The free rectangle to have the intersection removed
            intersection (Rect): The intersection to be removed

        Returns:
            tp.List[Rect]: A list of new free rectangles made from the original
            free rectangle without the intersection.
        """
        fr = []

        # Rectangle at the left of the intersection
        if free_rect.left < intersection.left:
            fr.append(Rect(free_rect.x,
                          free_rect.y, 
                          intersection.left - free_rect.left, 
                          free_rect.height))
        # Rectangle at the bottom of the intersection
        if free_rect.bottom < intersection.bottom:
            fr.append(Rect(free_rect.x,
                          free_rect.y,
                          free_rect.width,
                          intersection.bottom - intersection.bottom))
        # Rectangle at the right of the intersection
        if free_rect.right > intersection.right:
            fr.append(Rect(intersection.right,
                          free_rect.y,
                          free_rect.right - intersection.right,
                          free_rect.height))
        # Rectangle at the top of the intersection
        if free_rect.top > intersection.top:
            fr.append(Rect(free_rect.x,
                          intersection.top,
                          free_rect.width,
                          free_rect.top - intersection.top))

        return fr

    def _remove_contained_rects(self, rects: tp.List[Rect]) -> tp.List[Rect]:
        """Given a list of rectangles, remove the
        rectangles that are contained in another one.

        Args:
            rects (tp.List[Rect]): The list of rectangles to remove
            the rectangles that are contained

        Returns:
            tp.List[Rect]: The new list without contained rectangles.
        """
        r = []
        N = len(rects)

        # Checks if the rectangle rects[i]
        # is contained in any other of the rectangles, except by
        # itself
        for i in range(0, N):
            ri = rects[i]
            append = True
            
            for j in range(0, N):
                rj = rects[j]

                if i != j and rj.contains(ri):
                    append = False
              
            if append:
                r.append(ri)

        return r

    def _remove_intersections(self, rect:Rect):
        r = []

        for free_rect in self.free_rects:
            if rect.intersects(free_rect):
                intersection = free_rect.intersection_with(rect)
                new_rects = self._remove_intersection_from_rect(free_rect, intersection)
                r = r + new_rects
            else:
                r.append(free_rect)

        r = self._remove_contained_rects(r)

        self.free_rects = r
        

    def insert(self, rect: Rect) -> bool:
        """Insert a rectangle into the bin.

        Args:
            rect (Rect): The rectangle to be inserted

        Returns:
            bool: True if it was possible to insert the rectangle into the bin and Fale otherwise
        """
        
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

            # Remove intersections with the current rectangle
            # and also fully-contained free rectangles
            self._remove_intersections(rect)


            return True

        return False
        
if __name__ == "__main__":
    bin = Bin(50,50)
    rect1 = Rect(0,0,10,10)
    bin.insert(rect1)
    rect2 = Rect(0,0,10,20)
    bin.insert(rect2)