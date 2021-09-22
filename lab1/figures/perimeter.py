#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Perimeter(Figure):
    scale = 1

    class UpperArc:
        angle_start = 1 / 1 * pi
        angle_end = 3 / 2 * pi
        delta_radius = 30

    class Arc:
        pass

    class LowerLine:
        delta = 20

    class RightLine:
        delta = 20

    class UpperLine:
        delta = 20
        square_delta = 10

    def __init__(self, builder, center, d_width, d_height,
                 arc, square, circle,
                 scale=1):
        self.__builder = builder
        self.__center = center
        self.scale = scale

        self.__arc = arc
        self.__square = square
        self.__circle = circle

        self.__d_width = d_width
        self.__d_height = d_height

    def build(self):
        self.check()
        self.__perimeter()

    def check(self):
        if self.LowerLine.delta <= 0:
            raise ValueError(f'Perimeter.LowerLine.delta <= 0: {self.LowerLine.delta}')

        if self.RightLine.delta <= 0:
            raise ValueError(f'Perimeter.RightLine.delta <= 0: {self.RightLine.delta}')

        if self.UpperLine.delta <= 0:
            raise ValueError(f'Perimeter.UpperLine.delta <= 0: {self.UpperLine.delta}')
        if self.UpperLine.square_delta <= 0:
            raise ValueError(f'Perimeter.UpperLine.square_delta <= 0: {self.UpperLine.square_delta}')
        upper_line_len = (self.__d_width + self.__square.s_x_offset() - self.s_ul_square_delta()) - \
                         (self.__d_width + self.__circle.s_radius() / 2)
        if upper_line_len <= 0:
            raise ValueError(f'Perimeter.upper_line_len <= 0: {upper_line_len}')

    def s_ll_delta(self):
        return self.LowerLine.delta * self.scale
    
    def s_rl_delta(self):
        return self.RightLine.delta * self.scale
    
    def s_ul_delta(self):
        return self.UpperLine.delta * self.scale

    def s_ul_square_delta(self):
        return self.UpperLine.square_delta * self.scale
    
    def s_ua_delta_radius(self):
        return self.UpperArc.delta_radius * self.scale

    def __perimeter(self):
        self.__upper_arc()
        lower_endpoint = self.__arc_line_lower()
        upper_endpoint = self.__arc_line_upper()

        right_endpoint = self.__line_lower(lower_endpoint)
        upper_right_endpoint = self.__line_right(right_endpoint)
        upper_left_endpoint = self.__upper_line(upper_right_endpoint)

        self.__angle_line(upper_endpoint, upper_left_endpoint)

    def __upper_arc(self):
        self.__builder.build_arc(r=self.__circle.s_radius() + self.s_ua_delta_radius(),
                                 a1=self.UpperArc.angle_start, a2=self.UpperArc.angle_end,
                                 xy=self.__center)

    def __arc_line_lower(self):
        x = self.__d_width - (self.__circle.s_radius() + self.s_ua_delta_radius())

        endpoint = (x, self.__d_height + self.__circle.s_radius())
        self.__builder.build_line(points=[
            (x, self.__d_height),
            endpoint
        ])

        return endpoint

    def __arc_line_upper(self):
        y = self.__d_height - (self.__circle.s_radius() + self.s_ua_delta_radius())

        endpoint = (self.__d_width + self.__circle.s_radius() / 2, y)
        self.__builder.build_line(points=[
            (self.__d_width, y),
            endpoint
        ])

        return endpoint

    def __line_lower(self, lower_endpoint):
        endpoint = (self.__d_width + self.__square.s_x_offset() + self.__square.s_side() + self.s_rl_delta(),
                    self.__d_height + self.__arc.s_radius() + self.__arc.s_delta_radius() + self.s_ll_delta())
        self.__builder.build_line(points=[
            (lower_endpoint[0],
             self.__d_height + self.__arc.s_radius() + self.__arc.s_delta_radius() + self.s_ll_delta()),
            endpoint
        ])

        return endpoint

    def __line_right(self, right_endpoint):
        endpoint = (right_endpoint[0],
                    self.__d_height - (self.__square.s_y_offset() + self.s_ul_delta()))
        self.__builder.build_line(points=[
            right_endpoint,
            endpoint
        ])

        return endpoint

    def __upper_line(self, upper_right_endpoint):
        endpoint = (self.__d_width + self.__square.s_x_offset() - self.s_ul_square_delta(),
                    upper_right_endpoint[1])
        self.__builder.build_line(points=[
            upper_right_endpoint,
            endpoint
        ])

        return endpoint

    def __angle_line(self, upper_endpoint, upper_right_endpoint):
        self.__builder.build_line(points=[
            upper_endpoint,
            upper_right_endpoint
        ])
