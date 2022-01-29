
class Point:
    """2-vector representing a polygon point"""
    def __init__(self, x, y):
        self.x, self.y = x, y

    def scale(self, scale=0.5):
        self.x *= scale
        self.y *= scale

    def move(self, x_offset, y_offset):
        self.x += x_offset
        self.y += y_offset


class EquilateralTriangle:
    def __init__(self, width):
        """Create 3 points representing an equilateral triangle on a PIL
        coordinate system (top-left==0,0 orientation)"""

        # positional / dimensional attributes
        self.width = width
        self.height = 3 ** .5 / 2 * width  # eq. for height of equilateral tri
        self.left = 0
        self.top = 0

        # Representation of triangle on an x,y coordinate plane
        self.tip = Point(width / 2, 0)
        self._points = (
            self.tip, Point(0, self.height), Point(width, self.height)
        )

    def _update_top_left(self):
        self.left = min(p.x for p in self._points)
        self.top = min(p.y for p in self._points)

    @property
    def points(self):
        return tuple((point.x, point.y) for point in self._points)

    @property
    def center_x(self):
        return self.left + self.width/2

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    def reposition(self, new_point):
        """Position the triangle with it's tip on the specified point"""
        # get x and y offsets for translation of triangle
        x_offset = -(self.tip.x - new_point[0])
        y_offset = -(self.tip.y - new_point[1])

        # move the triangle
        for point in self._points:
            point.move(x_offset, y_offset)

        self._update_top_left()

    def scale(self, scale=0.5):
        """Scale each point in the triangle/polygon by a scaling ratio. Updates
        triangle width and height by applying the same scaling factor. Updates
        topleft position"""
        for point in self._points:
            point.scale(scale)

        # update width height and top left
        self.width *= scale
        self.height *= scale
        self._update_top_left()

    def flip(self):
        """Flip self over horizontally (rotation parallel to x-axis)"""
        for point in self._points:
            point.y *= -1
