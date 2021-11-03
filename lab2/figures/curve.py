#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
from math import sin, cos, radians

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Curve(Figure):

    stroke = (1, 0, 0)
    stroke_tangent = (0, 1, 0)
    stroke_normal = (0, 0, 1)

    c = 1 / np.sqrt(2 * pi)

    y = [-1, 1]
    x = [-10, 10]
    x_a = [-100, 100]
    e = 0.15

    s = 1
    m = 0

    def __init__(self, builder, center, d_width, d_height):
        self.__builder = builder
        self.__center = center

        self.__d_width = d_width
        self.__d_height = d_height

    def func(self, x):
        a = self.c / self.s
        b = -(1 / 2) * ((x - self.m) / self.s) ** 2

        y = a * (np.e ** b)

        return y

    def derivative(self, x):
        return self.func(x) * (self.m - x) / (self.s ** 2)

    def tangent(self, x0):
        return lambda x: self.func(x0) + self.derivative(x0) * (x - x0)

    def normal(self, x0):
        return lambda x: self.func(x0) - (1 / self.derivative(x0)) * (x - x0)

    def build(self):
        x = np.arange(self.x[0] * 2, self.x[1] * 2 + self.e, self.e)
        y = self.get_points(x)

        # x[0]..x[1] -> 0..width
        x = [e * (self.__d_width / self.x[1]) + self.__d_width for e in x]
        # 0..1 -> 0..height
        y = [self.__d_height - e * self.__d_height for e in y]

        self.__curve(x, y)

    def build_tangent(self, x0):
        f = self.tangent(x0)

        x0 = self.x_a[0] * (self.__d_width / self.x[1]) + self.__d_width
        y0 = self.__d_height - f(self.x_a[0]) * self.__d_height
        x1 = self.x_a[1] * (self.__d_width / self.x[1]) + self.__d_width
        y1 = self.__d_height - f(self.x_a[1]) * self.__d_height

        xy0 = (x0, y0)
        xy1 = (x1, y1)

        line = [xy0,
                xy1]

        self.__builder.build_line_curve(line, stroke=self.stroke_tangent)

    def build_normal(self, x_0):
        f = self.tangent(x_0)

        x0 = self.x_a[0] * (self.__d_width / self.x[1]) + self.__d_width
        y0 = self.__d_height - f(self.x_a[0]) * self.__d_height
        x1 = self.x_a[1] * (self.__d_width / self.x[1]) + self.__d_width
        y1 = self.__d_height - f(self.x_a[1]) * self.__d_height

        xy0 = (x0, y0)
        xy1 = (x1, y1)

        o = (x_0 * (self.__d_width / 10) + self.__d_width,
             self.__d_height - self.func(x_0) * self.__d_height)

        line = [self.rotate(o, xy0, pi / 2),
                self.rotate(o, xy1, pi / 2)]


        self.__builder.build_line_curve(line, stroke=self.stroke_normal)

    @staticmethod
    def rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        import math
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    def get_points(self, x):
        y = []
        for x_i in x:
            y.append(self.func(x_i))

        return np.array(y)

    def __curve(self, x, y):
        points = list(zip(x, y))
        lines = [(points[i], points[i + 1]) for i in range(len(points) - 1)]

        for line in lines:
            self.__builder.build_line_curve(line, stroke=self.stroke)
