#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np

# Internal
from lab1.figures.interface.ifigures import Figure

pi = np.pi


class Circle(Figure):
    scale = 1

    radius = 40

    def __init__(self, builder, center, d_width, d_height, scale=1):
        self.__builder = builder
        self.__center = center
        self.scale = scale

        self.__d_width = d_width
        self.__d_height = d_height

    def build(self):
        self.check()
        self.__centre_circle()

    def check(self):
        if self.radius <= 0:
            raise ValueError(f'Circle.radius <= 0: {self.radius}')

    def s_radius(self):
        return self.radius * self.scale

    def __centre_circle(self):
        self.__builder.build_circle(r=self.s_radius(),
                                    xy=self.__center)
