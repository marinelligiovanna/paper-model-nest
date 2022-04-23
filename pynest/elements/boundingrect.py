from pynest.elements.polygon import Polygon
from pynest.elements.piece import Piece
import numpy as np
from pynest.utils import convex_hull_polygon, create_rectangle
import typing as tp

class BoundingRect:
    
    def __init__(self, piece:Piece, shield:int = 2.5):
        self.piece: Piece = piece
        self.shield = shield
        self.x = None
        self.y = None
        self.width = None
        self.height = None

        self._set_min_bounding_rect()

    def _add_shield(self):
        self.width += 2 * self.shield
        self.height += 2 * self.shield
        self.piece.translate(self.shield, self.shield)

    def _set_min_bounding_rect(self):
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

            if area < min_area:
                self.theta = theta
                self.x = xmin
                self.y = ymin
                self.width = width
                self.height = height
                # self.bounding_rect = rect
                # min_area = area

        self.piece.rotate(-self.theta, (0,0,), inplace=True)

        self._add_shield()
        self._translate_to_origin()

    def _translate_to_origin(self):
        self.piece.translate(-self.x, -self.y)
        self.x = 0.
        self.y = 0.

    def plot(self):
        x0 = self.x
        y0 = self.y
        x1 = self.x + self.width
        y1 = self.y + self.height
        
        rect = create_rectangle(x0, x1, y0, y1)
        rect.plot()