import gizeh


class Builder:
    figures = []
    surface = None

    def __init__(self, surf_width, surf_height, bg_color, stroke, stroke_width):
        self.__build_surface(surf_width, surf_height, bg_color)

        self.stroke = stroke
        self.stroke_width = stroke_width

    def build_line(self, points, stroke=None, stroke_width=None):
        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        line = gizeh.polyline(points=points,
                              stroke=stroke, stroke_width=stroke_width)
        line.draw(self.surface)

        self.figures.append(line)

    def build_circle(self, r, xy, stroke=None, stroke_width=None):
        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        circle = gizeh.circle(r=r, xy=xy,
                              stroke=stroke, stroke_width=stroke_width)
        circle.draw(self.surface)

        self.figures.append(circle)

    def build_arc(self, r, a1, a2, xy, stroke=None, stroke_width=None):
        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        arc = gizeh.arc(r=r, a1=a1, a2=a2, xy=xy,
                        stroke=stroke, stroke_width=stroke_width)
        arc.draw(self.surface)

        self.figures.append(arc)

    def get_image(self):
        return self.surface.get_npimage()

    def __build_surface(self, surf_width, surf_height, bg_color):
        self.surface = gizeh.Surface(width=surf_width, height=surf_height, bg_color=bg_color)

    def __handle_stroke(self, stroke, stroke_width):
        if stroke is None:
            stroke = self.stroke
        if stroke_width is None:
            stroke_width = self.stroke_width

        return stroke, stroke_width
