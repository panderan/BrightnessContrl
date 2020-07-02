import logging
import os
import sys
import time
from ctypes import Structure, byref, windll, wintypes
from enum import Enum
from multiprocessing import Process

from PyQt5.QtCore import QObject, QPoint, Qt
from PyQt5.QtGui import (QColor, QCursor, QIcon, QPainter, QPainterPath,
                         QPalette, QPixmap)
from PyQt5.QtWidgets import (QAction, QGraphicsDropShadowEffect, QMenu,
                             QMessageBox, QSystemTrayIcon, QWidget)

import gui.uic.mainwindow as ui
import res_rc
from bclib.bc import get_physical_monitor_handles


version = 1.2


class ResizeDirtection(Enum):
    ''' 窗口缩放方向
    '''
    TopLeft = 1
    Top = 2
    TopRight = 3
    Right = 4
    BottomRight = 5
    Bottom = 6
    BottomLeft = 7
    Left = 8


class AppMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_MainWidget()
        self.ui.setupUi(self)
        self.monitors = []

        self.__enable = True

        self._start_pos = None
        self._end_pos = None
        self._is_drag = False
        self._press = False
        self._is_resize = False
        self._resize_direction = None
        self._margin = 10
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui.label_wintitle.setText("Brightness Ctrl v%.1f"%version)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)
        shadow.setColor(Qt.black)
        shadow.setBlurRadius(8)
        self.setGraphicsEffect(shadow)

        self.tray_icon = None
        self.tray_icon_menu = None
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon_menu = QMenu(self)
            restore_action = QAction("恢复主窗口", self)
            restore_action.triggered.connect(self.action_restore)
            self.tray_icon_menu.addAction(restore_action)
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setContextMenu(self.tray_icon_menu)
            self.tray_icon.setIcon(QIcon(':/images/icon.ico'))
            self.tray_icon.show()
        self.ui.btn_exit.clicked.connect(self.slot_btn_exit)
        self.ui.tbtn_refresh.clicked.connect(self.slot_tbtn_refresh_clicked, Qt.DirectConnection)
        self.ui.btn_show_monitor_info.clicked.connect(self.slot_btn_show_monitor_info)
        self.ui.hsilder_brightness.valueChanged.connect(self.slot_hsilder_brightness_value_changed)
        self.ui.spinbox_brightness.valueChanged.connect(self.slot_spinbox_brightness_value_changed)
        self.ui.hsilder_contrast.valueChanged.connect(self.slot_hsilder_contrast_value_changed)
        self.ui.spinbox_contrast.valueChanged.connect(self.slot_spinbox_contrast_value_changed)
        self.tray_icon.activated.connect(self.slot_system_tray_activated)
        self.ui.btn_x.clicked.connect(self.close)
        self.ui.btn_x.setAttribute(Qt.WA_Hover, True)
        self.init_monitors()

    def init_monitors(self):
        err, self.monitors = get_physical_monitor_handles()
        if err:
            QMessageBox(QMessageBox.Critical, "错误", \
                self.monitors + "\nPlease restart the app to refresh or continue using current devices handle.").exec()
            return

        self.ui.combobox_monitor.clear()
        for monitor in self.monitors:
            self.ui.combobox_monitor.addItem(monitor.description, monitor)

        monitor = self.ui.combobox_monitor.currentData()
        if monitor is not None:
            self.enable_all_settings(True)
            self.set_current_monitor_brightness(monitor.brightness)
            self.set_current_monitor_contrast(monitor.contrast)
        else:
            self.enable_all_settings(False)

    def enable_all_settings(self, flag: bool):
        if flag is not self.__enable:
            self.ui.hsilder_brightness.setEnabled(flag)
            self.ui.hsilder_contrast.setEnabled(flag)
            self.ui.spinbox_brightness.setEnabled(flag)
            self.ui.spinbox_contrast.setEnabled(flag)
            self.__enable = flag

    def slot_hsilder_brightness_value_changed(self):
        self.ui.spinbox_brightness.setValue(self.ui.hsilder_brightness.value())
        monitor = self.ui.combobox_monitor.currentData()
        if monitor is not None:
            monitor.brightness = self.ui.hsilder_brightness.value()
            if monitor.errcheck:
                QMessageBox(QMessageBox.Warning, "警告", \
                    monitor.get_errstring_and_cls + "\nPlease refresh monitors.").exec()
        else:
            self.enable_all_settings(False)
    
    def slot_spinbox_brightness_value_changed(self):
        self.ui.hsilder_brightness.setValue(self.ui.spinbox_brightness.value())
        monitor = self.ui.combobox_monitor.currentData()
        if monitor is not None:
            monitor.brightness = self.ui.spinbox_brightness.value()
            if monitor.errcheck:
                QMessageBox(QMessageBox.Warning, "警告", \
                    monitor.get_errstring_and_cls + "\nPlease refresh monitors.").exec()
        else:
            self.enable_all_settings(False)

    def slot_hsilder_contrast_value_changed(self):
        self.ui.spinbox_contrast.setValue(self.ui.hsilder_contrast.value())
        monitor = self.ui.combobox_monitor.currentData()
        if monitor is not None:
            monitor.contrast = self.ui.hsilder_contrast.value()
            if monitor.errcheck:
                QMessageBox(QMessageBox.Warning, "警告", \
                    monitor.get_errstring_and_cls + "\nPlease refresh monitors.").exec()
        else:
            self.enable_all_settings(False)
    
    def slot_spinbox_contrast_value_changed(self):
        self.ui.hsilder_contrast.setValue(self.ui.spinbox_contrast.value())
        monitor = self.ui.combobox_monitor.currentData()
        if monitor is not None:
            monitor.contrast = self.ui.spinbox_contrast.value()
            if monitor.errcheck:
                QMessageBox(QMessageBox.Warning, "警告", \
                    monitor.get_errstring_and_cls + "\nPlease refresh monitors.").exec()
        else:
            self.enable_all_settings(False)
    
    def slot_tbtn_refresh_clicked(self):
        from brightctrl_app import app, app_real_path
        if app_real_path[len(app_real_path)-7: len(app_real_path)].lower() != 'app.exe':
            QMessageBox(QMessageBox.Critical, "错误", \
                "App path is incorrect(%s)\n\nPlease restart the app manually."%app_real_path).exec()
            return
        self.close()
        self.tray_icon.hide()
        logging.info("Restart APP: %s"%app_real_path)
        os.startfile(app_real_path)
        app.quit()
        logging.info("Old app quit.")

    def set_current_monitor_brightness(self, brightness_values):
        self.ui.hsilder_brightness.setMinimum(brightness_values[0])
        self.ui.hsilder_brightness.setMaximum(brightness_values[-1])
        self.ui.hsilder_brightness.setValue(brightness_values[1])
        self.ui.spinbox_brightness.setMinimum(brightness_values[0])
        self.ui.spinbox_brightness.setMaximum(brightness_values[-1])
        self.ui.spinbox_brightness.setValue(brightness_values[1])

    def set_current_monitor_contrast(self, contrast_values):
        self.ui.hsilder_contrast.setMinimum(contrast_values[0])
        self.ui.hsilder_contrast.setMaximum(contrast_values[-1])
        self.ui.hsilder_contrast.setValue(contrast_values[1])
        self.ui.spinbox_contrast.setMinimum(contrast_values[0])
        self.ui.spinbox_contrast.setMaximum(contrast_values[-1])
        self.ui.spinbox_contrast.setValue(contrast_values[1])

    def action_restore(self):
        self.show()
        pass

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def slot_btn_exit(self):
        self.tray_icon.hide()
        import brightctrl_app
        brightctrl_app.app.quit()

    def slot_btn_show_monitor_info(self):
        monitor = self.ui.combobox_monitor.currentData()
        if monitor is not None:
            dialog = QMessageBox(QMessageBox.Information, "Detail", monitor.show_info())
            dialog.exec_()
        else:
            self.enable_all_settings(False)

    def slot_system_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.action_restore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.isResize(event):
                self._is_resize = True
                self._press = True
            else:
                self._is_drag = True
                self._start_pos = QPoint(event.x(), event.y())

    def mouseMoveEvent(self, event):
        if self._is_resize:
            self._resizeWidget(event)
        if self._is_drag:
            self._end_pos = event.pos() - self._start_pos
            self.move(self.pos() + self._end_pos)
        if not self._is_resize:
            self.isResize(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_drag = False
            self._press = False
            self._is_resize = False
            self._resize_direction = None
            self._start_pos = None
            self._end_pos = None
            self.setCursor(QCursor(Qt.ArrowCursor))   

    def isResize(self, event):
        x_pos, y_pos = event.pos().x(), event.pos().y()
        w, h = self.geometry().width(), self.geometry().height()
        if x_pos < self._margin and y_pos < self._margin:
            self._resize_direction = ResizeDirtection.TopLeft
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif w - x_pos < self._margin and y_pos < self._margin:
            self._resize_direction = ResizeDirtection.TopRight
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif w - x_pos < self._margin and h - y_pos < self._margin:
            self._resize_direction = ResizeDirtection.BottomRight
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif x_pos < self._margin and h - y_pos < self._margin:
            self._resize_direction = ResizeDirtection.BottomLeft
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif x_pos < self._margin:
            self._resize_direction = ResizeDirtection.Left
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif w - x_pos < self._margin:
            self._resize_direction = ResizeDirtection.Right
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif y_pos < self._margin:
            self._resize_direction = ResizeDirtection.Top
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif h - y_pos < self._margin:
            self._resize_direction = ResizeDirtection.Bottom
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            self._resize_direction = None
            self.setCursor(QCursor(Qt.ArrowCursor))   

        if self._resize_direction is not None:
            return True
        return False            

    def _resizeWidget(self, event):
        if not self._is_resize:
            return False

        x_pos, y_pos = event.pos().x(), event.pos().y()
        x, y, w, h = self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()
        if self._resize_direction is ResizeDirtection.TopLeft:
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
            x += x_pos
            w -= x_pos
            y += y_pos
            h -= y_pos
        if self._resize_direction is ResizeDirtection.TopRight:
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
            w = x_pos
            y += y_pos
            h -= y_pos
        if self._resize_direction is ResizeDirtection.BottomRight:
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
            w = x_pos
            h = y_pos
        if self._resize_direction is ResizeDirtection.BottomLeft:
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
            x += x_pos
            w -= x_pos
            h = y_pos
        if self._resize_direction is ResizeDirtection.Left:
            self.setCursor(QCursor(Qt.SizeHorCursor))
            x += x_pos
            w -= x_pos
        if self._resize_direction is ResizeDirtection.Right:
            self.setCursor(QCursor(Qt.SizeHorCursor))
            w = x_pos
        if self._resize_direction is ResizeDirtection.Top:
            self.setCursor(QCursor(Qt.SizeVerCursor))
            y += y_pos
            h -= y_pos
        if self._resize_direction is ResizeDirtection.Bottom:
            self.setCursor(QCursor(Qt.SizeVerCursor))
            h = y_pos
        self.setGeometry(x, y, w, h)
        return True

    def paintEvent(self, e):
        palette = QPalette(self.palette())
        palette.setColor(QPalette.Background, QColor(255,255,255))
        self.setPalette(palette)

        painter = QPainter(self)
        shadow_width = 8
        painter.fillRect(shadow_width+1, \
                         shadow_width+1, \
                         self.width()-(shadow_width+1)*2, \
                         self.height()-(shadow_width+1)*2, \
                         QColor(255,255,255))
        painter.fillRect(shadow_width+1, \
                         shadow_width+1, \
                         self.width()-(shadow_width+1)*2 - 30, \
                         24, \
                         QColor(0,122,204))
