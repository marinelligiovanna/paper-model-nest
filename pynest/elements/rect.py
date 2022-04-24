import matplotlib.pyplot as plt

class Rect:

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"Rect({self.x}, {self.y}, {self.width}, {self.height})"

    def __iter__(self):
        yield self.bottom_left
        yield self.top_left
        yield self.top_right
        yield self.bottom_right

    def __lt__(self, rect):
        return self.area() < rect.area()
    
    @property
    def bottom(self):
        return self.y   

    @property
    def top(self):
        return self.y + self.height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom_left(self):
        return (self.left, self.bottom,)

    @property
    def bottom_right(self):
        return (self.right, self.bottom,)
    
    @property
    def top_left(self):
        return (self.left, self.top,)
    
    @property
    def top_right(self):
        return (self.right, self.top,)

    def translate_to(self, x, y):
        self.x = x
        self.y = y

    def area(self):
        return self.height * self.width

    def intersects(self, rect):
        if(self.bottom > rect.top) or (rect.bottom > self.top) or \
          (self.right < rect.left) or (rect.right < self.left):
          return False 

    def fit_into(self, rect):
        if rect.width < self.width and rect.height < self.height:
            return True
        return False

    def plot(self) -> None:
        xs = []
        ys = []
        for point in self:
            xs.append(point[0])
            ys.append(point[1])
        
        plt.plot(xs, ys, 'k-')
