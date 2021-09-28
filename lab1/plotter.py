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

from lab1.figures.auxiliary import Auxiliary
from lab1.figures.grid import Grid

from lab1.figures.text import Text


class Plotter:
    builder = None

    circle = None
    arc = None
    square = None
    perimeter = None

    auxiliary = None
    grid = None

    text = None

    if_auxiliary = False

    scale = 1

    surf_width = 700
    surf_height = 700

    d = 25

    d_width = int(surf_width / 2)
    d_height = int(surf_height / 2)

    bg_color = (1, 1, 1)  # White
    st_color = (0, 0, 0)  # Black
    st_width = 4

    center = (d_width, d_height)

    def __init__(self):
        self.builder = Builder(self.surf_width, self.surf_height, self.bg_color, self.st_color, self.st_width)

        self.set_default()

    def __build_figures(self):
        self.grid.build()

        self.circle.build()
        self.arc.build()
        self.square.build()
        self.perimeter.build()

        if self.if_auxiliary:
            self.auxiliary.build()
            self.text.build_aux()

        self.text.build()

    def build(self):
        self.__complex_check()
        self.__build_figures()

        self.builder.prepare_image()
        self.builder.get_image()

    def build_pre(self):
        self.__complex_check()
        self.__build_figures()

    def build_after(self):
        self.builder.prepare_image()
        self.builder.get_image()

    def build_local(self):
        self.__complex_check()
        self.__build_figures()

        self.builder.prepare_image()
        figure = self.builder.get_image_local()
        self.__show_figure(figure)

    def change_scale(self):
        self.circle.scale = self.scale
        self.arc.scale = self.scale
        self.square.scale = self.scale
        self.perimeter.scale = self.scale

        self.text.scale = self.scale

    def set_default(self):

        self.grid = Grid(builder=self.builder,
                         d=self.d, surf_width=self.surf_width, surf_height=self.surf_height)
        self.circle = Circle(builder=self.builder, center=self.center,
                             d_width=self.d_width, d_height=self.d_height, scale=self.scale)
        self.arc = Arc(builder=self.builder, center=self.center,
                       d_width=self.d_width, d_height=self.d_height, scale=self.scale)
        self.square = Square(builder=self.builder, center=self.center,
                             d_width=self.d_width, d_height=self.d_height, scale=self.scale)
        self.perimeter = Perimeter(builder=self.builder, center=self.center,
                                   d_width=self.d_width, d_height=self.d_height,
                                   circle=self.circle, arc=self.arc, square=self.square, scale=self.scale)

        self.auxiliary = Auxiliary(builder=self.builder, center=self.center,
                                   d_width=self.d_width, d_height=self.d_height,
                                   circle=self.circle, arc=self.arc, square=self.square, scale=self.scale,
                                   perimeter=self.perimeter)

        self.text = Text(builder=self.builder, center=self.center,
                         d_width=self.d_width, d_height=self.d_height,
                         scale=self.scale,
                         aux=self.auxiliary)

    def __complex_check(self):
        if self.arc.radius <= self.circle.radius:
            raise ValueError(f'Arc.radius <= Circle.radius: {self.arc.radius} <= {self.circle.radius}')
        if self.square.x_offset <= self.circle.radius:
            raise ValueError(f'Circle.x_offset <= Circle.radius: {self.square.x_offset} <= {self.circle.radius}')
        if self.square.y_offset <= self.circle.radius:
            raise ValueError(f'Circle.y_offset <= Circle.radius: {self.square.y_offset} <= {self.circle.radius}')

    def __show_figure(self, data):
        # Basic fig
        fig, ax = plt.subplots(figsize=(8, 8))
        #  ax.grid()

        # X and Y axis tick
        #  plt.xticks(np.arange(-self.d_width, self.d_width, self.d), rotation=90)
        #  plt.yticks(np.arange(-self.d_height, self.d_height, self.d))
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

        # Image display and axis transformation from (0, width/height) to (-d_width/d_height, d_width/-d_height)
        ax.imshow(data, interpolation='nearest', extent=(-self.d_width, self.d_width, self.d_height, -self.d_height))
        fig.show()


if __name__ == '__main__':
    fig = Plotter()

    #  fig.builder.projective(x0=1, y0=1, w0=1000,
    #                         yx=90, yy=800, wy=1,
    #                         xx=800, xy=50, wx=1)

    #  fig.build_local()

    #  fig.builder.affine(yx=0, yy=1, wy=0,
    #                     xx=1, xy=1, wx=0)

    fig.build_pre()
    fig.builder.prepare_image()

    fig.builder.shift_rotate(ox=10, oy=10,
                             cx=20, cy=20, a=2)

    fig.builder.get_image()
    fig.build_local()

    fig.build_local()

