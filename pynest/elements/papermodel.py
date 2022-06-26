from pynest.packing.bottomleft import BLPacker
from pynest.elements.piece import Piece
from pynest.elements.viewbox import ViewBox
from pynest.elements.boundingrect import MinBoundingRect
import typing as tp
import lxml.etree as xmltree
from pynest.elements.piece import Piece
from pynest.elements.viewbox import ViewBox

A4 = (297, 210,)
class PaperModel:

    def __init__(self, svg_path:str):
        self.svg_path = svg_path
        self.width = None
        self.height = None
        self.viewbox:ViewBox = None
        self.pieces: tp.List[Piece] = None
        self.bounding_rects: tp.List[MinBoundingRect] = None

        self._read_svg()
        self._set_bounding_rects()

    def _set_viewbox(self, root):
        vb = root.get('viewBox')
        self.viewbox = ViewBox(vb)
    
    def _set_dimensions(self, root):
        self.width = float(root.get('width').replace("mm", ""))
        self.height = float(root.get('height').replace("mm", ""))

    def _create_piece_from_paths(self, paths, name=None):
        piece = Piece(name=name)
        for path in paths:
            d = path.get('d')
            transform = path.get('transform')
            piece.add_segments_from_path(d, self.width, self.viewbox, transform=transform)

        return piece
    
    def _create_pieces_from_groups(self, groups, pieces, name=None):
        for group in groups:
            group_groups = group.findall(f'./{self.svg_ns}g')

            # Nested groups
            if len(group_groups) > 0:
                self._create_pieces_from_groups(group_groups, pieces, group.get('id'))
            # Groups containing only paths
            else:
                piece_name = name + "-" + group.get('id') 
                paths = group.findall(f'./{self.svg_ns}path')
                pieces.append(self._create_piece_from_paths(paths, piece_name))

    def _read_svg(self):
        svg = xmltree.parse(self.svg_path)

        # Name space 
        nsmap = svg.getroot().nsmap
        self.svg_ns = '{' + nsmap['svg'] + '}'

        # Parse svg, reading paths into pieces
        root = svg.getroot()
        self._set_viewbox(root)
        self._set_dimensions(root)

        # Group of pieces' groups is called "cut"
        cut = svg.find(f'.//{self.svg_ns}g[@id="cut"]')
        groups = cut.findall(f'./{self.svg_ns}g')
    	
        # Create pieces
        pieces = []
        self._create_pieces_from_groups(groups, pieces)

        # Remove pieces without len
        pieces = [p for p in pieces if len(p) > 0]

        self.pieces = pieces

    def _set_bounding_rects(self):
        self.bounding_rects = []

        for piece in self.pieces:
            mbr = MinBoundingRect(piece)
            self.bounding_rects.append(mbr)

    def pack_bottomleft(self, paper_dims:tp.Tuple[int, int] = A4):
        width, height = paper_dims
        packer = BLPacker(width, height, self.bounding_rects)
        packer.pack()

if __name__ == "__main__":
    import os
    data_path = f"{os.getcwd()}/pynest/data/svgs"

    model = PaperModel(f'{data_path}/e190-e2.svg')