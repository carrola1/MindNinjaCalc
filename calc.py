#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from math import pi,log,log10,log2,ceil,floor,sqrt,sin,cos,tan,asin,acos,atan,degrees,radians
from PyQt5.QtWidgets import QTextEdit,QApplication,QGridLayout,QWidget
from PyQt5.QtGui import QIcon


class Example(QWidget):
    def __init__(self):
        super().__init__()
        # Parameters
        self.maxLines = 100

        # Widgets
        self.textEdit = QTextEdit()
        self.resDisp = QTextEdit(readOnly=True)

        # Text Fields
        self.curText = ['']*self.maxLines
        self.resText = ['']*self.maxLines

        # Variables
        self.symDict =  {   '0e': '0*10**',
                            '1e': '1*10**',
                            '2e': '2*10**',
                            '3e': '3*10**',
                            '4e': '4*10**',
                            '5e': '5*10**',
                            '6e': '6*10**',
                            '7e': '7*10**',
                            '8e': '8*10**',
                            '9e': '9*10**'
                        }
        self.keyList = [('uu' + str(i)) for i in range(0,self.maxLines)]
        for ii in range(0,self.maxLines):
            self.symDict[self.keyList[ii]] = self.keyList[ii]
        self.initUI()

    def initUI(self):
        # Style
        self.textEdit.setStyleSheet("background-color: #1f3960; color: white; font-size: 20px")
        self.resDisp.setStyleSheet("background-color: #8191aa; font-size: 20px")

        # Callback
        self.textEdit.textChanged.connect(self.updateResults)

        # Layout
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.textEdit, 0, 0)
        grid.addWidget(self.resDisp, 0, 1)
        self.setGeometry(600, 600, 700, 500)
        self.setWindowTitle('Main window')
        self.show()

    def updateResults(self):
        # Get text and break into lines
        text = self.textEdit.toPlainText()
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
        newResults = newResults.join(self.resText)
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
        else:
            self.evalExp(newLine, lineNum)
        return

    def evalExp(self,newExp,lineNum):
        try:
            for key in self.symDict:
                newExp = newExp.replace(key, self.symDict[key])
            newResult = str(eval(newExp))
            self.resText[lineNum] = newResult
        except:
            self.resText[lineNum] = ''
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())