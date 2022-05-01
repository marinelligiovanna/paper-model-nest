import typing as tp

from numpy import rec
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

    def _free_rects_without_intersection(self, free_rect:Rect, intersection:Rect) ->tp.List[Rect]:
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
            fr.append(Rect(intersection.x,
                          free_rect.y,
                          free_rect.right - intersection.right,
                          free_rect.height))
        # Rectangle at the top of the intersection
        if free_rect.top > intersection.top:
            fr.append(Rect(free_rect.x,
                          intersection.y,
                          free_rect.width,
                          free_rect.top - intersection.top))

        return fr

    def _remove_contained_rects(self, rects: tp.List[Rect]) -> tp.List[Rect]:
        r = []
        N = len(rects)

        for i in range(0, N):
            ri = rects[i]
            append_ri = True
            
            for j in range(i+1, N):
                rj = rects[j]
                append_rj = True
                
                # Rj is contained in Ri - Do not append
                if ri.contains(rj):
                    append_rj = False
                # Ri is contained in Rj - Do not append
                elif rj.contains(ri):
                    append_ri = False
                
                if append_rj:
                    r.append(rj)

            if append_ri:
                r.append(ri)

        return r

    def _remove_intersections(self, rect:Rect):
        r = []

        for free_rect in self.free_rects:
            if rect.intersects(free_rect):
                intersection = free_rect.intersection_with(rect)
                new_rects = self._free_rects_without_intersection(free_rect, intersection)
                r = r + new_rects
            else:
                r.append(free_rect)

        r = self._remove_contained_rects(r)

        self.free_rects = r
        

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

            # Remove intersections with the current rectangle
            # and also fully-contained free rectangles
            self._remove_intersections(rect)


            return True

        return False
            