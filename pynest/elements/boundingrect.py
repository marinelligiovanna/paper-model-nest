from pynest.elements.rect import Rect
from pynest.elements.piece import Piece
import numpy as np
from pynest.utils import convex_hull_polygon
from copy import deepcopy

class MinBoundingRect(Rect):
    """A Minimum Bouding Rectangle represents a rectangle envelope
    for a 2-d piece of the paper model.
    """
    
    def __init__(self, piece:Piece, shield:int = 2.5):
        super().__init__(0,0,0,0)
        self.piece: Piece = piece
        self.shield = shield

        self._set_bounding_rect()

    def _add_shield(self):
        self.width += 2 * self.shield
        self.height += 2 * self.shield
        self.piece.translate(self.shield, self.shield)

    def _set_bounding_rect(self):
        points = np.array(self.piece.to_points())
        convex_hull = convex_hull_polygon(points)

        min_area = np.Inf
        # Rotate the convex hull such that the current
        # segment is parallel to the x-axis.
        for segment in convex_hull.segments:
            theta = segment.x_angle()

            convex_hull_rotated = convex_hull.rotate(-theta, (0,0,))
            convex_hull_points = np.array(convex_hull_rotated.to_points())

            # Calculate bouding rectangle
            xs = convex_hull_points[:, 0]
            ys = convex_hull_points[:, 1]

            xmin = np.min(xs)
            xmax = np.max(xs)
            ymin = np.min(ys)
            ymax = np.max(ys)

            width = xmax - xmin
            height = ymax - ymin
            area = width * height

            # Save the bounding rectangle with the minimum area
            if area < min_area:
                min_area = area
                self.theta = theta
                self.x = xmin
                self.y = ymin
                self.width = width
                self.height = height
                
        # Rotathe the piece so that it fits into the bounding rectangle.
        self.piece.rotate(-self.theta, (0,0,), inplace=True)

        # Add a shield and translate both piece and the rectangle to origin
        self._add_shield()
        self.translate_to(0,0)

    def translate_to(self, x, y):
        x_dist = -self.x + x
        y_dist = -self.y + y
        self.translate(x_dist, y_dist)
        self.piece.translate(x_dist, y_dist)
        
    def plot(self, color=None, show_names:bool=True, show_rect:bool=True, **kwargs):
        if show_rect:
            super().plot(color="r")
        self.piece.plot(show_names)

    def rotated_90(self, inplace=False):
        angle = np.pi/2
        rect = self if inplace else deepcopy(self)

        rect.rotate_90(inplace=True)
        rect.piece.rotate(angle, center=(0,0,), inplace=True)
        rect.translate_to(0,0)

        return rect
