from pynest.elements.polygon import Polygon
from pynest.elements.segment import Segment
from pynest.elements.viewbox import ViewBox
import svg.path as spath
import typing as tp

class Piece(Polygon):
    
    def __init__(self, name:str = ""):
        super().__init__()
        self.name=name
        self.segments: tp.List[Segment] = []

    def _get_scale(self, width:float, viewbox:ViewBox):
        scale_width = viewbox.width - viewbox.xmin
        return width/scale_width

    def _apply_transform(self, segment:Segment, transform:str) -> Segment:
        if transform is None:
            return segment

        if transform.startswith('translate'):
            transform = transform.replace("translate", "")\
                                .replace("(", "")\
                                .replace(")", "")
            parts = transform.split(',')
            x_dist = float(parts[0])
            y_dist = float(parts[1])
            segment.translate(x_dist, y_dist)
        
        if transform.startswith("rotate"):
            transform = transform.replace("rotate", "")\
                                .replace("(", "")\
                                .replace(")", "")
            parts = transform.split(",")
            theta = float(parts[0])
            xc = float(parts[1])
            yc = float(parts[2])
            segment.rotate(theta, (xc, yc,))

        return segment

    def add_segments_from_path(self, d:str, width: float, viewbox:ViewBox, transform:str = None):
        # Convert to path object
        path = spath.parse_path(d)
        segments = path._segments
        n_segments = len(segments)

        scale = self._get_scale(width, viewbox)

        # Iterate in path and map segments
        for i in range(1, n_segments):
            segment = segments[i]

            start = segment.start
            end = segment.end

            x0 = start.real 
            y0 = start.imag 
            x1 = end.real 
            y1 = end.imag

            segment = Segment(x0,y0,x1,y1)
            segment = self._apply_transform(segment, transform)
            
            segment.x0 *= scale
            segment.x1 *= scale
            segment.y0 *= scale
            segment.y1 *= scale

            self.segments.append(segment)
