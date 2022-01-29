from PIL import Image, ImageDraw
from copy import deepcopy

from triangle import EquilateralTriangle

MAX_DEPTH = 7
BG_COLOR = 'black'
OUTER_COLOR = 'white'
INNER_COLOR = 'black'


def _recursive_draw_inner(tri, draw, max_depth, depth=0):
    """Given a triangle, scale the triangle by 1/2 then draw three similar
    triangles to the top, left, and right on the given triangle. For each
    sub-triangle created, repeat the process of copying, scaling, and drawing
    until the maximum depth is reached"""
    if depth >= max_depth:
        return

    # points where sub-triangle's tips will touch
    sub_points = (
        (tri.center_x, tri.top), (tri.left, tri.bottom), (tri.right, tri.bottom)
    )

    # scale the parent triangle by 1/2
    tri.scale(0.5)

    # moved scaled triangle to each point to draw sub-triangles
    for point in sub_points:
        tri.reposition(point)
        draw.polygon(tri.points, INNER_COLOR)
        # recursive step draws sub-triangles for this sub-triangle
        _recursive_draw_inner(deepcopy(tri), draw, max_depth, depth + 1)


def render_sierpinski(
        width,
        bg_color=None,
        outer_color=None,
        inner_color=None,
        max_depth=4
        ) -> Image:
    """Render a Sierpinski triangle with the specified color and depth.
    Returns PIL.Image object"""
    tri = EquilateralTriangle(width)

    # creating PIL image
    w, h = int(tri.width), int(tri.height)
    image = Image.new('RGB', (w, h), bg_color or BG_COLOR)
    draw = ImageDraw.Draw(image, 'RGB')

    # draw outer triangle
    draw.polygon(tri.points, fill=outer_color or OUTER_COLOR)

    # draw first inner triangle
    tri.scale(0.5)
    tri.flip()
    tri.reposition((w/2, h))
    draw.polygon(tri.points, fill=inner_color or INNER_COLOR)

    # draw interior triangles until the maximum depth is reached on each branch
    _recursive_draw_inner(tri, draw, max_depth)

    return image


if __name__ == '__main__':
    def main():
        im = render_sierpinski(7 * 10**3, max_depth=8)
        im.show()
    main()
