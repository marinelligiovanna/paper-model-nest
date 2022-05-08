import numpy as np
from pynest.elements.segment import Segment
import matplotlib.pyplot as plt
import typing as tp

class Polygon:
    """This class represents a Polygon as a set of 
    connected segments.
    """
    
    def __init__(self):
        self.segments : tp.List[Segment] = []

    def __repr__(self) -> str:
        repr = "Polygon("
        N = len(self.segments)

        for i in range(0, N):
            segment = self.segments[i]
            repr += f"\n\t{segment.__repr__()}"

            if i < N - 1:
                repr += ", "
        
        repr += ")"

        return repr
            
    def __iter__(self):
        return iter(self.segments)

    def add_segment(self, segment:Segment):
        """Add a segment to the polygon.

        Args:
            segment (Segment): The segment to be added
        """
        self.segments.append(segment)

    def to_points(self) -> tp.List[tp.Tuple[float, float]]:
        """Convert the polygon to a list of points.

        Returns:
            tp.List[tp.Tuple[float, float]]: A list of pais (x, y)
        """
        points = []
        for segment in self.segments:
            points.append(segment.start)
            points.append(segment.end)

        return points

    def points(self) -> tp.List[tp.Tuple[float, float]]:
        """Convert the polygon to a list of points.

        Returns:
            tp.List[tp.Tuple[float, float]]: A list of pais (x, y)
        """
        points = []
        for segment in self.segments:
            points.append(segment.start)
            points.append(segment.end)

        return points

    def centroid(self) -> tp.Tuple[float, float]:
        """Calculates the centroid of the polygon

        Returns:
            tp.Tuple[float, float]: A tuple (x,y) representing the coordinates of the centroid.
        """
        points = np.array(self.to_points())
        x_center = np.mean(points[:, 0])
        y_center = np.mean(points[:, 1])
        
        return (x_center, y_center,)

    def rotate(self, theta:float, center: tp.Tuple[float, float] = None, inplace=False):
        """Rotate the polygon to an angle theta around a center of mass.

        Args:
            theta (float): The angle to be rotated.
            center (tp.Tuple[float, float], optional): The center to rotate around. Defaults to the polygon centroid.
            inplace (bool, optional): A boolean describing if the current polygon will be rotated (True) or
                                      if the method will return a new polygon rotated (False). Defaults to False.
        """
        if center is None:
            center = self.centroid()
            
        # points = np.array(self.to_points())
        x = []
        y = []
        for segment in self.segments:
            x = x + [segment.x0, segment.x1]
            y = y + [segment.y0, segment.y1]

        P = np.array([x, y])
        C = np.array([[center[0] for _ in range(0, P.shape[1])],
                      [center[1] for _ in range(0, P.shape[1])]])
        R = np.array([[np.cos(theta), -np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]])

        P = np.matmul(R, P - C) + C 

        if inplace:
            pol = self
            self.segments = []
        else:
            pol = Polygon()
            
        for i in range(0, P.shape[1], 2):
            x0 = P[0, i]
            x1 = P[0, i+1]
            y0 = P[1, i]
            y1 = P[1, i+1]

            pol.add_segment(Segment(x0, y0, x1, y1))

        return pol

    def translate(self, x_dist: float, y_dist:float) -> None:
        """Translate the current polygon to a given x and y distance.

        Args:
            x_dist (float): The distance to translate the x coordinates. Positive values represents
            movements to the right and negative to the left of the x-axis.
            y_dist (float): The distance to translate the y coordinates. Positive values represents
            movements to the top and negative to the bottom of the y-axis.
        """
        for segment in self.segments:
            segment.translate(x_dist, y_dist)

    def plot(self) -> None:
        for segment in self.segments:
            # plt.plot(np.array([segment.x0, segment.x1]), np.array([segment.y0, segment.y1]), 'k-')
            segment.plot()