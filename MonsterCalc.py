#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from calc import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create editor
        self.editor = MainWidget()
        self.setCentralWidget(self.editor)

        # Create main view and icon
        self.setWindowTitle("MONSTER CALC")
        self.setGeometry(600, 300, 700, 500)
        self.setWindowTitle('MONSTER CALC')
        if ('win32' in sys.platform):
            path = os.path.abspath(os.path.dirname(sys.argv[0]))
            self.setWindowIcon(QIcon(path + '\Monster.png'))
            rawMonsterIco = QPixmap(path + '\Monster.png')
        else:
            self.setWindowIcon(
                QIcon('/Users/Andrew/Documents/Python/MonsterCalc/Monster.png'))
            rawMonsterIco = QPixmap(
                '/Users/Andrew/Documents/Python/MonsterCalc/Monster.png')
        self.monsterIco = rawMonsterIco.scaledToWidth(
            50, Qt.SmoothTransformation)
        self.saveName = ''

        # Create Menu
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.setStyleSheet("""

                        QMainWindow {
                            background-color: rgb(49,49,49);
                        }

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
                            color: white;
                            border: 1px solid #000;
                        }

                        QMenu::item::selected {
                            background-color: rgb(30,30,30);
                        }
                    """)

        # Create menu categories
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        settingsMenu = menubar.addMenu('&Settings')
        helpMenu = menubar.addMenu('&Help')

        # File menu
        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.openDialog)
        fileMenu.addAction(openAction)

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.checkSave)
        fileMenu.addAction(saveAction)

        saveAsAction = QAction('Save As..', self)
        saveAsAction.triggered.connect(self.saveDialog)
        fileMenu.addAction(saveAsAction)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Edit menu
        copyAction = QAction('Copy', self)
        copyAction.setShortcut('Ctrl+C')
        copyAction.triggered.connect(self.editor.textEdit.copy)
        editMenu.addAction(copyAction)

        cutAction = QAction('Cut', self)
        cutAction.setShortcut('Ctrl+X')
        cutAction.triggered.connect(self.editor.textEdit.cut)
        editMenu.addAction(cutAction)

        pasteAction = QAction('Paste', self)
        pasteAction.setShortcut('Ctrl+V')
        pasteAction.triggered.connect(self.editor.textEdit.paste)
        editMenu.addAction(pasteAction)

        clearAction = QAction('Clear all', self)
        clearAction.setShortcut('Ctrl+Shift+C')
        clearAction.triggered.connect(self.clearAll)
        editMenu.addAction(clearAction)

        # Settings menu
        sigFigAction = QAction('Significant Figures..', self)
        sigFigAction.triggered.connect(self.setSigFigs)
        settingsMenu.addAction(sigFigAction)

        resFormatMenu = settingsMenu.addMenu('Results Format')
        self.sciFormatAction = QAction('Scientific (1.0e4)', self)
        self.engFormatAction = QAction('Engineering (10.0e3)', self)
        self.siFormatAction = QAction('SI Unit (10.0k)', self)
        self.sciFormatAction.triggered.connect(self.setResFormatSci)
        self.sciFormatAction.setCheckable(True)
        self.engFormatAction.triggered.connect(self.setResFormatEng)
        self.engFormatAction.setCheckable(True)
        self.engFormatAction.setChecked(True)
        self.siFormatAction.triggered.connect(self.setResFormatSi)
        self.siFormatAction.setCheckable(True)
        resFormatMenu.addAction(self.sciFormatAction)
        resFormatMenu.addAction(self.engFormatAction)
        resFormatMenu.addAction(self.siFormatAction)

        # Help menu
        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.about)
        helpMenu.addAction(aboutAction)

    def openDialog(self):
        try:
            fname = QFileDialog.getOpenFileName(
                self, 'Open file', '/home', 'Text files (*.txt)')
            f = open(fname[0], 'r')
            with f:
                self.editor.textEdit.setPlainText(f.read())
            self.saveName = fname[0]
        except:
            pass
        return

    def saveDialog(self):
        try:
            fname = QFileDialog.getSaveFileName(
                self, 'Save file', '/home', 'Text files (*.txt)')
            f = open(fname[0], 'w')
            with f:
                f.write(self.editor.textEdit.toPlainText())
            self.saveName = fname[0]
        except:
            pass
        return

    def checkSave(self):
        if (self.saveName == ''):
            self.saveDialog()
        else:
            try:
                f = open(self.saveName, 'w')
                with f:
                    f.write(self.editor.textEdit.toPlainText())
            except:
                pass
        return

    def clearAll(self):
        self.editor.clear()
        return

    def setSigFigs(self):
        text, ok = QInputDialog.getText(self, 'Significant Figures',
                                        'Set # of significant figures' +
                                        'to display:')
        if ok:
            self.editor.setSigFigs(int(text))
        return

    def setResFormatSci(self):
        self.editor.resFormat = 'scientific'
        self.sciFormatAction.setChecked(True)
        self.engFormatAction.setChecked(False)
        self.siFormatAction.setChecked(False)
        return

    def setResFormatEng(self):
        self.editor.resFormat = 'engineering'
        self.sciFormatAction.setChecked(False)
        self.engFormatAction.setChecked(True)
        self.siFormatAction.setChecked(False)
        return

    def setResFormatSi(self):
        self.editor.resFormat = 'si'
        self.sciFormatAction.setChecked(False)
        self.engFormatAction.setChecked(False)
        self.siFormatAction.setChecked(True)
        return

    def about(self):
        msgBox = QMessageBox()
        msgBox.setIconPixmap(self.monsterIco)
        msgBox.setText('Monster Calc v1.2\nCreated by Andrew Carroll\n\n' +
                       'Special thanks to Mom for the artwork!')
        msgBox.setWindowTitle('About')
        msgBox.exec()
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    if ('win32' in sys.platform):
        myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ex.show()
    ex.editor.textEdit.setFocus()
    sys.exit(app.exec_())
