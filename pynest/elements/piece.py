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

    def add_segments_from_path(self, d:str, width: float, viewbox:ViewBox):
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

            x0 = start.real * scale
            y0 = start.imag * scale
            x1 = end.real * scale
            y1 = end.imag * scale

            self.segments.append(Segment(x0,y0,x1,y1))
