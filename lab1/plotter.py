#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np
from matplotlib import pyplot as plt

# Internal
from lab1.module.builder import Builder

from lab1.figures.circle import Circle
from lab1.figures.arc import Arc
from lab1.figures.square import Square
from lab1.figures.perimeter import Perimeter


class Plotter:
    builder = None

    circle = None
    arc = None
    square = None
    perimeter = None

    scale = 1

    surf_width = 800
    surf_height = 800

    d = 25

    d_width = int(surf_width / 2)
    d_height = int(surf_height / 2)

    bg_color = (255, 255, 255)  # White
    st_color = (0, 0, 0)  # Black
    st_width = 2

    center = (d_width, d_height)

    def __init__(self):
        pass

    def setup_builder(self):
        self.builder = Builder(self.surf_width, self.surf_height, self.bg_color, self.st_color, self.st_width)

    def setup_figures(self):
        self.circle = Circle(builder=self.builder, center=self.center,
                             d_width=self.d_width, d_height=self.d_height, scale=self.scale)
        self.arc = Arc(builder=self.builder, center=self.center,
                       d_width=self.d_width, d_height=self.d_height, scale=self.scale)
        self.square = Square(builder=self.builder, center=self.center,
                             d_width=self.d_width, d_height=self.d_height, scale=self.scale)
        self.perimeter = Perimeter(builder=self.builder, center=self.center,
                                   d_width=self.d_width, d_height=self.d_height,
                                   circle=self.circle, arc=self.arc, square=self.square, scale=self.scale)

    def build(self):
        self.__complex_check()
        figure = self.__build_figures()
        self.__show_figure(figure)

    def __build_figures(self):
        self.circle.build()
        self.arc.build()
        self.square.build()
        self.perimeter.build()

        return self.builder.get_image()

    def __complex_check(self):
        if self.arc.radius <= self.circle.radius:
            raise ValueError(f'Arc.radius <= Circle.radius: {self.arc.radius} <= {self.circle.radius}')

    def __show_figure(self, data):
        # Basic fig
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.grid()

        # X and Y axis tick
        plt.xticks(np.arange(-self.d_width, self.d_width, self.d), rotation=90)
        plt.yticks(np.arange(-self.d_height, self.d_height, self.d))

        # Image display and axis transformation from (0, width/height) to (-d_width/d_height, d_width/-d_height)
        ax.imshow(data, interpolation='nearest', extent=(-self.d_width, self.d_width, self.d_height, -self.d_height))
        fig.show()


if __name__ == '__main__':
    fig = Plotter()
    fig.setup_builder()
    fig.setup_figures()
    fig.build()
