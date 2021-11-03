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
from ui.main_ui import Ui_MainWindow
from ui.anim import ThreadAuto, ThreadTransform
from ui.error import error_window
import plotter


def handle_value_error(f):
    try:
        f()
    except ValueError as e:
        error_window(e)


class Window(QMainWindow, Ui_MainWindow):
    plotter = None
    image = None

    default_dict = {}

    def __init__(self, parent=None):
        self.plotter = plotter.Plotter()

        super().__init__(parent)
        self.setupUi(self)

        self.collect_default()

        # Interface func init
        self.connect()
        self.build_figure()

        self.threadpool = QThreadPool()

    def build_figure(self):
        handle_value_error(self.plotter.build)
        self.update_image()

    def update_image(self):
        image = self.plotter.builder.get_image_bytes()

        qp = QtGui.QPixmap()
        qp.loadFromData(image)

        self.plot.setPixmap(qp)

    # -----------------------------------------------------------------
    def connect(self):
        # Meta
        self.default_2.clicked.connect(self.default_handler)

        # Base curve
        self.sigma.valueChanged.connect(self.apply_sigma)
        self.mu.valueChanged.connect(self.apply_mu)

        self.build.clicked.connect(self.build_handler)

        # Auto curve
        self.build_auto.clicked.connect(self.build_auto_handler)

        # Lines
        self.tangent.clicked.connect(self.build_tangent)
        self.normal.clicked.connect(self.build_normal)

        # Transform
        self.transform.clicked.connect(self.transform_handler)

    # -----------------------------------------------------------------
    # Meta

    def default_handler(self):
        self.set_default()

    def button_lock(self):
        self.build.setEnabled(False)
        self.build_auto.setEnabled(False)

        self.tangent.setEnabled(False)
        self.normal.setEnabled(False)

        self.transform.setEnabled(False)

    def button_unlock(self):
        self.build.setEnabled(True)
        self.build_auto.setEnabled(True)

        self.tangent.setEnabled(True)
        self.normal.setEnabled(True)

        self.transform.setEnabled(True)

    # -----------------------------------------------------------------
    # Base curve

    def apply_sigma(self):
        self.plotter.curve.s = self.sigma.value()

    def apply_mu(self):
        self.plotter.curve.m = self.mu.value()

    def build_handler(self):
        self.build_figure()

    # -----------------------------------------------------------------
    # Auto curve

    def build_auto_handler(self):
        self.button_lock()
        thread = ThreadAuto(self.sigma_to.value(), self.sigma_from.value(),
                            self.mu_to.value(), self.mu_from.value(),
                            self.steps.value(),
                            self.plotter)

        thread.signal.return_signal.connect(self.update_worker_image)
        thread.signal.finish_signal.connect(self.button_unlock)
        self.threadpool.start(thread)

    def update_worker_image(self, image):
        qp = QtGui.QPixmap()
        qp.loadFromData(image)

        self.plot.setPixmap(qp)

    # -----------------------------------------------------------------
    # Lines

    def build_tangent(self):
        x = self.build_x.value() / 10
        self.plotter.curve.build_tangent(x)
        self.build_figure()

    def build_normal(self):
        x = self.build_x.value() / 10
        self.plotter.curve.build_normal(x)
        self.build_figure()

    # -----------------------------------------------------------------
    # Transform

    def transform_handler(self):
        self.button_lock()

        self.ch_label_x.setText(f' {int(self.ch_label_x.text()) + self.shift_x.value()}')
        self.ch_label_y.setText(f' {int(self.ch_label_y.text()) + self.shift_y.value()}')
        self.ch_label_pi.setText(f' {float(self.ch_label_pi.text()) + self.rot_angle.value()}')

        thread = ThreadTransform(self.shift_x.value(), self.shift_y.value(),
                                 self.rot_x.value(), self.rot_y.value(),
                                 self.rot_angle.value(),
                                 self.plotter)

        thread.signal.return_signal.connect(self.update_worker_image)
        thread.signal.finish_signal.connect(self.button_unlock)
        self.threadpool.start(thread)

    # -----------------------------------------------------------------

    def collect_default(self):
        self.default_dict['sigma'] = self.sigma.value()
        self.default_dict['mu'] = self.mu.value()

        self.default_dict['sigma_from'] = self.sigma_from.value()
        self.default_dict['sigma_to'] = self.sigma_to.value()
        self.default_dict['mu_from'] = self.mu_from.value()
        self.default_dict['mu_to'] = self.mu_to.value()

        self.default_dict['steps'] = self.steps.value()

        self.default_dict['shift_x'] = self.shift_x.value()
        self.default_dict['shift_y'] = self.shift_y.value()

        self.default_dict['rot_x'] = self.rot_x.value()
        self.default_dict['rot_y'] = self.rot_y.value()

        self.default_dict['rot_angle'] = self.rot_angle.value()

    def set_default(self):
        self.sigma.setValue(self.default_dict['sigma'])
        self.mu.setValue(self.default_dict['mu'])

        self.sigma_from.setValue(self.default_dict['sigma_from'])
        self.sigma_to.setValue(self.default_dict['sigma_to'])
        self.mu_from.setValue(self.default_dict['mu_from'])
        self.mu_to.setValue(self.default_dict['mu_to'])

        self.steps.setValue(self.default_dict['steps'])

        self.shift_x.setValue(self.default_dict['shift_x'])
        self.shift_y.setValue(self.default_dict['shift_y'])

        self.rot_x.setValue(self.default_dict['rot_x'])
        self.rot_y.setValue(self.default_dict['rot_y'])

        self.rot_angle.setValue(self.default_dict['rot_angle'])

        self.ch_label_x.setText(f' 0')
        self.ch_label_y.setText(f' 0')
        self.ch_label_pi.setText(f' 0.0')


def except_hook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Error message:\n", tb)
    QApplication.quit()


if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
