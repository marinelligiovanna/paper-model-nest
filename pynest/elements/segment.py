import numpy as np
import matplotlib.pyplot as plt

class Segment:
    """This class represents a line segment, represented
    by two points (x0, y0) and (x1, y1) on a plane.
    """
    def __init__(self, x0:float, y0:float, x1:float, y1:float):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def __repr__(self) -> str:
        return f"Segment(({self.x0}, {self.y0}) -> ({self.x1}, {self.y1}))"
    
    @property
    def start(self):
        return (self.x0, self.y0,)

    @property
    def end(self):
        return (self.x1, self.y1, )

    def x_angle(self) -> float:
        """Finds the angle between the current segment
        and the x-axis.

        Returns:
            float: The angle
        """
        deltaX = self.x1 - self.x0
        deltaY = self.y1 - self.y0

        return np.arctan(deltaY/deltaX)

    def rotate(self,theta:float, center =(0,0,)):
        """Rotate the current segment by an angle
        theta considering the given center.

        Args:
            theta (float): The angle to rotate the segment
            center (tuple, optional): The center to rotate around. Defaults to (0,0,).

        """
        P = np.array([[self.x0, self.x1], 
                      [self.y0, self.y1]])
        C = np.array([[center[0], center[0]], 
                      [center[1], center[1]]])
        R = np.array([[np.cos(theta), -np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]])

        P = np.matmul(R, P - C) + C

        return Segment(P[0,0], P[1,0], P[0,1], P[1,1])

    def plot(self):
        points = np.array([self.start, self.end])
        plt.plot(points[:,0], points[:,1], 'k-', lw=1)

    def translate(self, x_dist:float, y_dist:float) -> None:
        """Translates a segment to a given x and y distance.
        """
        self.x0 += x_dist
        self.y0 += y_dist
        self.x1 += x_dist
        self.y1 += y_dist