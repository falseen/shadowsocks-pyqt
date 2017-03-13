# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\github\shadowsocks-pyqt\logwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogWindow(object):
    def setupUi(self, LogWindow):
        LogWindow.setObjectName("LogWindow")
        LogWindow.resize(800, 431)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/Shadowsocks_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LogWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(LogWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LogBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.LogBrowser.setGeometry(QtCore.QRect(10, 10, 781, 411))
        self.LogBrowser.setObjectName("LogBrowser")
        LogWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LogWindow)
        QtCore.QMetaObject.connectSlotsByName(LogWindow)

    def retranslateUi(self, LogWindow):
        _translate = QtCore.QCoreApplication.translate
        LogWindow.setWindowTitle(_translate("LogWindow", "日志查看器"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LogWindow = QtWidgets.QMainWindow()
    ui = Ui_LogWindow()
    ui.setupUi(LogWindow)
    LogWindow.show()
    sys.exit(app.exec_())

