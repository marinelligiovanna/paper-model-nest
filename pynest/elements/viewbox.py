class ViewBox:

    def __init__(self, viewbox:str):
        viewbox_parts = viewbox.split(" ")
        viewbox_parts = [float(p) for p in viewbox_parts]
        self.xmin = viewbox_parts[0]
        self.ymin = viewbox_parts[1]
        self.width = viewbox_parts[2]
        self.height = viewbox_parts[3]