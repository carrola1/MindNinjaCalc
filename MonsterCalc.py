#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys,ctypes
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,QFileDialog,QInputDialog
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
        if ('win32' in sys.platform):
            self.setWindowIcon(QIcon('C:\GitHub\MonsterCalc\Monster.png'))
        else:
            self.setWindowIcon(QIcon('/Users/Andrew/Documents/Python/MonsterCalc/Monster.png'))

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

    def openDialog(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home','Text files (*.txt)')
            f = open(fname[0],'r')
            with f:
                self.editor.textEdit.setPlainText(f.read())
            self.saveName = fname[0]
        except:
            pass
        return

    def saveDialog(self):
        try:
            fname = QFileDialog.getSaveFileName(self,'Save file', '/home',"Text files (*.txt)")
            f = open(fname[0],'w')
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
                                        'Set # of significant figures to display:')
        if ok:
            self.editor.setSigFigs(int(text))
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

