#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from math import pi,log,log10,log2,ceil,floor,sqrt,sin,cos,tan,asin,acos,atan,degrees,radians
from PyQt5.QtWidgets import QTextEdit,QApplication,QGridLayout,QWidget,QLabel,QMainWindow,QAction,QFileDialog,qApp
from PyQt5.QtGui import QIcon,QColor,QTextCharFormat,QFont,QSyntaxHighlighter,QPalette
from PyQt5.QtCore import QRegExp,Qt
from myfuncs import mySum,bitget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = MainWidget()
        self.setCentralWidget(self.editor)

        self.setWindowTitle("Monster Calc")
        self.setGeometry(600, 300, 700, 500)

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

        self.setStyleSheet("background-color: #b8b9ba")
        self.show()

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Parameters
        self.maxLines = 100

        # Create Widgets
        self.textEdit = QTextEdit()
        self.resDisp = QTextEdit(readOnly=True)
        self.titleBar = QLabel()
        self.titleBar.setText('Monster Calc')

        # Syntax Highlighter
        self.highlight = KeywordHighlighter(self.textEdit.document())

        # Create Text Fields of length maxLines
        self.curText = ['']*self.maxLines
        self.resText = ['']*self.maxLines

        # Overload symbols
        self.symDict =  {   '0e': '0*10**', # allow use of 'e' for x10^X notation
                            '1e': '1*10**',
                            '2e': '2*10**',
                            '3e': '3*10**',
                            '4e': '4*10**',
                            '5e': '5*10**',
                            '6e': '6*10**',
                            '7e': '7*10**',
                            '8e': '8*10**',
                            '9e': '9*10**',
                            'sum': 'mySum'  # replace built-in sum() to take a list of args instead of a py list
                        }

        # Store symDict keys
        self.keyList = [('uu' + str(i)) for i in range(0,self.maxLines)]
        for ii in range(0,self.maxLines):
            self.symDict[self.keyList[ii]] = self.keyList[ii]

        self.initUI()

    def initUI(self):
        # Widget Styles
        self.textEdit.setStyleSheet("background-color: #1f3960; color: white; font-size: 20px")
        self.resDisp.setStyleSheet("background-color: #8191aa; font-size: 20px")
        self.titleBar.setStyleSheet("background-color: #b8b9ba; color: #1f3960; font-size: 30px;")
        self.titleBar.setAlignment(Qt.AlignCenter)

        # Do not allow text wrapping
        self.textEdit.setLineWrapMode(0)
        self.resDisp.setLineWrapMode(0)

        # Turn off display scrollbar and synchronize scrolling
        self.resDisp.setVerticalScrollBarPolicy(1)
        self.textEdit.verticalScrollBar().valueChanged.connect(self.resDisp.verticalScrollBar().setValue)
        self.resDisp.verticalScrollBar().valueChanged.connect(self.textEdit.verticalScrollBar().setValue)

        # Text Changed Callback
        self.textEdit.textChanged.connect(self.updateResults)

        # Layout
        grid = QGridLayout()
        self.setLayout(grid)
        self.titleBar.setFixedHeight(25)
        grid.addWidget(self.titleBar,0,0,1,2)
        grid.addWidget(self.textEdit, 1, 0)
        grid.addWidget(self.resDisp, 1, 1)

    def updateResults(self):
        # Get text and break into lines
        text = self.textEdit.toPlainText()
        self.highlight.highlightBlock(text)
        textLines = text.split("\n")

        # Find change
        for ii in range(0,len(textLines)):
            if (textLines[ii] != self.curText[ii]):
                self.curText[ii] = textLines[ii]
                self.evalLine(ii)
        # Clear unused lines
        self.resText[len(textLines):] = ['']*(len(self.resText)-len(textLines))

        # Update results
        newResults = "\n"
        newResults = newResults.join(self.resText[0:len(textLines)])
        self.resDisp.setPlainText(newResults)
        return

    def evalLine(self,lineNum):
        newLine = self.curText[lineNum]
        if ('=' in newLine):
            newLine = newLine.split('=')
            newVar = newLine[0].strip()
            self.evalExp(newLine[1],lineNum)
            self.symDict[newVar] = self.symDict.pop(self.keyList[lineNum])
            self.symDict[newVar] = self.resText[lineNum]
            self.keyList[lineNum] = newVar
            self.highlight.updateRules(self.keyList)
        else:
            self.evalExp(newLine, lineNum)
        return

    def evalExp(self,newExp,lineNum):
        try:
            for key in self.symDict:
                newExp = newExp.replace(key, self.symDict[key])
            newResult = str(eval(newExp))
            if ('function' not in newResult):
                self.resText[lineNum] = newResult
            else:
                self.resText[lineNum] = ''
        except:
            self.resText[lineNum] = ''
        return

class KeywordHighlighter (QSyntaxHighlighter):

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        self.keywords = ['floor', 'ceiling', 'sqrt', 'log', 'log10', 'log2', 'sin', 'cos',
                            'tan','abs','asin', 'acos', 'atan', 'radians', 'degrees','hex',
                            'bin','dec','min','max','sum','pi','abs','bitget']
        self.operators = ['\+', '-', '\*', '<<', '>>', '\^', '\&', '/', '0b', '0x']

        self.styles =   {   'keyword': self.styleFormat('yellow', 'bold'),
                            'operators': self.styleFormat('light blue'),
                            'symbols': self.styleFormat('light green', 'bold')}

        rules = []
        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, self.styles['keyword'])
            for w in self.keywords]
        rules += [(r'%s' % o, 0, self.styles['operators'])
            for o in self.operators]

        # Build a QRegExp for each pattern
        self.intRules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]

        self.rules = self.intRules

    def styleFormat(self, color, style=''):
        """Return a QTextCharFormat with the given attributes.
        """
        _color = QColor()
        _color.setNamedColor(color)

        _format = QTextCharFormat()
        _format.setForeground(_color)
        if 'bold' in style:
            _format.setFontWeight(QFont.Bold)
        if 'italic' in style:
            _format.setFontItalic(True)

        return _format

    def updateRules(self,symbols):
        newRules = []
        # Keyword, operator, and brace rules
        newRules += [(r'\b%s\b' % w, 0, self.styles['symbols'])
                  for w in symbols]
        newRules = [(QRegExp(pat), index, fmt)
                    for (pat, index, fmt) in newRules]
        self.rules = self.intRules + newRules

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.     """
        # Do other syntax formatting
        for expression, nth, thisFormat in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, thisFormat)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())