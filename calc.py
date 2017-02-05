#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QTextEdit, QAction, QApplication,QPushButton,QGridLayout,QWidget,QLabel
from PyQt5.QtGui import QIcon


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.textEdit = QTextEdit()
        self.resDisp = QTextEdit(readOnly=True)

        self.textEdit.textChanged.connect(self.updateDisp)

        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.textEdit, 0, 0)
        grid.addWidget(self.resDisp, 0, 1)
        self.setGeometry(300, 300, 350, 250)
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