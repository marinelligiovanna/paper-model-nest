import numpy as np
import matplotlib.pyplot as plt

class Segment:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def __repr__(self) -> str:
        return f"Segment({self.x0}, {self.y0}, {self.x1}, {self.y1})"
    
    def start(self):
        return (self.x0, self.y0,)

    def end(self):
        return (self.x1, self.y1, )

    def x_angle(self) -> float:
        deltaX = self.x1 - self.x0
        deltaY = self.y1 - self.y0

        return np.arctan(deltaY/deltaX)

    def rotate(self,theta:float, center =(0,0,)):
        P = np.array([[self.x0, self.x1], 
                      [self.y0, self.y1]])
        C = np.array([[center[0], center[0]], 
                      [center[1], center[1]]])
        R = np.array([[np.cos(theta), -np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]])

        P = np.matmul(R, P - C) + C

        return Segment(P[0,0], P[1,0], P[0,1], P[1,1])

    def plot(self):
        points = np.array([self.start(), self.end()])
        plt.plot(points[:,0], points[:,1], 'k-', lw=1)