# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(909, 836)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frequencySlider = QtWidgets.QSlider(self.centralwidget)
        self.frequencySlider.setEnabled(False)
        self.frequencySlider.setGeometry(QtCore.QRect(480, 40, 160, 22))
        self.frequencySlider.setMaximum(1000)
        self.frequencySlider.setOrientation(QtCore.Qt.Horizontal)
        self.frequencySlider.setObjectName("frequencySlider")
        self.maxFrequencylineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.maxFrequencylineEdit.setEnabled(True)
        self.maxFrequencylineEdit.setGeometry(QtCore.QRect(660, 40, 71, 20))
        self.maxFrequencylineEdit.setObjectName("maxFrequencylineEdit")
        self.minFrequencyLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.minFrequencyLineEdit.setEnabled(True)
        self.minFrequencyLineEdit.setGeometry(QtCore.QRect(390, 40, 81, 21))
        self.minFrequencyLineEdit.setObjectName("minFrequencyLineEdit")
        self.frequencyLabel = QtWidgets.QLabel(self.centralwidget)
        self.frequencyLabel.setGeometry(QtCore.QRect(520, 10, 101, 21))
        self.frequencyLabel.setTextFormat(QtCore.Qt.AutoText)
        self.frequencyLabel.setScaledContents(False)
        self.frequencyLabel.setObjectName("frequencyLabel")
        self.checkBox_sweep = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_sweep.setEnabled(False)
        self.checkBox_sweep.setGeometry(QtCore.QRect(300, 20, 70, 17))
        self.checkBox_sweep.setObjectName("checkBox_sweep")
        self.MplWidget_phase = MplWidget(self.centralwidget)
        self.MplWidget_phase.setGeometry(QtCore.QRect(29, 140, 841, 641))
        self.MplWidget_phase.setMinimumSize(QtCore.QSize(480, 240))
        self.MplWidget_phase.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.MplWidget_phase.setObjectName("MplWidget_phase")
        self.comportComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comportComboBox.setGeometry(QtCore.QRect(30, 60, 81, 22))
        self.comportComboBox.setEditable(True)
        self.comportComboBox.setObjectName("comportComboBox")
        self.startStopButton = QtWidgets.QPushButton(self.centralwidget)
        self.startStopButton.setGeometry(QtCore.QRect(30, 30, 81, 23))
        self.startStopButton.setObjectName("startStopButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 909, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.maxFrequencylineEdit.setText(_translate("MainWindow", "150000"))
        self.minFrequencyLineEdit.setText(_translate("MainWindow", "50000"))
        self.frequencyLabel.setText(_translate("MainWindow", "50000.0"))
        self.checkBox_sweep.setText(_translate("MainWindow", "sweep"))
        self.startStopButton.setText(_translate("MainWindow", "START"))
from mplwidget import MplWidget
