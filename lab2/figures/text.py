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

    def __zero(self):
        self.__builder.build_text((self.offset_x(), self.offset_y()),
                                  '0', self.st_color_axis, self.fontsize())

    def __x(self):
        self.__builder.build_text((self.offset_x() + self.__d_width, self.offset_y()),
                                  'x', self.st_color_axis, self.fontsize())

    def __y(self):
        self.__builder.build_text((self.offset_x(), self.offset_y() - self.__d_height),
                                  'y', self.st_color_axis, self.fontsize())

