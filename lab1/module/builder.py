#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np
import gizeh

# Internal
from lab1.module.storage import Point, Line, points2line, line2points


class Builder:
    figures = []
    points = []
    surface = None

    d = 0.005

    def __init__(self, surf_width, surf_height, bg_color, stroke, stroke_width):
        self.__build_surface(surf_width, surf_height, bg_color)

        self.__surf_width = surf_width
        self.__surf_height = surf_height

        self.__stroke = stroke
        self.__stroke_width = stroke_width

    def pi(self, x):
        return (-x) * np.pi

    def build_line(self, points, stroke=None, stroke_width=None):
        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        line = gizeh.polyline(points=points,
                              stroke=stroke, stroke_width=stroke_width)

        self.__add_figure(points2line(points))
        self.__add_figure(line)

    def build_circle(self, r, xy, stroke=None, stroke_width=None):
        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        circle = gizeh.circle(r=r, xy=xy,
                              stroke=stroke, stroke_width=stroke_width)
        self.__add_figure(circle)

    def build_circle_gizeh(self, r, xy, stroke=None, stroke_width=None):
        self.build_arc(r, self.pi(0), self.pi(2), xy, stroke=stroke, stroke_width=stroke_width)

    def build_arc(self, r, a1, a2, xy, stroke=None, stroke_width=None):
        x0 = xy[0]
        y0 = xy[1]

        x = lambda t: x0 + r * np.cos(t)
        y = lambda t: y0 + r * np.sin(t)

        points = []

        for t in np.arange(self.pi(a2), self.pi(a1 - self.d), self.d):
            points.append((x(t), y(t)))

        for i in range(len(points) - 1):
            self.build_line([points[i], points[i + 1]], stroke=stroke, stroke_width=stroke_width)

    def build_arc_gizeh(self, r, a1, a2, xy, stroke=None, stroke_width=None):

        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        arc = gizeh.arc(r=r, a1=a1, a2=a2, xy=xy,
                        stroke=stroke, stroke_width=stroke_width)
        self.__add_figure(arc)

    def get_image(self):
        group = gizeh.Group(self.figures)
        #  group = self.shear(group, 0.7, 0.2)
        #  group = group.scale(0.7, center=(self.__surf_width / 2, self.__surf_height / 2))

        group.draw(self.surface)

        return self.surface.get_npimage()

    def shear(self, group, cx, cy):
        group = group.shear(cx, cy)
        group = group.translate((-400 * cx, -400 * cy))

        return group

    def interception_check(self):
        raise NotImplementedError

    def __add_figure(self, figure):
        if type(figure) is Line:
            self.points.append(figure)
        elif type(figure) is gizeh.Element:
            self.figures.append(figure)
        else:
            raise ValueError

    def __build_surface(self, surf_width, surf_height, bg_color):
        self.surface = gizeh.Surface(width=surf_width, height=surf_height, bg_color=bg_color)

    def __handle_stroke(self, stroke, stroke_width):
        if stroke is None:
            stroke = self.__stroke
        if stroke_width is None:
            stroke_width = self.__stroke_width

        return stroke, stroke_width
