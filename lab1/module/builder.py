#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import os

import numpy as np
import gizeh

# Internal
from lab1.module.storage import Point, Line, points2line, line2points


class Builder:
    figures = []
    lines = []

    texts = []

    surface = None
    group = None

    d = 0.005

    def __init__(self, surf_width, surf_height, bg_color, stroke, stroke_width):
        self.__bg_color = bg_color

        self.__surf_width = surf_width
        self.__surf_height = surf_height

        self.__stroke = stroke
        self.__stroke_width = stroke_width

        self.__build_surface()

    def pi(self, x):
        return (-x) * np.pi

    def build_line(self, points, stroke=None, stroke_width=None):
        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        self.__add_figure({'line': points2line(points), 'stroke': stroke, 'stroke_width': stroke_width})

    def build_circle(self, r, xy, stroke=None, stroke_width=None):
        self.build_arc(r, self.pi(2), self.pi(0), xy, stroke=stroke, stroke_width=stroke_width)

    def build_circle_gizeh(self, r, xy, stroke=None, stroke_width=None):
        stroke, stroke_width = self.__handle_stroke(stroke, stroke_width)

        circle = gizeh.circle(r=r, xy=xy,
                              stroke=stroke, stroke_width=stroke_width)
        self.__add_figure(circle)

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

    def build_text(self, xy, text, stroke, fontsize, angle=0):
        self.texts.append({'xy': xy, 'text': text, 'stroke': stroke, 'angle': angle, 'fontsize': fontsize})

    def prepare_image(self):
        self.__draw_lines()
        self.group = gizeh.Group(self.figures)

    def cleanup(self):
        self.figures = []
        self.lines = []
        self.texts = []

        self.surface = gizeh.Surface(width=self.__surf_width, height=self.__surf_height, bg_color=self.__bg_color)

    def get_image(self):
        self.group.draw(self.surface)
        self.surface.write_to_png('source.png')

        self.cleanup()

    def get_image_local(self):
        self.group.draw(self.surface)

        return self.surface.get_npimage()

    def projective(self, x0, y0, w0, xx, yx, wx, xy, yy, wy):
        dx = self.__surf_width / 2
        dy = self.__surf_height / 2

        lines = []
        for line_data in self.lines:
            line = line_data['line']
            stroke = line_data['stroke']
            stroke_width = line_data['stroke_width']

            s_x = line.start.x - dx
            s_y = dy - line.start.y
            e_x = line.end.x - dx
            e_y = dy - line.end.y

            ns_x = self.__projective_x(s_x, s_y, x0, y0, w0, xx, yx, wx, xy, yy, wy) + dx
            ns_y = dy - self.__projective_y(s_x, s_y, x0, y0, w0, xx, yx, wx, xy, yy, wy)
            ne_x = self.__projective_x(e_x, e_y, x0, y0, w0, xx, yx, wx, xy, yy, wy) + dx
            ne_y = dy - self.__projective_y(e_x, e_y, x0, y0, w0, xx, yx, wx, xy, yy, wy)

            lines.append({'line': points2line([(ns_x, ns_y), (ne_x, ne_y)]),
                          'stroke': stroke, 'stroke_width': stroke_width})
        self.lines = lines

        texts = []
        for t in self.texts:
            x = t['xy'][0]
            y = t['xy'][1]

            text = t['text']
            stroke = t['stroke']
            angle = t['angle']
            fontsize = t['fontsize']

            s_x = x - dx
            s_y = dy - y

            ns_x = self.__projective_x(s_x, s_y, x0, y0, w0, xx, yx, wx, xy, yy, wy) + dx
            ns_y = dy - self.__projective_y(s_x, s_y, x0, y0, w0, xx, yx, wx, xy, yy, wy)

            texts.append({'xy': (ns_x, ns_y), 'text': text, 'stroke': stroke, 'angle': angle, 'fontsize': fontsize})

        self.texts = texts

    def __projective_x(self, x, y, x0, y0, w0, xx, yx, wx, xy, yy, wy):
        result = (x0 * w0 + xx * wx * x + xy * wy * y) \
                 / (w0 + wx * x + wy * y)
        return result

    def __projective_y(self, x, y, x0, y0, w0, xx, yx, wx, xy, yy, wy):
        result = (y0 * w0 + yx * wx * x + yy * wy * y) \
                 / (w0 + wx * x + wy * y)
        return result

    def affine(self, xx, yx, wx, xy, yy, wy):
        dx = self.__surf_width / 2
        dy = self.__surf_height / 2

        lines = []
        for line_data in self.lines:
            line = line_data['line']
            stroke = line_data['stroke']
            stroke_width = line_data['stroke_width']

            s_x = line.start.x - dx
            s_y = dy - line.start.y
            e_x = line.end.x - dx
            e_y = dy - line.end.y

            ns_x = self.__affine_x(s_x, s_y, xx, yx, wx, xy, yy, wy) + dx
            ns_y = dy - self.__affine_y(s_x, s_y, xx, yx, wx, xy, yy, wy)
            ne_x = self.__affine_x(e_x, e_y, xx, yx, wx, xy, yy, wy) + dx
            ne_y = dy - self.__affine_y(e_x, e_y, xx, yx, wx, xy, yy, wy)

            lines.append({'line': points2line([(ns_x, ns_y), (ne_x, ne_y)]),
                          'stroke': stroke, 'stroke_width': stroke_width})

        self.lines = lines

        texts = []
        for t in self.texts:
            x = t['xy'][0]
            y = t['xy'][1]

            text = t['text']
            stroke = t['stroke']
            angle = t['angle']
            fontsize = t['fontsize']

            s_x = x - dx
            s_y = dy - y

            ns_x = self.__affine_x(s_x, s_y, xx, yx, wx, xy, yy, wy) + dx
            ns_y = dy - self.__affine_y(s_x, s_y, xx, yx, wx, xy, yy, wy)

            texts.append({'xy': (ns_x, ns_y), 'text': text, 'stroke': stroke, 'angle': angle, 'fontsize': fontsize})

        self.texts = texts

    def __affine_x(self, x, y, xx, yx, wx, xy, yy, wy):
        result = xx * x + yx * y + wx
        return result

    def __affine_y(self, x, y, xx, yx, wx, xy, yy, wy):
        result = xy * x + yy * y + wy
        return result

    def shift_rotate(self, ox, oy, cx, cy, a):
        if ox != 0 or oy != 0:
            self.group = self.group.translate(xy=[ox, oy])
        if a != 0:
            self.group = self.group.rotate(self.pi(a), center=[cx, cy])

    def __draw_lines(self):
        for line_data in self.lines:
            line = line_data['line']
            stroke = line_data['stroke']
            stroke_width = line_data['stroke_width']
            gizeh_line = gizeh.polyline(points=line2points(line),
                                        stroke=stroke, stroke_width=stroke_width)

            self.__add_figure(gizeh_line)

        for text in self.texts:
            text = gizeh.text(text['text'], fontfamily="Arial", fontsize=text['fontsize'],
                              fill=text['stroke'], xy=text['xy'], angle=text['angle'])

            self.__add_figure(text)

    def __add_figure(self, figure):
        if type(figure) is dict:
            self.lines.append(figure)
        elif type(figure) is gizeh.Element:
            self.figures.append(figure)
        else:
            raise ValueError(type(figure))

    def __build_surface(self):
        self.surface = gizeh.Surface(width=self.__surf_width, height=self.__surf_height, bg_color=self.__bg_color)

    def __handle_stroke(self, stroke, stroke_width):
        if stroke is None:
            stroke = self.__stroke
        if stroke_width is None:
            stroke_width = self.__stroke_width

        return stroke, stroke_width
