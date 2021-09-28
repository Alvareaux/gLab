#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Text(Figure):
    if_auxiliary = False

    st_color_axis = (100 / 255, 100 / 255, 100 / 255)

    st_color_1 = (1, 0, 0)
    st_color_2 = (0, 1, 0)
    st_color_3 = (0, 0, 1)

    __fontsize = 18

    __offset_x = -15
    __offset_y = -15

    def __init__(self, builder, center, d_width, d_height,
                 aux,
                 scale=1):
        self.__builder = builder
        self.__center = center
        self.scale = scale

        self.__aux = aux

        self.__d_width = d_width
        self.__d_height = d_height

    def fontsize(self):
        return self.__fontsize * self.scale

    def offset_x(self):
        return self.__offset_x * self.scale + self.__d_width

    def offset_y(self):
        return self.__d_height - self.__offset_y * self.scale

    def build(self):
        self.__zero()
        self.__x()
        self.__y()

    def build_aux(self):
        self.__labels_circle()

        self.__labels_arc_1()
        self.__labels_arc_2()
        self.__labels_arc_l()
        self.__labels_arc_r()

        self.__labels_square_offset()
        self.__labels_square_side()

        self.__labels_perimeter_arc()
        self.__labels_perimeter_ll()
        self.__labels_perimeter_rl()
        self.__labels_perimeter_ul()
        self.__labels_perimeter_uld()

    def __zero(self):
        self.__builder.build_text((self.offset_x(), self.offset_y()),
                                  '0', self.st_color_axis, self.fontsize())

    def __x(self):
        self.__builder.build_text((self.offset_x() + self.__d_width, self.offset_y()),
                                  'x', self.st_color_axis, self.fontsize())

    def __y(self):
        self.__builder.build_text((self.offset_x(), self.offset_y() - self.__d_height),
                                  'y', self.st_color_axis, self.fontsize())

    def __labels_circle(self):
        xy, st = self.__aux.circle_label()
        self.__builder.build_text((xy[0] + 10 * self.scale, xy[1] + 10 * self.scale),
                                  'cR', st, self.fontsize())

    def __labels_arc_1(self):
        xy, st = self.__aux.arc_label_1()
        self.__builder.build_text((xy[0] - 10 * self.scale, xy[1] - 10 * self.scale),
                                  'ar', st, self.fontsize())

    def __labels_arc_2(self):
        xy, st = self.__aux.arc_label_2()
        self.__builder.build_text((xy[0] - 18 * self.scale, xy[1] - 10 * self.scale),
                                  'adR', st, self.fontsize())

    def __labels_arc_l(self):
        xy, st = self.__aux.arc_label_l()
        self.__builder.build_text((xy[0] - 9 * self.scale, xy[1] - 10 * self.scale),
                                  'aS', st, self.fontsize())

    def __labels_arc_r(self):
        xy, st = self.__aux.arc_label_r()
        self.__builder.build_text((xy[0] + 18 * self.scale, xy[1] - 10 * self.scale),
                                  'aM', st, self.fontsize())

    def __labels_square_offset(self):
        xy, st = self.__aux.square_label_offset()
        self.__builder.build_text((xy[0] - 30 * self.scale, xy[1]),
                                  'sOxy', st, self.fontsize())

    def __labels_square_side(self):
        xy, st = self.__aux.square_label_side()
        self.__builder.build_text((xy[0] - 35 * self.scale, xy[1] - 15 * self.scale),
                                  'sA', st, self.fontsize())

    def __labels_perimeter_arc(self):
        xy, st = self.__aux.perimeter_label_arc()
        self.__builder.build_text((xy[0] - 15 * self.scale, xy[1] - 15 * self.scale),
                                  'uaD', st, self.fontsize())

    def __labels_perimeter_ll(self):
        xy, st = self.__aux.perimeter_label_ll()
        self.__builder.build_text((xy[0], xy[1] + 15 * self.scale),
                                  'llD', st, self.fontsize())

    def __labels_perimeter_rl(self):
        xy, st = self.__aux.perimeter_label_rl()
        self.__builder.build_text((xy[0] + 20 * self.scale, xy[1]),
                                  'rlD', st, self.fontsize())

    def __labels_perimeter_ul(self):
        xy, st = self.__aux.perimeter_label_ul()
        self.__builder.build_text((xy[0], xy[1] - 15 * self.scale),
                                  'ulD', st, self.fontsize())

    def __labels_perimeter_uld(self):
        xy, st = self.__aux.perimeter_label_uld()
        self.__builder.build_text((xy[0] - 35 * self.scale, xy[1] - 15 * self.scale),
                                  'ulsD', st, self.fontsize())