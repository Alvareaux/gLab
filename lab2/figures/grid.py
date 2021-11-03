#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Grid(Figure):
    st_color_grid = (200 / 255, 200 / 255, 200 / 255)
    st_width = 2

    st_color_axis = (100 / 255, 100 / 255, 100 / 255)
    st_width_axis = st_width

    point_len = 15
    point_angle = pi / 6

    def __init__(self, builder,
                 d, surf_width, surf_height):
        self.__builder = builder

        self.__d = d

        self.__surf_width = surf_width
        self.__surf_height = surf_height

    def build(self):
        self.__grid_h()
        self.__grid_v()

        self.__x_axis()
        self.__x_point()

        self.__y_axis()
        self.__y_point()

    def __grid_h(self):
        for i in range(self.__d, self.__surf_height, self.__d):
            self.__builder.build_line(points=[
                (0, i),
                (self.__surf_width, i)
            ], stroke=self.st_color_grid, stroke_width=self.st_width)

    def __grid_v(self):
        for i in range(self.__d, self.__surf_width, self.__d):
            self.__builder.build_line(points=[
                (i, 0),
                (i, self.__surf_height)
            ], stroke=self.st_color_grid, stroke_width=self.st_width)

    def __x_axis(self):
        self.__builder.build_line(points=[
            (0, self.__surf_height / 2),
            (self.__surf_width, self.__surf_height / 2)
        ], stroke=self.st_color_axis, stroke_width=self.st_width_axis)

    def __x_point(self):
        start = (self.__surf_width, self.__surf_height / 2)

        self.__builder.build_line(points=[
            start,
            (start[0] - self.point_len * np.cos(self.point_angle), start[1] - self.point_len * np.sin(self.point_angle))
        ], stroke=self.st_color_axis, stroke_width=self.st_width_axis * 1.5)

        self.__builder.build_line(points=[
            start,
            (start[0] - self.point_len * np.cos(self.point_angle), start[1] + self.point_len * np.sin(self.point_angle))
        ], stroke=self.st_color_axis, stroke_width=self.st_width_axis * 1.5)

    def __y_axis(self):
        self.__builder.build_line(points=[
            (self.__surf_width / 2, 0),
            (self.__surf_width / 2, self.__surf_height)
        ], stroke=self.st_color_axis, stroke_width=self.st_width_axis)

    def __y_point(self):
        start = (self.__surf_width / 2, 0)

        self.__builder.build_line(points=[
            start,
            (start[0] + self.point_len * np.sin(self.point_angle), start[1] + self.point_len * np.cos(self.point_angle))
        ], stroke=self.st_color_axis, stroke_width=self.st_width_axis)

        self.__builder.build_line(points=[
            start,
            (start[0] - self.point_len * np.sin(self.point_angle), start[1] + self.point_len * np.cos(self.point_angle))
        ], stroke=self.st_color_axis, stroke_width=self.st_width_axis)

