#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QTextEdit,QApplication,QGridLayout,QWidget
from PyQt5.QtGui import QIcon


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.textEdit = QTextEdit()
        self.resDisp = QTextEdit(readOnly=True)
        self.initUI()

    def initUI(self):
        # Style
        self.textEdit.setStyleSheet("background-color: #1f3960; color: white; font-size: 20px")
        self.resDisp.setStyleSheet("background-color: #8191aa; font-size: 20px")

        self.textEdit.textChanged.connect(self.updateDisp)
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.textEdit, 0, 0)
        grid.addWidget(self.resDisp, 0, 1)
        self.setGeometry(600, 600, 700, 500)
        self.setWindowTitle('Main window')
        self.show()

    def updateDisp(self):
        text = self.textEdit.toPlainText()
        self.resDisp.setPlainText(text)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())