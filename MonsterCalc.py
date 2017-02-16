#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys,ctypes
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtGui import QIcon
from calc import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = MainWidget()
        self.setCentralWidget(self.editor)

        self.setWindowTitle("MONSTER CALC")
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('MONSTER CALC')
        self.setWindowIcon(QIcon('Monster.png'))

        # Create Menu
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.setStyleSheet("""
                QMenuBar {
                    background-color: rgb(49,49,49);
                    color: rgb(255,255,255);
                    border: 1px solid #000;
                }

                QMenuBar::item {
                    background-color: rgb(49,49,49);
                    color: rgb(255,255,255);
                }

                QMenuBar::item::selected {
                    background-color: rgb(30,30,30);
                }

                QMenu {
                    background-color: rgb(49,49,49);
                    color: rgb(255,255,255);
                    border: 1px solid #000;
                }

                QMenu::item::selected {
                    background-color: rgb(30,30,30);
                }
            """)
        fileMenu = menubar.addMenu('&File')
        funcMenu = menubar.addMenu('&Functions')

        self.setStyleSheet("background-color: rgb(49,49,49)")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    if ('win32' in sys.platform):
        myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ex.show()
    sys.exit(app.exec_())

