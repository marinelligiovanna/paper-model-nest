from elements.rect import Rect
from pynest.elements.piece import Piece
import numpy as np
from pynest.utils import convex_hull_polygon

class BoundingRect:
    
    def __init__(self, piece:Piece, shield:int = 2.5):
        self.piece: Piece = piece
        self.shield = shield
        self.rect : Rect = None

        self._set_bounding_rect()

    def _add_shield(self):
        self.rect.width += 2 * self.shield
        self.rect.height += 2 * self.shield
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

            if area < min_area:
                min_area = area
                self.theta = theta
                self.rect = Rect(xmin, ymin, width, height)
                
        self.piece.rotate(-self.theta, (0,0,), inplace=True)

        self._add_shield()
        self._translate_to_origin()

    def _translate_to_origin(self):
        self.piece.translate(-self.x, -self.y)
        self.rect.translate_to(0,0)

    def plot(self):
        self.rect.plot()
        self.piece.plot()