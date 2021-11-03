#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import sys
import traceback

# External
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)

# Internal
from ui.main_ui import Ui_MainWindow
import plotter


def handle_value_error(f):
    try:
        f()
    except ValueError as e:
        error_window(e)


def error_window(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(str(e))
    msg.setWindowTitle("Error")
    msg.exec_()


class Window(QMainWindow, Ui_MainWindow):
    plotter = None
    image = None

    def __init__(self, parent=None):
        self.plotter = plotter.Plotter()

        super().__init__(parent)
        self.setupUi(self)

        # Interface func init
        self.connect()

        self.build_figure()

    def build_figure(self):
        handle_value_error(self.plotter.build)
        self.update_image()

    def update_image(self):
        self.label.setPixmap(QtGui.QPixmap("source.png"))

    # -----------------------------------------------------------------
    def connect(self):
        self.build.clicked.connect(self.build_figure)
        self.default_2.clicked.connect(self.set_to_default)
        self.transform.clicked.connect(self.transform_handler)

        self.labels.stateChanged.connect(self.labels_checkbox)

        self.cicle_r.valueChanged.connect(self.apply_cicle_r)
        self.arc_r.valueChanged.connect(self.apply_arc_r)
        self.arc_dx.valueChanged.connect(self.apply_arc_dx)
        self.arc_angle_s.valueChanged.connect(self.apply_arc_as)
        self.arc_angle_e.valueChanged.connect(self.apply_arc_ae)
        self.s_ox.valueChanged.connect(self.apply_square_s_ox)
        self.s_oy.valueChanged.connect(self.apply_square_s_oy)
        self.s_side.valueChanged.connect(self.apply_square_s_side)
        self.ua_d.valueChanged.connect(self.apply_perimeter_ua_d)
        self.ll_d.valueChanged.connect(self.apply_perimeter_ll_d)
        self.rl_d.valueChanged.connect(self.apply_perimeter_rl_d)
        self.ul_d.valueChanged.connect(self.apply_perimeter_ul_d)
        self.ul_s_d.valueChanged.connect(self.apply_perimeter_ul_s_d)
        self.scale_value.valueChanged.connect(self.apply_scale)

    def apply_cicle_r(self):
        self.plotter.circle.radius = self.cicle_r.value()

    def apply_arc_r(self):
        self.plotter.arc.radius = self.arc_r.value()

    def apply_arc_dx(self):
        self.plotter.arc.delta_radius = self.arc_dx.value()

    def apply_arc_as(self):
        self.plotter.arc.angle_start = self.arc_angle_s.value()

    def apply_arc_ae(self):
        self.plotter.arc.angle_end = self.arc_angle_e.value()

    def apply_square_s_ox(self):
        self.plotter.square.x_offset = self.s_ox.value()

    def apply_square_s_oy(self):
        self.plotter.square.y_offset = self.s_oy.value()

    def apply_square_s_side(self):
        self.plotter.square.side = self.s_side.value()

    def apply_perimeter_ua_d(self):
        self.plotter.perimeter.UpperArc.delta_radius = self.ua_d.value()

    def apply_perimeter_ll_d(self):
        self.plotter.perimeter.LowerLine.delta = self.ll_d.value()

    def apply_perimeter_rl_d(self):
        self.plotter.perimeter.RightLine.delta = self.rl_d.value()

    def apply_perimeter_ul_d(self):
        self.plotter.perimeter.UpperLine.delta = self.ul_d.value()

    def apply_perimeter_ul_s_d(self):
        self.plotter.perimeter.UpperLine.square_delta = self.ul_s_d.value()

    def apply_scale(self):
        self.plotter.scale = self.scale_value.value()
        self.plotter.change_scale()

    # -----------------------------------------------------------------

    def labels_checkbox(self):
        if self.labels.isChecked():
            self.plotter.if_auxiliary = True
        else:
            self.plotter.if_auxiliary = False

    def set_to_default(self):
        self.plotter.set_default()

        self.cicle_r.setValue(self.plotter.circle.radius)

        self.arc_r.setValue(self.plotter.arc.radius)
        self.arc_dx.setValue(self.plotter.arc.delta_radius)
        self.arc_angle_s.setValue(self.plotter.arc.angle_start)
        self.arc_angle_e.setValue(self.plotter.arc.angle_end)

        self.s_ox.setValue(self.plotter.square.x_offset)
        self.s_oy.setValue(self.plotter.square.y_offset)
        self.s_side.setValue(self.plotter.square.side)

        self.plotter.perimeter.default()
        self.ua_d.setValue(self.plotter.perimeter.UpperArc.delta_radius)
        self.ll_d.setValue(self.plotter.perimeter.LowerLine.delta)
        self.rl_d.setValue(self.plotter.perimeter.RightLine.delta)
        self.ul_d.setValue(self.plotter.perimeter.UpperLine.delta)
        self.ul_s_d.setValue(self.plotter.perimeter.UpperLine.square_delta)

        self.scale_value.setValue(1)

    def transform_handler(self):
        try:
            index = self.tabWidget.currentIndex()

            if index == 0:
                self.transform_base()
            elif index == 1:
                self.transform_affine()
            elif index == 2:
                self.transform_projective()
        except ZeroDivisionError as e:
            error_window(e)

    def transform_base(self):
        try:
            self.plotter.build_pre()
            self.plotter.builder.prepare_image()

            self.plotter.builder.shift_rotate(ox=self.shift_x.value(), oy=-self.shift_y.value(),
                                              cx=self.rot_x.value() + self.plotter.d_width,
                                              cy=self.rot_y.value() + self.plotter.d_height, a=self.rot_angle.value())

            self.plotter.builder.get_image()
            self.update_image()
        except ValueError as e:
            error_window(e)

    def transform_affine(self):
        try:
            self.plotter.build_pre()
            self.plotter.builder.affine(xx=self.rX_x.value(), xy=self.rX_y.value(), wx=self.r0_x.value(),
                                        yx=self.rY_x.value(), yy=self.rY_y.value(), wy=self.r0_y.value())
            self.plotter.build_after()
            self.update_image()
        except ValueError as e:
            error_window(e)

    def transform_projective(self):
        try:
            self.plotter.build_pre()
            self.plotter.builder.projective(x0=self.pr0_x.value(), y0=self.pr0_y.value(), w0=self.pr0_w.value(),
                                            xx=self.prX_x.value(), xy=self.prX_y.value(), wx=self.prX_w.value(),
                                            yx=self.prY_x.value(), yy=self.prY_y.value(), wy=self.prY_w.value())
            self.plotter.build_after()
            self.update_image()
        except ValueError as e:
            error_window(e)


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
