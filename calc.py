import sys,ctypes
from math import pi,log,log10,log2,ceil,floor,sqrt,sin,cos,tan,asin,acos,atan,exp
from math import radians as rad
from math import degrees as deg
from PyQt5.QtWidgets import QTextEdit,QGridLayout,QWidget,QLabel,QToolButton,QAction,QSplitter
from PyQt5.QtGui import QPixmap,QIcon,QFont
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
        self.symTool = QToolButton()
        self.splitEdit = QSplitter()

        # Create text fields of length maxLines
        self.curText = ['']*self.maxLines
        self.resText = ['']*self.maxLines

        # Supported functions and symbols
        self.funcs = ['floor', 'ceil', 'sqrt', 'log', 'log10', 'log2', 'exp', 'sin', 'cos',
                        'tan', 'abs', 'asin', 'acos', 'atan', 'rad', 'deg', 'hex',
                        'bin', 'dec', 'min', 'max', 'sum', 'bitget', 'a2h', 'h2a']
        self.operators = ['\+', '-', '\*', '<<', '>>', '\^', '\&', '/', '=','%','\|']
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
        volKeys = ['ml', 'mL', 'l', 'L', 'c', 'pt', 'qt', 'gal', 'oz', 'tsp', 'tbl']

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
        if ('win32' in sys.platform):
            monsterImage = QPixmap("C:\GitHub\MonsterCalc\MonsterCalc.png")
        else:
            monsterImage = QPixmap("/Users/Andrew/Documents/Python/MonsterCalc/MonsterCalc.png")
        self.titleBar.setPixmap(monsterImage)
        funcIcon = QIcon()
        if ('win32' in sys.platform):
            functionImage = QPixmap("C:\GitHub\MonsterCalc\Functions.png")
        else:
            functionImage = QPixmap("/Users/Andrew/Documents/Python/MonsterCalc/Functions.png")
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
        funcT0 = QAction('MATH',self.funcTool)
        func0  = QAction('floor:  Round down',self.funcTool)
        func1  = QAction('ceil:   Round up',self.funcTool)
        func2  = QAction('min:    Return list min', self.funcTool)
        func3  = QAction('max:    Return list max', self.funcTool)
        func4  = QAction('sum:    Return list sum', self.funcTool)
        func5  = QAction('sqrt:   Square root', self.funcTool)
        func6  = QAction('abs:    Absolute value', self.funcTool)
        func7  = QAction('log:    Log base e', self.funcTool)
        func8  = QAction('log10:  Log base 10', self.funcTool)
        func9  = QAction('log2:   Log base 2', self.funcTool)
        func10 = QAction('exp:    Exponential (e**x)', self.funcTool)
        funcT1 = QAction('GEOMETRY', self.funcTool)
        func11 = QAction('sin:    Sine', self.funcTool)
        func12 = QAction('cos:    Cosine', self.funcTool)
        func13 = QAction('tan:    Tangent', self.funcTool)
        func14 = QAction('asin:   Arc-Sine', self.funcTool)
        func15 = QAction('acos:   Arc-Cosine', self.funcTool)
        func16 = QAction('atan:   Arc-Tangent', self.funcTool)
        func17 = QAction('rad:    Convert deg to rad', self.funcTool)
        func18 = QAction('deg:    Convert rad to deg', self.funcTool)
        funcT2 = QAction('PROGRAMMING', self.funcTool)
        func19 = QAction('hex:    Convert to hex', self.funcTool)
        func20 = QAction('bin:    Convert to bin', self.funcTool)
        func21 = QAction('dec:    Convert to dec', self.funcTool)
        func22 = QAction('bitget: Bit slice (value,lsb,msb)', self.funcTool)
        func23 = QAction('a2h:    Convert ASCII \'str\' to hex', self.funcTool)
        func24 = QAction('h2a:    Convert hex to ASCII', self.funcTool)

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPixelSize(16)
        funcT0.setFont(titleFont)
        funcT1.setFont(titleFont)
        funcT2.setFont(titleFont)

        funcs = [funcT0,func0,func1,func2,func3,func4,func5,func6,func7,func8,func9,func10,funcT1,func11,
                 func12,func13,func14,func15,func16,func17,func18,funcT2,func19,func20,func21,func22,
                 func23,func24]
        for action in funcs:
            if (":" in action.text()):
                action.triggered.connect(self.funcTriggered)
            self.funcTool.addAction(action)
        self.funcTool.setPopupMode(2)

        # Symbol Tool Button
        symT0 = QAction('MISC', self.symTool)
        sym0  = QAction('ans:   Result from previous line', self.symTool)
        sym1  = QAction('to:    Unit conversion (ex. 5 mm to in)', self.symTool)
        symT1 = QAction('MATH', self.symTool)
        sym2  = QAction('**:    Power (ex. 2**3 = 8)', self.symTool)
        sym3  = QAction('%:     Modulus (ex. 5 % 2 = 1)', self.symTool)
        sym4  = QAction('e:     Exponent (ex. 5e-3 = 0.005)', self.symTool)
        symT2 = QAction('PROGRAMMING', self.symTool)
        sym5  = QAction('0x:    Hex (ex. 0x12 = 18)', self.symTool)
        sym6  = QAction('0b:    Binary (ex. 0b101 = 5)', self.symTool)
        sym7  = QAction('<<:    Shift left (ex. 2 << 2 = 8)', self.symTool)
        sym8  = QAction('>>:    Shift right (ex. 8 >> 2 = 2)', self.symTool)
        sym9  = QAction('|:     Bitwise OR (ex. 8 | 1 = 9)', self.symTool)
        sym10 = QAction('&:     Bitwise AND (ex. 5 & 1 = 1)', self.symTool)
        sym11 = QAction('^:     Bitwise XOR (ex. 5 ^ 1 = 4)', self.symTool)
        symT3 = QAction('SCIENTIFIC NOTATION', self.symTool)
        sym12 = QAction('p:     Pico (ex. 1p = 1e-12)', self.symTool)
        sym13 = QAction('n:     Nano (ex. 1n = 1e-9)', self.symTool)
        sym14 = QAction('u:     Micro (ex. 1u = 1e-6)', self.symTool)
        sym15 = QAction('m:     Milli (ex. 1m = 1e-3)', self.symTool)
        sym16 = QAction('k:     Killo (ex. 1k = 1e3)', self.symTool)
        sym17 = QAction('M:     Mega (ex. 1M = 1e6)', self.symTool)
        symT4 = QAction('UNITS', self.symTool)
        sym18 = QAction('mm:    Millimeters', self.symTool)
        sym19 = QAction('cm:    Centimeters', self.symTool)
        sym20 = QAction('m:     Meters', self.symTool)
        sym21 = QAction('km:    Killometers', self.symTool)
        sym22 = QAction('mil:   Thousandths of an inch', self.symTool)
        sym23 = QAction('mL:    Milliliter', self.symTool)
        sym24 = QAction('L:     Liter', self.symTool)
        sym25 = QAction('tsp:   Teaspoon', self.symTool)
        sym26 = QAction('tbl:   Tablespoon', self.symTool)
        sym27 = QAction('oz:    Fluid ounce', self.symTool)
        sym28 = QAction('pt:    Pint', self.symTool)
        sym29 = QAction('qt:    Quart', self.symTool)
        sym30 = QAction('gal:   Gallon', self.symTool)
        sym31 = QAction('mg:    Milligram', self.symTool)
        sym32 = QAction('g:     Gram', self.symTool)
        sym33 = QAction('kg:    Killogram', self.symTool)
        sym34 = QAction('oz:    Ounce', self.symTool)
        sym35 = QAction('lbs:   Pound', self.symTool)
        sym36 = QAction('N:     Newton', self.symTool)
        sym37 = QAction('kN:    Killonewton', self.symTool)
        sym38 = QAction('lbf:   Pound force', self.symTool)
        sym39 = QAction('C:     Degrees celsius', self.symTool)
        sym40 = QAction('F:     Degrees farenheit', self.symTool)

        syms = [symT0, sym0, sym1, symT1, sym2, sym3, sym4, symT2, sym5, sym6, sym7, sym8, sym9, sym10, sym11,
                 symT3, sym12, sym13, sym14, sym15, sym16, symT4, sym17, sym18, sym19, sym20, sym21, sym22,
                 sym23, sym24, sym25, sym25, sym26, sym27, sym28, sym29, sym30, sym31, sym32, sym33, sym34,
                 sym35, sym36, sym37, sym38, sym39, sym40]
        for action in syms:
            if (":" in action.text()):
                action.triggered.connect(self.symTriggered)
            self.symTool.addAction(action)
        self.symTool.setPopupMode(2)

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
        #grid.addWidget(self.symTool, 0, 1, Qt.AlignRight)
        grid.addWidget(self.funcTool,0,2,Qt.AlignRight)
        grid.addWidget(self.splitEdit,1,0,1,3)

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

    def symTriggered(self):
        symFunc = self.sender()
        symFullText = symFunc.text()
        symText = symFullText.split(':')[0]
        self.textEdit.insertPlainText(symText)
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
