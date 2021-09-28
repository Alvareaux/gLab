#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Auxiliary(Figure):
    st_color_1 = (1, 0, 0)
    st_color_2 = (0, 1, 0)
    st_color_3 = (0, 0, 1)

    def __init__(self, builder, center, d_width, d_height,
                 arc, square, circle, perimeter,
                 scale=1):
        self.__builder = builder
        self.__center = center
        self.scale = scale

        self.__arc = arc
        self.__square = square
        self.__circle = circle
        self.__perimeter = perimeter

        self.__d_width = d_width
        self.__d_height = d_height

    def build(self):
        self._circle()
        self._arc()
        self._square()
        self._perimeter()

    def _circle(self):
        self.__circle_radius()

    def _arc(self):
        self.__arc_radius()
        self.__arc_radius_d()
        self.__arc_left_line()
        self.__arc_right_line()

    def _square(self):
        self.__square_offset()
        self.__square_side()

    def _perimeter(self):
        self.__perimeter_arc()
        self.__perimeter_ll()
        self.__perimeter_rl()
        self.__perimeter_ul()
        self.__perimeter_uld()

    def __circle_radius(self):
        r = self.__circle.s_radius()
        self.__builder.build_line(points=[
            (self.__d_width, self.__d_height),
            (self.__d_width + np.sqrt(2 * (r ** 2))/2, self.__d_height + np.sqrt(2 * (r ** 2))/2)
        ], stroke=self.st_color_1)

    def __arc_radius(self):
        r = self.__arc.s_radius()

        self.__builder.build_line(points=[
            (self.__d_width, self.__d_height),
            (self.__d_width, self.__d_height + r)
        ], stroke=self.st_color_1)

    def __arc_radius_d(self):
        r = self.__arc.s_radius()
        d = self.__arc.s_delta_radius()

        self.__builder.build_line(points=[
            (self.__d_width, self.__d_height + r),
            (self.__d_width, self.__d_height + r + d)
        ], stroke=self.st_color_2)

    def __arc_left_line(self):
        line_left_upper_x = self.__arc.s_radius() * np.cos(self.__builder.pi(self.__arc.angle_start)) + self.__d_width
        line_left_upper_y = self.__arc.s_radius() * np.sin(self.__builder.pi(self.__arc.angle_start)) + self.__d_height

        self.__builder.build_line(points=[
            (self.__d_width, self.__d_height),
            (line_left_upper_x, line_left_upper_y)
        ], stroke=self.st_color_3)

    def __arc_right_line(self):
        line_right_upper_x = self.__arc.s_radius() * np.cos(self.__builder.pi(self.__arc.angle_end)) + self.__d_width
        line_right_upper_y = self.__arc.s_radius() * np.sin(self.__builder.pi(self.__arc.angle_end)) + self.__d_height

        self.__builder.build_line(points=[
            (self.__d_width, self.__d_height),
            (line_right_upper_x, line_right_upper_y)
        ], stroke=self.st_color_3)

    def __square_offset(self):
        self.__builder.build_line(points=[
            (self.__d_width, self.__d_height),
            (self.__d_width + self.__square.s_x_offset(), self.__d_height - self.__square.s_y_offset())
        ], stroke=self.st_color_2)

    def __square_side(self):
        base_point = (self.__d_width + self.__square.s_x_offset(), self.__d_height - self.__square.s_y_offset())

        self.__builder.build_line(points=[
            (base_point[0] + self.__square.s_side(), base_point[1]),
            (base_point[0] + self.__square.s_side(), base_point[1] + self.__square.s_side())
        ], stroke=self.st_color_1)

    def __perimeter_arc(self):
        line_left_lower_x = self.__circle.s_radius() * \
                            np.cos(self.__builder.pi(3 / 4)) + self.__d_width
        line_left_lower_y = self.__circle.s_radius() * \
                            np.sin(self.__builder.pi(3 / 4)) + self.__d_height

        line_left_upper_x = (self.__perimeter.s_ua_delta_radius() + self.__circle.s_radius()) * \
                            np.cos(self.__builder.pi(3 / 4)) + self.__d_width
        line_left_upper_y = (self.__perimeter.s_ua_delta_radius() + self.__circle.s_radius()) * \
                            np.sin(self.__builder.pi(3 / 4)) + self.__d_height

        self.__builder.build_line(points=[
            (line_left_lower_x, line_left_lower_y),
            (line_left_upper_x, line_left_upper_y)
        ], stroke=self.st_color_3)

    def __perimeter_ll(self):
        self.__builder.build_line(points=[
            (self.__d_width, self.__d_height + self.__arc.s_radius() + self.__arc.s_delta_radius()),
            (self.__d_width,
             self.__d_height + self.__arc.s_radius() + self.__arc.s_delta_radius() + self.__perimeter.s_ll_delta())
        ], stroke=self.st_color_3)

    def __perimeter_rl(self):
        self.__builder.build_line(points=[
            (self.__d_width + self.__square.s_x_offset() + self.__square.s_side(),
             self.__d_height - self.__square.s_y_offset() + self.__square.s_side() / 2),
            (self.__d_width + self.__square.s_x_offset() + self.__square.s_side() + self.__perimeter.s_rl_delta(),
             self.__d_height - self.__square.s_y_offset() + self.__square.s_side() / 2)
        ], stroke=self.st_color_3)

    def __perimeter_ul(self):
        self.__builder.build_line(points=[
            (self.__d_width + self.__square.s_x_offset() + self.__square.s_side() / 2,
             self.__d_height - self.__square.s_y_offset()),
            (self.__d_width + self.__square.s_x_offset() + self.__square.s_side() / 2,
             self.__d_height - (self.__square.s_y_offset() + self.__perimeter.s_ul_delta()))
        ], stroke=self.st_color_3)

    def __perimeter_uld(self):
        self.__builder.build_line(points=[
            (self.__d_width + self.__square.s_x_offset() - self.__perimeter.s_ul_square_delta(),
             self.__d_height - (self.__square.s_y_offset() + self.__perimeter.s_ul_delta())),
            (self.__d_width + self.__square.s_x_offset(),
             self.__d_height - (self.__square.s_y_offset() + self.__perimeter.s_ul_delta()))
        ], stroke=self.st_color_2)

    # -----------------------------------------------------------------------------------------------------------------

    def circle_label(self):
        r = self.__circle.s_radius()
        return (self.__d_width + np.sqrt(2 * (r ** 2))/2, self.__d_height + np.sqrt(2 * (r ** 2))/2), self.st_color_1

    def arc_label_1(self):
        r = self.__arc.s_radius()

        return (self.__d_width, self.__d_height + r), self.st_color_1

    def arc_label_2(self):
        r = self.__arc.s_radius()
        d = self.__arc.s_delta_radius()

        return (self.__d_width, self.__d_height + r + d), self.st_color_2

    def arc_label_l(self):
        line_left_upper_x = self.__arc.s_radius() * np.cos(self.__builder.pi(self.__arc.angle_start)) + self.__d_width
        line_left_upper_y = self.__arc.s_radius() * np.sin(self.__builder.pi(self.__arc.angle_start)) + self.__d_height

        return (line_left_upper_x, line_left_upper_y), self.st_color_3

    def arc_label_r(self):
        line_right_upper_x = self.__arc.s_radius() * np.cos(self.__builder.pi(self.__arc.angle_end)) + self.__d_width
        line_right_upper_y = self.__arc.s_radius() * np.sin(self.__builder.pi(self.__arc.angle_end)) + self.__d_height

        return (line_right_upper_x, line_right_upper_y), self.st_color_3

    def square_label_offset(self):
        return (self.__d_width + self.__square.s_x_offset() / 2,
                self.__d_height - self.__square.s_y_offset() / 2), \
               self.st_color_2

    def square_label_side(self):
        return (self.__d_width + self.__square.s_x_offset() + self.__square.s_side() + self.__perimeter.s_rl_delta(),
                self.__d_height - self.__square.s_y_offset() + self.__square.s_side() / 2), \
               self.st_color_1

    def perimeter_label_arc(self):
        line_left_upper_x = (self.__perimeter.s_ua_delta_radius() + self.__circle.s_radius()) * \
                            np.cos(self.__builder.pi(3 / 4)) + self.__d_width
        line_left_upper_y = (self.__perimeter.s_ua_delta_radius() + self.__circle.s_radius()) * \
                            np.sin(self.__builder.pi(3 / 4)) + self.__d_height

        return (line_left_upper_x, line_left_upper_y), self.st_color_3

    def perimeter_label_ll(self):
        return (self.__d_width,
                self.__d_height + self.__arc.s_radius() + self.__arc.s_delta_radius()
                + self.__perimeter.s_ll_delta()), \
               self.st_color_3

    def perimeter_label_rl(self):
        return (self.__d_width + self.__square.s_x_offset() + self.__square.s_side() + self.__perimeter.s_rl_delta(),
                self.__d_height - self.__square.s_y_offset() + self.__square.s_side() / 2), self.st_color_3

    def perimeter_label_ul(self):
        return (self.__d_width + self.__square.s_x_offset() + self.__square.s_side() / 2,
                self.__d_height - (self.__square.s_y_offset() + self.__perimeter.s_ul_delta())), self.st_color_3

    def perimeter_label_uld(self):
        return (self.__d_width + self.__square.s_x_offset(),
                self.__d_height - (self.__square.s_y_offset() + self.__perimeter.s_ul_delta())), self.st_color_2
