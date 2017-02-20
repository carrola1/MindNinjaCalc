from math import pi,log,log10,log2,ceil,floor,sqrt,sin,cos,tan,asin,acos,atan
from math import radians as rad
from math import degrees as deg
from PyQt5.QtWidgets import QTextEdit,QGridLayout,QWidget,QLabel,QToolButton,QAction
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QSize,Qt
from syntaxhighlighter import KeywordHighlighter
from myfuncs import mySum,bitget,h2a,a2h
import re

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Parameters
        self.maxLines = 100

        # Create Widgets
        self.textEdit = QTextEdit()
        self.resDisp = QTextEdit(readOnly=True)
        self.titleBar = QLabel()
        self.funcList = QToolButton()

        # Create Text Fields of length maxLines
        self.curText = ['']*self.maxLines
        self.resText = ['']*self.maxLines

        self.funcs = ['floor', 'ceil', 'sqrt', 'log', 'log10', 'log2', 'sin', 'cos',
                         'tan', 'abs', 'asin', 'acos', 'atan', 'rad', 'deg', 'hex',
                         'bin', 'dec', 'min', 'max', 'sum', 'bitget',
                         'a2h', 'h2a']
        self.operators = ['\+', '-', '\*', '<<', '>>', '\^', '\&', '/', '=','%']
        self.prefix = ['0x','0b']
        self.suffix = ['p','n','u','m','k','M','e']
        self.symbols = ['ans','pi']

        # Syntax Highlighter
        self.highlight = KeywordHighlighter(self.textEdit.document(),self.funcs,self.operators,
                                            self.symbols,self.suffix,self.prefix)

        self.userSyms = {}
        self.symKeys = []
        self.clear()

        self.sigFigs = 4

        self.initUI()

    def initUI(self):
        # Widget Styles
        self.textEdit.setStyleSheet("background-color: #232323; color: white; font-size: 20px; border: black")
        self.resDisp.setStyleSheet("background-color: #a0a0a0; font-size: 20px; border: black")
        self.titleBar.setStyleSheet("background-color: rgb(49,49,49)")
        monsterImage = QPixmap("MonsterCalc.png")
        self.titleBar.setPixmap(monsterImage)
        funcIcon = QIcon()
        functionImage = QPixmap("Functions.png")
        funcIcon.addPixmap(functionImage)
        self.funcList.setIcon(funcIcon)
        self.setStyleSheet("""
                                QToolButton {
                                    background-color: #a0a0a0;
                                }

                                QMenu {
                                    background-color: #232323;
                                    color: #a0a0a0;
                                    font: bold;
                                    font-family: "Lucida Console";
                                    border: 1px solid #000;
                                }

                                QMenu::item::selected {
                                    background-color: rgb(30,30,30);
                                }
                            """)

        # Do not allow text wrapping
        self.textEdit.setLineWrapMode(0)
        self.resDisp.setLineWrapMode(0)

        # Turn off display scrollbar and synchronize scrolling
        self.resDisp.setVerticalScrollBarPolicy(1)
        self.textEdit.verticalScrollBar().valueChanged.connect(self.resDisp.verticalScrollBar().setValue)
        self.resDisp.verticalScrollBar().valueChanged.connect(self.textEdit.verticalScrollBar().setValue)

        # Function Tool Button
        func0  = QAction('floor:  Round down',self.funcList)
        func1  = QAction('ceil:   Round up',self.funcList)
        func2  = QAction('sqrt:   Square root', self.funcList)
        func3  = QAction('log:    Log base e', self.funcList)
        func4  = QAction('log10:  Log base 10', self.funcList)
        func5  = QAction('log2:   Log base 2', self.funcList)
        func6  = QAction('sin:    Sine', self.funcList)
        func7  = QAction('cos:    Cosine', self.funcList)
        func8  = QAction('tan:    Tangent', self.funcList)
        func9  = QAction('asin:   Arc-Sine', self.funcList)
        func10 = QAction('acos:   Arc-Cosine', self.funcList)
        func11 = QAction('atan:   Arc-Tangent', self.funcList)
        func12 = QAction('abs:    Absolute value', self.funcList)
        func13 = QAction('rad:    Convert deg to rad', self.funcList)
        func14 = QAction('deg:    Convert rad to deg', self.funcList)
        func15 = QAction('hex:    Convert to hex', self.funcList)
        func16 = QAction('bin:    Convert to bin', self.funcList)
        func17 = QAction('dec:    Convert to dec', self.funcList)
        func18 = QAction('bitget: Bit slice (value,lsb,msb)', self.funcList)
        func19 = QAction('a2h:    Convert ASCII \'str\' to hex', self.funcList)
        func20 = QAction('h2a:    Convert hex to ASCII', self.funcList)
        func21 = QAction('min:    Return list min', self.funcList)
        func22 = QAction('max:    Return list max', self.funcList)
        func23 = QAction('sum:    Return list sum', self.funcList)

        funcs = [func0,func1,func2,func3,func4,func5,func6,func7,func8,func9,func10,func11,
                 func12,func13,func14,func15,func16,func17,func18,func19,func20,func21,func22,
                 func23]
        for action in funcs:
            action.triggered.connect(self.funcTriggered)
            self.funcList.addAction(action)
        self.funcList.setPopupMode(2)

        # Callbacks
        self.textEdit.textChanged.connect(self.updateResults)

        # Layout
        grid = QGridLayout()
        self.setLayout(grid)
        self.titleBar.setFixedHeight(25)
        self.funcList.setIconSize(QSize(200, 25))
        grid.addWidget(self.titleBar,0,0)
        grid.addWidget(self.funcList,0,1,Qt.AlignRight)
        grid.addWidget(self.textEdit, 1, 0)
        grid.addWidget(self.resDisp, 1, 1)

    def updateResults(self):
        # Get text and break into lines
        text = self.textEdit.toPlainText()
        textLines = text.split("\n")

        # Find change
        for ii in range(0,len(textLines)):
            if (textLines[ii] != self.curText[ii]):
                self.curText[ii] = textLines[ii]
            self.evalLine(ii)
        self.highlight.highlightBlock(text)
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
            if (newVar != '') & (' ' not in newVar):
                self.evalExp(newLine[1],lineNum)
                self.userSyms[newVar] = self.userSyms.pop(self.symKeys[lineNum])
                self.userSyms[newVar] = self.resText[lineNum]
                self.symKeys[lineNum] = newVar
                self.highlight.updateRules(self.symKeys)
        else:
            self.evalExp(newLine, lineNum)
        return

    def evalExp(self,newExp,lineNum):
        try:
            for key in self.userSyms:
                if (lineNum > 0):
                    self.userSyms['ans'] = self.resText[lineNum-1]
                else:
                    self.userSyms['ans'] = 'None'
                newExp = re.sub(r'\b'+key+r'\b',self.userSyms[key],newExp)

            # scientific notations
            newExp = re.sub('(\d)(p)', '(\g<1>*10**-12)',newExp)
            newExp = re.sub('(\d)(n)', '(\g<1>*10**-9)', newExp)
            newExp = re.sub('(\d)(u)', '(\g<1>*10**-6)', newExp)
            newExp = re.sub('(\d)(m)', '(\g<1>*10**-3)', newExp)
            newExp = re.sub('(\d)(k)', '(\g<1>*10**3)', newExp)
            newExp = re.sub('(\d)(M)', '(\g<1>*10**6)', newExp)

            newResult = eval(newExp)
            try:
                if (newResult % 1 != 0):
                    newResult = '{0:.{digits}g}'.format(newResult, digits=self.sigFigs)
            except:
                pass
            newResult = str(newResult)

            # Ignore python's "Built-in Function..." warning
            if ('function' not in newResult):
                self.resText[lineNum] = newResult
            else:
                self.resText[lineNum] = ''
        except:
            self.resText[lineNum] = ''
        return

    def funcTriggered(self):
        trigFunc = self.sender()
        funcFullText = trigFunc.text()
        funcText = funcFullText.split(':')[0] + '('
        self.textEdit.insertPlainText(funcText)
        return

    def clear(self):
        self.textEdit.setPlainText('')
        # Overload symbols
        self.userSyms = {
                        'sum':  'mySum'  # replace built-in sum() to take a list of args instead of a py list
                        }
        # Store userSyms keys
        self.symKeys = [('uu' + str(i)) for i in range(0, self.maxLines)]
        for ii in range(0, self.maxLines):
            self.userSyms[self.symKeys[ii]] = self.symKeys[ii]
        self.highlight.updateRules(self.symKeys)
        return

    def setSigFigs(self,digits):
        try:
            self.sigFigs = digits
            self.updateResults()
        except:
            pass
        return
