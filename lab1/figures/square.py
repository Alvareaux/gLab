#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Square(Figure):
    scale = 1

    x_offset = 80  # x_offset > Circle.radius
    y_offset = 80 + 50

    side = 50

    def __init__(self, builder, center, d_width, d_height, scale=1):
        self.__builder = builder
        self.__center = center
        self.scale = scale

        self.__d_width = d_width
        self.__d_height = d_height

    def build(self):
        self.check()
        self.__square()

    def check(self):
        if self.x_offset <= 0:
            raise ValueError(f'Square.x_offset <= 0: {self.x_offset}')
        if self.y_offset <= 0:
            raise ValueError(f'Square.y_offset <= 0: {self.y_offset}')

        if self.side <= 0:
            raise ValueError(f'Square.side <= 0: {self.side}')

    def s_x_offset(self):
        return self.x_offset * self.scale

    def s_y_offset(self):
        return self.y_offset * self.scale

    def s_side(self):
        return self.side * self.scale

    def __square(self):
        base_point = (self.__d_width + self.s_x_offset(), self.__d_height - self.s_y_offset())

        self.__square_line_lower(base_point)
        self.__square_line_left(base_point)
        self.__square_line_upper(base_point)
        self.__square_line_right(base_point)

    def __square_line_lower(self, base_point):
        self.__builder.build_line(points=[
            base_point,
            (base_point[0] + self.s_side(), base_point[1])
        ])

    def __square_line_left(self, base_point):
        self.__builder.build_line(points=[
            base_point,
            (base_point[0], base_point[1] + self.s_side())
        ])

    def __square_line_upper(self, base_point):
        self.__builder.build_line(points=[
            (base_point[0], base_point[1] + self.s_side()),
            (base_point[0] + self.s_side(), base_point[1] + self.s_side())
        ])

    def __square_line_right(self, base_point):
        self.__builder.build_line(points=[
            (base_point[0] + self.s_side(), base_point[1]),
            (base_point[0] + self.s_side(), base_point[1] + self.s_side())
        ])
