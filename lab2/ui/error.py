#!/usr/bin/env python
# -*- coding: utf-8 -*-

# External
from PyQt5.QtWidgets import  QMessageBox


def error_window(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(str(e))
    msg.setWindowTitle("Error")
    msg.exec_()
