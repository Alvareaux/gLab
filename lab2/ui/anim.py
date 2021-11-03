#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import sys
import time
import traceback

# External
import numpy as np

from PyQt5.QtCore import QObject, QThread, QRunnable, pyqtSignal, pyqtSlot, QThreadPool
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)

# Internal
from lab2.ui.error import error_window


class Signals(QObject):
    return_signal = pyqtSignal(bytes)
    finish_signal = pyqtSignal()


class ThreadAuto(QRunnable):
    signal = pyqtSignal(bytes)

    def __init__(self, sigma_to, sigma_from, mu_to, mu_from, steps, plotter):
        super(ThreadAuto, self).__init__()

        self.sigma_to = sigma_to
        self.sigma_from = sigma_from

        self.mu_to = mu_to
        self.mu_from = mu_from

        self.steps = steps

        self.plotter = plotter

        self.signal = Signals()

    @pyqtSlot()
    def run(self):
        d_s = (self.sigma_to - self.sigma_from) / self.steps
        if d_s == 0:
            s_range = [self.sigma_to] * self.steps
            print(s_range)
        else:
            s_range = np.arange(self.sigma_from, self.sigma_to + d_s, d_s)

        d_m = (self.mu_to - self.mu_from) / self.steps
        if d_m == 0:
            m_range = [self.mu_to] * self.steps
        else:
            m_range = np.arange(self.mu_from, self.mu_to + d_m, d_m)

        for i in range(self.steps):
            print(s_range[i], m_range[i])
            self.plotter.curve.s = s_range[i]
            self.plotter.curve.m = m_range[i]

            self.plotter.build()
            image = self.plotter.builder.get_image_bytes()

            self.signal.return_signal.emit(image)

        self.signal.finish_signal.emit()


class ThreadTransform(QRunnable):
    signal = pyqtSignal(bytes)

    d_x = 0.5
    d_pi = 0.01

    def __init__(self, dx, dy, rot_x, rot_y, d_rot, plotter):
        super(ThreadTransform, self).__init__()

        self.dx = dx
        self.dy = dy

        self.rot_x = rot_x
        self.rot_y = rot_y

        self.d_rot = d_rot

        self.plotter = plotter

        self.signal = Signals()

    @pyqtSlot()
    def run(self):
        self.shift()
        self.rotate()

        self.signal.finish_signal.emit()

    def shift(self):
        try:
            if self.dx != 0:
                count = abs(int(self.dx / self.d_x))

                d_x = self.d_x * self.dx / abs(self.dx)
                d_y = self.dy / count
            else:
                count = abs(int(self.dy / self.d_x))

                d_x = 0
                d_y = self.d_x * self.dy / abs(self.dy)

            for i in range(count):
                image = self.shift_rotate(ox=d_x, oy=d_y,
                                          cx=0,
                                          cy=0, a=0)

                self.signal.return_signal.emit(image)

        except ValueError as e:
            error_window(e)
        except ZeroDivisionError as e:
            return

    def rotate(self):
        try:
            count = abs(int(self.d_rot / self.d_pi))
            d_pi = self.d_pi * self.d_rot / abs(self.d_rot)

            for i in range(count):
                image = self.shift_rotate(ox=0, oy=0,
                                          cx=self.rot_x,
                                          cy=self.rot_y, a=d_pi)

                self.signal.return_signal.emit(image)

        except ValueError as e:
            error_window(e)
        except ZeroDivisionError as e:
            return

    def shift_rotate(self, ox, oy, cx, cy, a):
        self.plotter.builder.shift_rotate(ox=ox, oy=-oy,
                                          cx=cx + self.plotter.d_width,
                                          cy=cy + self.plotter.d_height, a=a)

        image = self.plotter.builder.get_image_bytes()

        return image