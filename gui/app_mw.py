import gui.uic.mainwindow as ui
from ctypes import wintypes, windll, byref, Structure
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget,  QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QCursor, QPalette, QPainter, QPainterPath, QColor, QPixmap
from bclib.bc import get_physical_monitor_handles
import res_rc
from enum import Enum

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
        self.ui.btn_show_monitor_info.clicked.connect(self.slot_btn_show_monitor_info)
        self.ui.hsilder_brightness.valueChanged.connect(self.slot_hsilder_brightness_value_changed)
        self.ui.spinbox_brightness.valueChanged.connect(self.slot_spinbox_brightness_value_changed)
        self.tray_icon.activated.connect(self.slot_system_tray_activated)
        self.ui.btn_x.clicked.connect(self.close)
        self.ui.btn_x.setAttribute(Qt.WA_Hover, True)
        self.init_monitors()

    def init_monitors(self):
        self.monitors = get_physical_monitor_handles()
        for monitor in self.monitors:
            self.ui.combobox_monitor.addItem(monitor.description, monitor)

        monitor = self.ui.combobox_monitor.currentData()
        self.set_current_monitor_brightness(monitor.brightness)

    def slot_hsilder_brightness_value_changed(self):
        self.ui.spinbox_brightness.setValue(self.ui.hsilder_brightness.value())
        monitor = self.ui.combobox_monitor.currentData()
        monitor.brightness = self.ui.hsilder_brightness.value()
    
    def slot_spinbox_brightness_value_changed(self):
        self.ui.hsilder_brightness.setValue(self.ui.spinbox_brightness.value())
        monitor = self.ui.combobox_monitor.currentData()
        monitor.brightness = self.ui.spinbox_brightness.value()

    def set_current_monitor_brightness(self, brightness_values):
        self.ui.hsilder_brightness.setMinimum(brightness_values[0])
        self.ui.hsilder_brightness.setMaximum(brightness_values[-1])
        self.ui.hsilder_brightness.setValue(brightness_values[1])
        self.ui.spinbox_brightness.setMinimum(brightness_values[0])
        self.ui.spinbox_brightness.setMaximum(brightness_values[-1])
        self.ui.spinbox_brightness.setValue(brightness_values[1])

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
        dialog = QMessageBox(QMessageBox.Information, "Detail", monitor.show_info())
        dialog.exec_()

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
        painter.drawPixmap(0, 0, 8, 8, QPixmap(':/images/border.png'), 0, 0, 8, 8)
        painter.drawPixmap(8, 0, self.width()-16, 8, QPixmap(':/images/border.png'), 8, 0, 1, 8)
        painter.drawPixmap(self.width()-8, 0, 8, 8, QPixmap(':/images/border.png'), 8, 0, 8, 8)
        painter.drawPixmap(self.width()-8, 8, 8, self.height()-16, QPixmap(':/images/border.png'), 8, 8, 8, 1)
        painter.drawPixmap(self.width()-8, self.height()-8, 8, 8, QPixmap(':/images/border.png'), 8, 8, 8, 8)
        painter.drawPixmap(8, self.height()-8, self.width()-16, 8, QPixmap(':/images/border.png'), 8, 8, 1, 8)
        painter.drawPixmap(0, self.height()-8, 8, 8, QPixmap(':/images/border.png'), 0, 8, 8, 8)
        painter.drawPixmap(0, 8, 8, self.height() - 16, QPixmap(':/images/border.png'), 0, 8, 8, 1)

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



        






