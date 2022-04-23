import numpy as np
from pynest.elements.segment import Segment
import matplotlib.pyplot as plt
import typing as tp

class Polygon:
    
    def __init__(self):
        self.segments = []

    def add_segment(self, segment:Segment):
        self.segments.append(segment)

    
    def to_points(self) -> tp.List[tp.Tuple[float, float]]:
        points = []
        for segment in self.segments:
            points.append(segment.start())
            points.append(segment.end())

        return points

    def plot(self) -> None:
        for segment in self.segments:
            plt.plot(np.array([segment.x0, segment.x1]), np.array([segment.y0, segment.y1]), 'k-')

    def centroid(self) -> tp.Tuple[float, float]:
        points = np.array(self.to_points())
        x_center = np.mean(points[:, 0])
        y_center = np.mean(points[:, 1])
        
        return (x_center, y_center,)

    def rotate(self, theta, center: tp.Tuple[float, float] = None, inplace=False):

        if center is None:
            center = self.centroid()
            
        points = np.array(self.to_points())

        P = np.array([points[:, 0], points[:, 1]])
        C = np.array([[center[0] for _ in range(0, P.shape[1])],
                      [center[1] for _ in range(0, P.shape[1])]])
        R = np.array([[np.cos(theta), -np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]])

        P = np.matmul(R, P - C) + C 

        if inplace:
            pol = self
        else:
            pol = Polygon()
            
        x0 = P[0,0]
        y0 = P[1,0]

        for i in range(1, P.shape[1]):
            x1 = P[0, i]
            y1 = P[1, i]
            pol.add_segment(Segment(x0, y0, x1, y1))

            x0 = x1
            y0 = y1

        return pol