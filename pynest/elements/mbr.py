from pynest.elements.polygon import Polygon
from pynest.elements.segment import Segment
import numpy as np
from pynest.utils import convex_hull_polygon, create_rectangle
import typing as tp

class MinBoundingRect(Polygon):
    
    def __init__(self, piece):
        super.__init__()
        self.piece = piece
        self.rotated_piece = None
        self.rotated_convex_hull = None
        self.theta = None
        self.area = np.Inf
        self._set_min_bounding_rect()
        
    def _set_min_bounding_rect(self):
        points = np.array(self.piece.to_points())
        convex_hull = convex_hull_polygon(points)

        for segment in convex_hull.segments:
            theta = segment.x_angle()

            chull_rotated = convex_hull.rotate(-theta, (0,0,))
            chull_points = np.array(chull_rotated.to_points())

            xs = chull_points[:, 0]
            ys = chull_points[:, 1]

            xmin = np.min(xs)
            xmax = np.max(xs)
            ymin = np.min(ys)
            ymax = np.max(ys)

            ret_area = (ymax - ymin) * (xmax - xmin)
            ret = create_rectangle(xmin, xmax, ymin, ymax)

            if ret_area < self.area:
                self.theta = theta
                self.area = ret_area
                self.rotated_convex_hull = chull_rotated
                self.segments = ret.segments
        
        self.rotated_piece = self.piece.rotate(-self.theta, (0,0,))
    
    
    def to_polygon(self):
        polygon = Polygon()
        polygon.segments = self.segments

        return polygon

