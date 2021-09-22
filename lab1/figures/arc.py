#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Arc(Figure):
    scale = 1

    radius = 70  # radius > Circle.radius
    delta_radius = 30

    angle_start = 1 / 8 * pi
    angle_end = 3 / 4 * pi

    def __init__(self, builder, center, d_width, d_height, scale=1):
        self.__builder = builder
        self.__center = center
        self.scale = scale

        self.__d_width = d_width
        self.__d_height = d_height

    def build(self):
        self.check()
        self.__big_arc()

    def check(self):
        if self.radius <= 0:
            raise ValueError(f'Arc.radius <= 0: {self.radius}')

        if self.delta_radius <= 0:
            raise ValueError(f'Arc.delta_radius <= 0: {self.delta_radius}')

    def __big_arc(self):
        self.__inside_arc()
        self.__outside_arc()
        self.__left_line()
        self.__right_line()

    def s_radius(self):
        return self.radius * self.scale

    def s_delta_radius(self):
        return self.delta_radius * self.scale

    def __inside_arc(self):
        self.__builder.build_arc(r=self.s_radius(),
                                 a1=self.angle_start, a2=self.angle_end,
                                 xy=self.__center)

    def __outside_arc(self):
        self.__builder.build_arc(r=self.s_radius() + self.s_delta_radius(),
                                 a1=self.angle_start, a2=self.angle_end,
                                 xy=self.__center)

    def __left_line(self):
        line_left_upper_x = self.s_radius() * np.cos(self.angle_start) + self.__d_width
        line_left_upper_y = self.s_radius() * np.sin(self.angle_start) + self.__d_height

        line_left_lower_x = (self.s_radius() + self.s_delta_radius()) * \
                            np.cos(self.angle_start) + self.__d_width
        line_left_lower_y = (self.s_radius() + self.s_delta_radius()) * \
                            np.sin(self.angle_start) + self.__d_height

        self.__builder.build_line(points=[
            (line_left_upper_x, line_left_upper_y),
            (line_left_lower_x, line_left_lower_y)
        ])

    def __right_line(self):
        line_right_upper_x = self.s_radius() * np.cos(self.angle_end) + self.__d_width
        line_right_upper_y = self.s_radius() * np.sin(self.angle_end) + self.__d_height

        line_right_lower_x = (self.s_radius() + self.s_delta_radius()) * \
                             np.cos(self.angle_end) + self.__d_width
        line_right_lower_y = (self.s_radius() + self.s_delta_radius()) * \
                             np.sin(self.angle_end) + self.__d_height

        self.__builder.build_line(points=[
            (line_right_upper_x, line_right_upper_y),
            (line_right_lower_x, line_right_lower_y)
        ])