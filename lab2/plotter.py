#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base

# External
import numpy as np
from matplotlib import pyplot as plt

# Internal
from lab2.module.builder import Builder

from lab2.figures.curve import Curve
from lab2.figures.grid import Grid

from lab2.figures.text import Text


class Plotter:
    builder = None

    curve = None

    auxiliary = None
    grid = None

    text = None

    if_auxiliary = False

    framerate = 60

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

        self.curve.build()

        self.text.build()

    def build(self):
        self.__build_figures()

        self.builder.prepare_image()
        self.builder.get_image()

    def build_pre(self):
        self.__build_figures()

    def build_after(self):
        self.builder.prepare_image()
        self.builder.get_image()

    def build_local(self):
        self.__build_figures()

        self.builder.prepare_image()
        figure = self.builder.get_image_local()
        self.__show_figure(figure)

    def set_default(self):
        self.grid = Grid(builder=self.builder,
                         d=self.d, surf_width=self.surf_width, surf_height=self.surf_height)

        self.curve = Curve(builder=self.builder, center=self.center,
                           d_width=self.d_width, d_height=self.d_height)

        self.text = Text(builder=self.builder, center=self.center,
                         d_width=self.d_width, d_height=self.d_height,
                         scale=1,
                         aux=self.auxiliary)

    def __show_figure(self, data):
        fig, ax = plt.subplots(figsize=(8, 8))

        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

        # Image display and axis transformation from (0, width/height) to (-d_width/d_height, d_width/-d_height)
        ax.imshow(data, interpolation='nearest', extent=(-self.d_width, self.d_width, self.d_height, -self.d_height))
        fig.show()


if __name__ == '__main__':
    fig = Plotter()

    fig.build_pre()
    fig.builder.prepare_image()

    fig.builder.shift_rotate(ox=10, oy=10,
                             cx=20, cy=20, a=2)

    fig.builder.get_image()
    fig.build_local()

    fig.build_local()

