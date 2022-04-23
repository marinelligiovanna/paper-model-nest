from pynest.elements.polygon import Polygon
from pynest.elements.piece import Piece
from pynest.elements.segment import Segment
import numpy as np
from pynest.utils import convex_hull_polygon, create_rectangle
import typing as tp

class BoundingRect:
    
    def __init__(self, piece:Piece):
        super.__init__()
        self.piece: Piece = piece
        self.bounding_rect: Polygon = None

    def set_min_bounding_rect(self, rotate_piece:bool=True):
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

            area = (ymax - ymin) * (xmax - xmin)
            rect = create_rectangle(xmin, xmax, ymin, ymax)

            if area < min_area:
                self.theta = theta
                self.bounding_rect = rect
                min_area = area

        if rotate_piece:
            self.piece = self.piece.rotate(-self.theta, (0,0,))
    
        def rotate(theta:float, center:tp.Tuple[float, float] = None):
            self.piece = self.piece.rotate(theta, center)
            self.bounding_rect = self.bounding_rect.rotate(theta, center)
            self.theta = self.theta + theta

            return self

