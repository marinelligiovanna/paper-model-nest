from cmath import exp
from scipy.spatial import ConvexHull
from pynest.elements.segment import Segment
from pynest.elements.polygon import Polygon

def convex_hull_polygon(points):
    hull = ConvexHull(points)
    chull = Polygon()

    for simplex in hull.simplices:
        x = points[simplex, 0]
        y = points[simplex, 1]

        # print(p0, p1)
        s = Segment(x[0], y[0], x[1], y[1])
        chull.add_segment(s)

    return chull

def create_rectangle(xmin, xmax, ymin, ymax, expand_border:float = 2.5) -> Polygon:
    xmin -= expand_border
    xmax += expand_border
    ymin -= expand_border
    ymax += expand_border
    
    s1 = Segment(xmin, ymin, xmin, ymax)
    s2 = Segment(xmin, ymax, xmax, ymax)
    s3 = Segment(xmax, ymax, xmax, ymin)
    s4 = Segment(xmax, ymin, xmin, ymin)

    ret = Polygon()
    ret.add_segment(s1)
    ret.add_segment(s2)
    ret.add_segment(s3)
    ret.add_segment(s4)

    return ret