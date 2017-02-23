from math import pi,log,log10,log2,ceil,floor,sqrt,sin,cos,tan,asin,acos,atan
from math import radians as rad
from math import degrees as deg
from PyQt5.QtWidgets import QTextEdit,QGridLayout,QWidget,QLabel,QToolButton,QAction,QSplitter
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QSize,Qt
from syntaxhighlighter import KeywordHighlighter
from myfuncs import bitget,h2a,a2h
from myfuncs import mySum as sum
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
        self.funcTool = QToolButton()
        self.splitEdit = QSplitter()

        # Create Text Fields of length maxLines
        self.curText = ['']*self.maxLines
        self.resText = ['']*self.maxLines

        # Supported functions and symbols
        self.funcs = ['floor', 'ceil', 'sqrt', 'log', 'log10', 'log2', 'sin', 'cos',
                        'tan', 'abs', 'asin', 'acos', 'atan', 'rad', 'deg', 'hex',
                        'bin', 'dec', 'min', 'max', 'sum', 'bitget', 'a2h', 'h2a']
        self.operators = ['\+', '-', '\*', '<<', '>>', '\^', '\&', '/', '=','%','|']
        self.prefix = ['0x','0b']
        self.suffix = ['p','n','u','m','k','M']
        self.tweener = ['e']
        self.symbols = ['ans','pi']

        # Lenth Units (refereced to mm)
        unitsLen = {'mm':'1', 'cm':'10', 'm':'1000', 'mil':'0.0254', 'in': '25.4',
                         'ft':'304.8'}
        lenKeys = ['mm','cm','m','mil','in','ft']

        # Volume Units (refereced to ml)
        unitsVol = {'ml': '1', 'mL': '1', 'l': '1000', 'L': '1000', 'c': '236.588',
                         'pt': '473.176', 'qt': '946.353', 'gal': '3785.41', 'oz': '29.5735',
                         'tsp': '4.92892', 'tbl': '14.7868'}
        volKeys = ['ml', 'mL', 'l', 'L', 'c', 'pt', 'qt', 'gal', 'fl', 'tsp', 'tbl']

        # Mass Units (refereced to g)
        unitsMass = {'mg': '.001', 'g': '1', 'kg': '1000', 'lbs': '453.592', 'oz': '28.3495'}
        massKeys = ['mg', 'g', 'kg', 'lbs', 'oz']

        # Force Units (refereced to N)
        unitsForce = {'N': '1', 'kN': '1000', 'lbf': '4.44822'}
        forceKeys = ['N', 'kN', 'lbf']

        # Temp Units (C to F handled diferently since transform is not proportional)
        tempKeys = ['C', 'F']

        self.units = [unitsLen,unitsVol,unitsMass,unitsForce]
        self.unitKeys = lenKeys + volKeys + massKeys + forceKeys + tempKeys

        # Syntax Highlighter
        self.highlight = KeywordHighlighter(self.textEdit.document(),self.funcs,self.operators,
                                            self.symbols,self.suffix,self.prefix,self.tweener,
                                            self.unitKeys)

        # Parameters for user-defined symbols
        self.userSyms = {}
        self.symKeys = []
        self.clear()

        # Default # sig figs to display
        self.sigFigs = 5

        self.initUI()

    def initUI(self):
        # Widget Styles
        self.textEdit.setStyleSheet("background-color: #232323; color: white; font-size: 20px; border: black;"
                                    "selection-color: #232323; selection-background-color: #c0c0c0")
        self.resDisp.setStyleSheet("background-color: #a0a0a0; font-size: 20px; border: black;"
                                   "selection-color: white; selection-background-color: #232323")
        self.titleBar.setStyleSheet("background-color: rgb(49,49,49)")
        self.splitEdit.setHandleWidth(2)
        self.splitEdit.setStyleSheet("color: black; background-color: black")
        monsterImage = QPixmap("MonsterCalc.png")
        self.titleBar.setPixmap(monsterImage)
        funcIcon = QIcon()
        functionImage = QPixmap("Functions.png")
        funcIcon.addPixmap(functionImage)
        self.funcTool.setIcon(funcIcon)
        self.setStyleSheet(
            """
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
        func0  = QAction('floor:  Round down',self.funcTool)
        func1  = QAction('ceil:   Round up',self.funcTool)
        func2  = QAction('sqrt:   Square root', self.funcTool)
        func3  = QAction('log:    Log base e', self.funcTool)
        func4  = QAction('log10:  Log base 10', self.funcTool)
        func5  = QAction('log2:   Log base 2', self.funcTool)
        func6  = QAction('sin:    Sine', self.funcTool)
        func7  = QAction('cos:    Cosine', self.funcTool)
        func8  = QAction('tan:    Tangent', self.funcTool)
        func9  = QAction('asin:   Arc-Sine', self.funcTool)
        func10 = QAction('acos:   Arc-Cosine', self.funcTool)
        func11 = QAction('atan:   Arc-Tangent', self.funcTool)
        func12 = QAction('abs:    Absolute value', self.funcTool)
        func13 = QAction('rad:    Convert deg to rad', self.funcTool)
        func14 = QAction('deg:    Convert rad to deg', self.funcTool)
        func15 = QAction('hex:    Convert to hex', self.funcTool)
        func16 = QAction('bin:    Convert to bin', self.funcTool)
        func17 = QAction('dec:    Convert to dec', self.funcTool)
        func18 = QAction('bitget: Bit slice (value,lsb,msb)', self.funcTool)
        func19 = QAction('a2h:    Convert ASCII \'str\' to hex', self.funcTool)
        func20 = QAction('h2a:    Convert hex to ASCII', self.funcTool)
        func21 = QAction('min:    Return list min', self.funcTool)
        func22 = QAction('max:    Return list max', self.funcTool)
        func23 = QAction('sum:    Return list sum', self.funcTool)

        funcs = [func0,func1,func2,func3,func4,func5,func6,func7,func8,func9,func10,func11,
                 func12,func13,func14,func15,func16,func17,func18,func19,func20,func21,func22,
                 func23]
        for action in funcs:
            action.triggered.connect(self.funcTriggered)
            self.funcTool.addAction(action)
        self.funcTool.setPopupMode(2)

        # Text changed callback
        self.textEdit.textChanged.connect(self.updateResults)

        # Layout
        grid = QGridLayout()
        self.setLayout(grid)
        self.titleBar.setFixedHeight(30)
        self.funcTool.setIconSize(QSize(200, 23))
        self.splitEdit.addWidget(self.textEdit)
        self.splitEdit.addWidget(self.resDisp)
        grid.addWidget(self.titleBar,0,0)
        grid.addWidget(self.funcTool,0,1,Qt.AlignRight)
        grid.addWidget(self.splitEdit,1,0,1,2)

    def updateResults(self):
        # Get text and break into lines
        text = self.textEdit.toPlainText()
        textLines = text.split("\n")

        # Find changes and evaluate each line
        for ii in range(0,len(textLines)):
            if (textLines[ii] != self.curText[ii]):
                self.curText[ii] = textLines[ii]
            self.evalLine(ii)
        self.highlight.highlightBlock(text)
        # Clear unused lines
        self.resText[len(textLines):] = ['']*(len(self.resText)-len(textLines))

        # Update displayed results
        newResults = "\n"
        newResults = newResults.join(self.resText[0:len(textLines)])
        self.resDisp.setPlainText(newResults)
        return

    def evalLine(self,lineNum):
        newLine = self.curText[lineNum]
        if ('=' in newLine):
            # Variable assignment detected
            newLine = newLine.split('=')
            newVar = newLine[0].strip()
            if (newVar != '') & (' ' not in newVar):
                self.evalExp(newLine[1],lineNum)
                self.userSyms[newVar] = self.userSyms.pop(self.symKeys[lineNum])
                self.userSyms[newVar] = self.resText[lineNum]
                self.symKeys[lineNum] = newVar
                self.highlight.updateRules(self.symKeys)
        elif (' to ' in newLine):
            # Conversion detected
            newLine = self.convUnits(newLine)
            self.evalExp(newLine, lineNum)
        else:
            self.evalExp(newLine, lineNum)
        return

    def evalExp(self,newExp,lineNum):
        try:
            # Find and replace user-defined symbols with values
            # Also recognizes 'ans' and replaced with result from previous line
            for key in self.userSyms:
                if (lineNum > 0):
                    self.userSyms['ans'] = self.resText[lineNum-1]
                else:
                    self.userSyms['ans'] = 'None'
                newExp = re.sub(r'\b'+key+r'\b',self.userSyms[key],newExp)

            # scientific notations
            newExp = re.sub(r'(\d+[.,]?\d*)(p\b)', r'(\g<1>*10**-12)',newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(n\b)', r'(\g<1>*10**-9)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(u\b)', r'(\g<1>*10**-6)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(m\b)', r'(\g<1>*10**-3)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(k\b)', r'(\g<1>*10**3)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(M\b)', r'(\g<1>*10**6)', newExp)

            newResult = eval(newExp)
            try:
                # Apply sig figs
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

    def convUnits(self,newLine):
        newLine = newLine.split('to')
        convFrom = newLine[0]
        convTo = newLine[1]
        try:
            # Special case for 'C to F' and 'F to C'
            if ((' C ' in convFrom) & (' F' in convTo)):
                convFrom = re.sub(r'\b' + 'C' + r'\b', '*1.8+32', convFrom)
                convTo = re.sub(r'\b' + 'F' + r'\b', '', convTo)
                newLine = convFrom + convTo
                return newLine
            elif ((' F ' in convFrom) & (' C' in convTo)):
                convFrom = re.sub(r'\b' + 'F' + r'\b', '/1.8-17.778', convFrom)
                convTo = re.sub(r'\b' + 'C' + r'\b', '', convTo)
                newLine = convFrom + convTo
                return newLine
            else:
                for unitType in self.units:
                    for unit in unitType:
                        convFrom = re.sub(r'\b' + unit + r'\b', '*' + unitType[unit], convFrom)
                        convTo = re.sub(r'\b' + unit + r'\b', '/' + unitType[unit], convTo)
                    if (convFrom != newLine[0]) & (convTo != newLine[1]):
                        newLine = convFrom + convTo
                        return newLine
                    else:
                        convFrom = newLine[0]
                        convTo = newLine[1]
        except:
            pass
        return newLine

    def funcTriggered(self):
        trigFunc = self.sender()
        funcFullText = trigFunc.text()
        funcText = funcFullText.split(':')[0] + '('
        self.textEdit.insertPlainText(funcText)
        return

    def clear(self):
        self.textEdit.setPlainText('')
        # Overload symbols
        self.userSyms = {}
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
