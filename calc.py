from math import pi,log,log10,log2,ceil,floor,sqrt,sin,cos,tan,asin,acos,atan,degrees,radians
from PyQt5.QtWidgets import QTextEdit,QGridLayout,QWidget,QLabel
from PyQt5.QtGui import QPixmap
from syntaxhighlighter import KeywordHighlighter
from myfuncs import mySum,bitget,h2a,a2h

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Parameters
        self.maxLines = 100

        # Create Widgets
        self.textEdit = QTextEdit()
        self.resDisp = QTextEdit(readOnly=True)
        self.titleBar = QLabel()

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
        self.textEdit.setStyleSheet("background-color: #232323; color: white; font-size: 20px; border: black")
        self.resDisp.setStyleSheet("background-color: #a0a0a0; font-size: 20px; border: black")
        self.titleBar.setStyleSheet("background-color: rgb(49,49,49)")
        monsterImage = QPixmap("MonsterCalc.png")
        self.titleBar.setPixmap(monsterImage)

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