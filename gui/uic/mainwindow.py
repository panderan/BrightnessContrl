# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\uic\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.setWindowModality(QtCore.Qt.NonModal)
        MainWidget.resize(400, 200)
        MainWidget.setMinimumSize(QtCore.QSize(400, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWidget.setWindowIcon(icon)
        MainWidget.setWindowOpacity(1.0)
        MainWidget.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_title = QtWidgets.QVBoxLayout()
        self.layout_title.setContentsMargins(0, 0, -1, -1)
        self.layout_title.setObjectName("layout_title")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_wintitle = QtWidgets.QLabel(MainWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setBold(True)
        font.setWeight(75)
        self.label_wintitle.setFont(font)
        self.label_wintitle.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label_wintitle.setStyleSheet("color:rgb(255, 255, 255);")
        self.label_wintitle.setObjectName("label_wintitle")
        self.horizontalLayout.addWidget(self.label_wintitle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_x = QtWidgets.QPushButton(MainWidget)
        self.btn_x.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_x.setMouseTracking(True)
        self.btn_x.setStyleSheet("QPushButton#btn_x {\n"
"    border-image: url(:/images/btn_x.png);\n"
"}\n"
"\n"
"QPushButton#btn_x:hover {\n"
"    border-image: url(:/images/btn_x2.png);\n"
"}\n"
"")
        self.btn_x.setText("")
        self.btn_x.setObjectName("btn_x")
        self.horizontalLayout.addWidget(self.btn_x)
        self.layout_title.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.layout_title)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_holdplace_2 = QtWidgets.QLabel(MainWidget)
        self.label_holdplace_2.setText("")
        self.label_holdplace_2.setObjectName("label_holdplace_2")
        self.gridLayout.addWidget(self.label_holdplace_2, 2, 0, 1, 1)
        self.layout_conf_brightness = QtWidgets.QHBoxLayout()
        self.layout_conf_brightness.setObjectName("layout_conf_brightness")
        self.label_hsilder_brightness = QtWidgets.QLabel(MainWidget)
        self.label_hsilder_brightness.setMinimumSize(QtCore.QSize(60, 0))
        self.label_hsilder_brightness.setObjectName("label_hsilder_brightness")
        self.layout_conf_brightness.addWidget(self.label_hsilder_brightness)
        self.hsilder_brightness = QtWidgets.QSlider(MainWidget)
        self.hsilder_brightness.setOrientation(QtCore.Qt.Horizontal)
        self.hsilder_brightness.setObjectName("hsilder_brightness")
        self.layout_conf_brightness.addWidget(self.hsilder_brightness)
        self.spinbox_brightness = QtWidgets.QSpinBox(MainWidget)
        self.spinbox_brightness.setMinimumSize(QtCore.QSize(46, 0))
        self.spinbox_brightness.setObjectName("spinbox_brightness")
        self.layout_conf_brightness.addWidget(self.spinbox_brightness)
        self.gridLayout.addLayout(self.layout_conf_brightness, 2, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.combobox_monitor = QtWidgets.QComboBox(MainWidget)
        self.combobox_monitor.setObjectName("combobox_monitor")
        self.horizontalLayout_2.addWidget(self.combobox_monitor)
        self.tbtn_refresh = QtWidgets.QToolButton(MainWidget)
        self.tbtn_refresh.setMinimumSize(QtCore.QSize(22, 22))
        self.tbtn_refresh.setMaximumSize(QtCore.QSize(22, 22))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbtn_refresh.setIcon(icon1)
        self.tbtn_refresh.setObjectName("tbtn_refresh")
        self.horizontalLayout_2.addWidget(self.tbtn_refresh)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.label_holdplace_3 = QtWidgets.QLabel(MainWidget)
        self.label_holdplace_3.setText("")
        self.label_holdplace_3.setObjectName("label_holdplace_3")
        self.gridLayout.addWidget(self.label_holdplace_3, 3, 0, 1, 1)
        self.label_combobox_monitor = QtWidgets.QLabel(MainWidget)
        self.label_combobox_monitor.setMinimumSize(QtCore.QSize(80, 0))
        self.label_combobox_monitor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_combobox_monitor.setObjectName("label_combobox_monitor")
        self.gridLayout.addWidget(self.label_combobox_monitor, 0, 0, 1, 1)
        self.layout_conf_contrast = QtWidgets.QHBoxLayout()
        self.layout_conf_contrast.setObjectName("layout_conf_contrast")
        self.label_hsilder_contrast = QtWidgets.QLabel(MainWidget)
        self.label_hsilder_contrast.setMinimumSize(QtCore.QSize(60, 0))
        self.label_hsilder_contrast.setObjectName("label_hsilder_contrast")
        self.layout_conf_contrast.addWidget(self.label_hsilder_contrast)
        self.hsilder_contrast = QtWidgets.QSlider(MainWidget)
        self.hsilder_contrast.setOrientation(QtCore.Qt.Horizontal)
        self.hsilder_contrast.setObjectName("hsilder_contrast")
        self.layout_conf_contrast.addWidget(self.hsilder_contrast)
        self.spinbox_contrast = QtWidgets.QSpinBox(MainWidget)
        self.spinbox_contrast.setMinimumSize(QtCore.QSize(46, 0))
        self.spinbox_contrast.setObjectName("spinbox_contrast")
        self.layout_conf_contrast.addWidget(self.spinbox_contrast)
        self.gridLayout.addLayout(self.layout_conf_contrast, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(MainWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.layout_buttons = QtWidgets.QGridLayout()
        self.layout_buttons.setObjectName("layout_buttons")
        self.btn_show_monitor_info = QtWidgets.QPushButton(MainWidget)
        self.btn_show_monitor_info.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_show_monitor_info.setObjectName("btn_show_monitor_info")
        self.layout_buttons.addWidget(self.btn_show_monitor_info, 0, 0, 1, 1)
        self.btn_exit = QtWidgets.QPushButton(MainWidget)
        self.btn_exit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_exit.setObjectName("btn_exit")
        self.layout_buttons.addWidget(self.btn_exit, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.layout_buttons)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "Brightness Ctrl"))
        self.label_wintitle.setText(_translate("MainWidget", "Brightness Control"))
        self.label_hsilder_brightness.setText(_translate("MainWidget", "亮　度："))
        self.tbtn_refresh.setText(_translate("MainWidget", "..."))
        self.label_combobox_monitor.setText(_translate("MainWidget", "　显示器："))
        self.label_hsilder_contrast.setText(_translate("MainWidget", "对比度："))
        self.btn_show_monitor_info.setText(_translate("MainWidget", "显示器信息"))
        self.btn_exit.setText(_translate("MainWidget", "退出"))
import res_rc
