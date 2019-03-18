import sys
import os
import ctypes
from math import pi, log2, ceil, floor, e
from cmath import sqrt, sin, cos, tan, asin, acos, atan, exp, log, log10
from cmath import phase, polar, rect
from math import radians as rad
from math import degrees as deg
from PySide2.QtWidgets import QTextEdit, QGridLayout, QWidget, QLabel
from PySide2.QtWidgets import QToolButton, QAction, QSplitter
from PySide2.QtGui import QPixmap, QIcon, QFont
from PySide2.QtCore import QSize, Qt
from syntaxhighlighter import KeywordHighlighter
from myfuncs import bitget, h2a, a2h, eng_string, findres, findrdiv, vdiv, rpar
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
        self.eeTool = QToolButton()
        self.funcTool = QToolButton()
        self.symTool = QToolButton()
        self.unitTool = QToolButton()
        self.splitEdit = QSplitter()

        # Create text fields of length maxLines
        self.curText = ['']*self.maxLines
        self.resText = ['']*self.maxLines

        # Supported functions and symbols
        self.funcs = ['floor', 'ceil', 'sqrt', 'log', 'log10', 'log2', 'exp',
                      'sin', 'cos', 'tan', 'abs', 'asin', 'acos', 'atan',
                      'rad', 'deg', 'polar', 'rect', 'phase',
                      'hex', 'bin', 'min', 'max', 'sum', 'bitget', 'a2h',
                      'h2a', 'findres', 'findrdiv', 'rpar', 'vdiv']
        self.operators = ['\+', '-', '\*', '<<', '>>', '\^', '\&', '/', '=',
                          '%', '\|']
        self.prefix = ['0x', '0b']
        self.suffix = ['p', 'n', 'u', 'm', 'k', 'M', 'G']
        self.tweener = ['e']
        self.symbols = ['ans', 'pi', 'e']
        self.unusual_syms = ['to']

        # Lenth Units (refereced to mm)
        unitsLen = {'mm': '1', 'cm': '10', 'm': '1000', 'km': '1000000',
                    'mil': '0.0254', 'in': '25.4', 'ft': '304.8'}
        lenKeys = ['mm', 'cm', 'm', 'km', 'mil', 'in', 'ft']

        # Volume Units (refereced to ml)
        unitsVol = {'ml': '1', 'mL': '1', 'l': '1000', 'L': '1000',
                    'c': '236.588', 'pt': '473.176', 'qt': '946.353',
                    'gal': '3785.41', 'oz': '29.5735', 'tsp': '4.92892',
                    'tbl': '14.7868'}
        volKeys = ['ml', 'mL', 'l', 'L', 'c', 'pt', 'qt', 'gal', 'oz', 'tsp',
                   'tbl']

        # Mass Units (refereced to g)
        unitsMass = {'mg': '.001', 'g': '1', 'kg': '1000', 'lbs': '453.592',
                     'oz': '28.3495'}
        massKeys = ['mg', 'g', 'kg', 'lbs', 'oz']

        # Force Units (refereced to N)
        unitsForce = {'N': '1', 'kN': '1000', 'lbf': '4.44822'}
        forceKeys = ['N', 'kN', 'lbf']

        # Temp Units (C to F unique since transform is not proportional)
        tempKeys = ['C', 'F']

        self.units = [unitsLen, unitsVol, unitsMass, unitsForce]
        self.unitKeys = lenKeys + volKeys + massKeys + forceKeys + tempKeys

        # Syntax Highlighter
        self.highlight = KeywordHighlighter(self.textEdit.document(),
                                            self.funcs, self.operators,
                                            self.symbols, self.suffix,
                                            self.prefix, self.tweener,
                                            self.unitKeys, self.unusual_syms)

        # Parameters for user-defined symbols
        self.userSyms = {}
        self.symKeys = []
        self.clear()

        # Default # sig figs to display
        self.sigFigs = 5

        # Set result formatting ('scientific', 'engineering', 'si')
        self.resFormat = 'engineering'

        # Convert '^' to '**'
        self.convXorToExp = 'True'

        self.initUI()

    def initUI(self):
        # Widget Styles
        self.textEdit.setStyleSheet('background-color: #212121;' +
                                    'color: white; font-size: 20px;' +
                                    'border: black;' +
                                    'selection-color: #212121;' +
                                    'selection-background-color: #c0c0c0')
        self.resDisp.setStyleSheet('background-color: #b0b0b0;' +
                                   'font-size: 20px; border: black;' +
                                   'selection-color: white;' +
                                   'selection-background-color: #212121')
        self.titleBar.setStyleSheet("background-color: rgb(49,49,49)")
        self.splitEdit.setHandleWidth(2)
        self.splitEdit.setStyleSheet("color: black; background-color: black")
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        if ('win32' in sys.platform):
            monsterImage = QPixmap(path + "\MonsterCalc.png")
        else:
            monsterImage = QPixmap(
                '/Users/Andrew/Documents/Python/MonsterCalc/MonsterCalc.png')
        self.titleBar.setPixmap(monsterImage)
        funcIcon = QIcon()
        if ('win32' in sys.platform):
            functionImage = QPixmap(path + "\Functions.png")
        else:
            functionImage = QPixmap(
                '/Users/Andrew/Documents/Python/MonsterCalc/Functions.png')
        funcIcon.addPixmap(functionImage)
        self.eeTool.setText('EE')
        self.funcTool.setText('Math')
        self.symTool.setText('Symbols')
        self.unitTool.setText('Units')
        self.setStyleSheet(
            """
                QToolButton {
                    background-color: #b0b0b0;
                    font-family: "Lucida Console";
                    font-size: 18px;
                    color: #212121;
                }

                QMenu {
                    background-color: #212121;
                    color: #b0b0b0;
                    font-family: "Lucida Console";
                    border: 1px solid #000;
                }

                QMenu::item::selected {
                    background-color: rgb(30,30,30);
                }
            """)

        # Do not allow text wrapping
        self.textEdit.LineWrapMode = QTextEdit.NoWrap
        self.resDisp.LineWrapMode = QTextEdit.NoWrap

        # Turn off display scrollbar and synchronize scrolling
        self.resDisp.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textEdit.verticalScrollBar().valueChanged.connect(
            self.resDisp.verticalScrollBar().setValue)
        self.resDisp.verticalScrollBar().valueChanged.connect(
            self.textEdit.verticalScrollBar().setValue)

        # Function Tool Button
        funcT0 = QAction('GENERAL MATH', self.funcTool)
        func0 = QAction('floor:  Round down', self.funcTool)
        func1 = QAction('ceil:   Round up', self.funcTool)
        func2 = QAction('min:    Return list min', self.funcTool)
        func3 = QAction('max:    Return list max', self.funcTool)
        func4 = QAction('sum:    Return list sum', self.funcTool)
        func5 = QAction('sqrt:   Square root', self.funcTool)
        func6 = QAction('abs:    Absolute value', self.funcTool)
        func7 = QAction('log:    Log base e', self.funcTool)
        func8 = QAction('log10:  Log base 10', self.funcTool)
        func9 = QAction('log2:   Log base 2', self.funcTool)
        func10 = QAction('exp:    Exponential (e**x)', self.funcTool)
        func11 = QAction('phase:  Phase of complex #', self.funcTool)
        func12 = QAction('rect:   Complex polar to rect (mag,ang)',
                         self.funcTool)
        func13 = QAction('polar:  Complex rect to polar', self.funcTool)
        funcT1 = QAction('GEOMETRY', self.funcTool)
        func14 = QAction('sin:    Sine', self.funcTool)
        func15 = QAction('cos:    Cosine', self.funcTool)
        func16 = QAction('tan:    Tangent', self.funcTool)
        func17 = QAction('asin:   Arc-Sine', self.funcTool)
        func18 = QAction('acos:   Arc-Cosine', self.funcTool)
        func19 = QAction('atan:   Arc-Tangent', self.funcTool)
        func20 = QAction('rad:    Convert deg to rad', self.funcTool)
        func21 = QAction('deg:    Convert rad to deg', self.funcTool)

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPixelSize(16)
        funcT0.setFont(titleFont)
        funcT1.setFont(titleFont)

        funcs = [funcT0, func0, func1, func2, func3, func4, func5, func6,
                 func7, func8, func9, func10, func11, func12, func13, funcT1,
                 func14, func15, func16, func17, func18, func19,
                 func20, func21]
        for action in funcs:
            if (":" in action.text()):
                action.triggered.connect(self.funcTriggered)
            self.funcTool.addAction(action)
        self.funcTool.setPopupMode(QToolButton.InstantPopup)

        # EE Tool Button
        eeT0 = QAction('ELECTRICAL', self.funcTool)
        ee0 = QAction('findres: Closest std value (target, tol)', self.eeTool)
        ee1 = QAction('vdiv: Calc voltage divider out (vin, R1, R2)', self.eeTool)
        ee2 = QAction('rpar: Parallel resistor calc (R1, R2, R3...)', self.eeTool)
        ee3 = QAction('findrdiv: Best R divider values (vin, vout, tol)', self.eeTool)
        eeT1 = QAction('PROGRAMMING', self.funcTool)
        ee4 = QAction('hex:    Convert to hex', self.funcTool)
        ee5 = QAction('bin:    Convert to bin', self.funcTool)
        ee6 = QAction('bitget: Bit slice (value,lsb,msb)', self.funcTool)
        ee7 = QAction('a2h:    Convert ASCII \'str\' to hex', self.funcTool)
        ee8 = QAction('h2a:    Convert hex to ASCII', self.funcTool)

        eeT0.setFont(titleFont)
        eeT1.setFont(titleFont)
        ees = [eeT0, ee0, ee1, ee2, ee3, eeT1, ee4, ee5, ee6, ee7, ee8]
        for action in ees:
            if (":" in action.text()):
                action.triggered.connect(self.eeTriggered)
            self.eeTool.addAction(action)
        self.eeTool.setPopupMode(QToolButton.InstantPopup)

        # Symbol Tool Button
        symT0 = QAction('MISC', self.symTool)
        sym0 = QAction('ans:   Result from previous line', self.symTool)
        sym1 = QAction('to:    Unit conversion (ex. 5 mm to in)', self.symTool)
        symT1 = QAction('MATH', self.symTool)
        sym2 = QAction('**:    Power (ex. 2**3 = 8)', self.symTool)
        sym3 = QAction('%:     Modulus (ex. 5 % 2 = 1)', self.symTool)
        sym4 = QAction('e:     Exponent (ex. 5e-3 = 0.005)', self.symTool)
        symT2 = QAction('PROGRAMMING', self.symTool)
        sym5 = QAction('0x:    Hex (ex. 0x12 = 18)', self.symTool)
        sym6 = QAction('0b:    Binary (ex. 0b101 = 5)', self.symTool)
        sym7 = QAction('<<:    Shift left (ex. 2 << 2 = 8)', self.symTool)
        sym8 = QAction('>>:    Shift right (ex. 8 >> 2 = 2)', self.symTool)
        sym9 = QAction('|:     Bitwise OR (ex. 8 | 1 = 9)', self.symTool)
        sym10 = QAction('&:     Bitwise AND (ex. 5 & 1 = 1)', self.symTool)
        sym11 = QAction('^:     Bitwise XOR (ex. 5 ^ 1 = 4)', self.symTool)
        symT3 = QAction('SCIENTIFIC NOTATION', self.symTool)
        sym12 = QAction('p:     Pico (ex. 1p = 1e-12)', self.symTool)
        sym13 = QAction('n:     Nano (ex. 1n = 1e-9)', self.symTool)
        sym14 = QAction('u:     Micro (ex. 1u = 1e-6)', self.symTool)
        sym15 = QAction('m:     Milli (ex. 1m = 1e-3)', self.symTool)
        sym16 = QAction('k:     Killo (ex. 1k = 1e3)', self.symTool)
        sym17 = QAction('M:     Mega (ex. 1M = 1e6)', self.symTool)
        sym18 = QAction('G:     Giga (ex. 1G = 1e9)', self.symTool)

        symT0.setFont(titleFont)
        symT1.setFont(titleFont)
        symT2.setFont(titleFont)
        symT3.setFont(titleFont)

        syms = [symT0, sym0, sym1, symT1, sym2, sym3, sym4, symT2, sym5, sym6,
                sym7, sym8, sym9, sym10, sym11, symT3, sym12, sym13, sym14,
                sym15, sym16, sym17, sym18]
        for action in syms:
            if (":" in action.text()):
                action.triggered.connect(self.symTriggered)
            self.symTool.addAction(action)
        self.symTool.setPopupMode(QToolButton.InstantPopup)

        # Unit Tool Button
        unitT0 = QAction('LENGTH', self.unitTool)
        unit0 = QAction('mm:    Millimeters', self.unitTool)
        unit1 = QAction('cm:    Centimeters', self.unitTool)
        unit2 = QAction('m:     Meters', self.unitTool)
        unit3 = QAction('km:    Killometers', self.unitTool)
        unit4 = QAction('mil:   Thousandths of an inch', self.unitTool)
        unit5 = QAction('in:    Inches', self.unitTool)
        unitT1 = QAction('VOLUME', self.unitTool)
        unit6 = QAction('mL:    Milliliter', self.unitTool)
        unit7 = QAction('L:     Liter', self.unitTool)
        unit8 = QAction('tsp:   Teaspoon', self.unitTool)
        unit9 = QAction('tbl:   Tablespoon', self.unitTool)
        unit10 = QAction('oz:    Fluid ounce', self.unitTool)
        unit11 = QAction('pt:    Pint', self.unitTool)
        unit12 = QAction('qt:    Quart', self.unitTool)
        unit13 = QAction('gal:   Gallon', self.unitTool)
        unitT2 = QAction('MASS', self.unitTool)
        unit14 = QAction('mg:    Milligram', self.unitTool)
        unit15 = QAction('g:     Gram', self.unitTool)
        unit16 = QAction('kg:    Killogram', self.unitTool)
        unit17 = QAction('oz:    Ounce', self.unitTool)
        unit18 = QAction('lbs:   Pound', self.unitTool)
        unitT3 = QAction('FORCE', self.unitTool)
        unit19 = QAction('N:     Newton', self.unitTool)
        unit20 = QAction('kN:    Killonewton', self.unitTool)
        unit21 = QAction('lbf:   Pound force', self.unitTool)
        unitT4 = QAction('TEMPERATURE', self.unitTool)
        unit22 = QAction('C:     Degrees celsius', self.unitTool)
        unit23 = QAction('F:     Degrees farenheit', self.unitTool)

        unitT0.setFont(titleFont)
        unitT1.setFont(titleFont)
        unitT2.setFont(titleFont)
        unitT3.setFont(titleFont)
        unitT4.setFont(titleFont)

        units = [unitT0, unit0, unit1, unit2, unit3, unit4, unit5, unitT1,
                 unit6, unit7, unit8, unit9, unit10, unit11, unit12, unit13,
                 unitT2, unit14, unit15, unit16, unit17, unit18, unitT3,
                 unit19, unit20, unit21, unitT4, unit22, unit23]
        for action in units:
            if (":" in action.text()):
                action.triggered.connect(self.unitTriggered)
            self.unitTool.addAction(action)
        self.unitTool.setPopupMode(QToolButton.InstantPopup)

        # Text changed callback
        self.textEdit.textChanged.connect(self.updateResults)

        # Layout
        grid = QGridLayout()
        self.setLayout(grid)
        self.titleBar.setFixedHeight(30)
        self.funcTool.setFixedWidth(100)
        self.symTool.setFixedWidth(100)
        self.unitTool.setFixedWidth(100)
        self.eeTool.setFixedWidth(100)
        self.splitEdit.addWidget(self.textEdit)
        self.splitEdit.addWidget(self.resDisp)
        #self.splitEdit.setStretchFactor(0, 3)  # better to leave editor/display same width
        grid.addWidget(self.titleBar, 0, 0, Qt.AlignLeft)
        grid.addWidget(self.unitTool, 0, 2, Qt.AlignRight)
        grid.addWidget(self.symTool, 0, 3, Qt.AlignRight)
        grid.addWidget(self.funcTool, 0, 4, Qt.AlignRight)
        grid.addWidget(self.eeTool, 0, 5, Qt.AlignRight)
        grid.addWidget(self.splitEdit, 1, 0, 1, 6)

    def updateResults(self):
        # Get text and break into lines
        text = self.textEdit.toPlainText()
        textLines = text.split("\n")

        # Find changes and evaluate each line
        for ii, line in enumerate(textLines):
            if (line != self.curText[ii]):
                self.curText[ii] = line
            self.evalLine(ii)
        self.highlight.highlightBlock(text)
        # Clear unused lines
        self.resText[len(textLines):] = ['']*(len(self.resText)-len(textLines))

        # Update displayed results
        newResults = "\n"
        newResults = newResults.join(self.resText[0:len(textLines)])
        self.resDisp.setPlainText(newResults)
        return

    def evalLine(self, lineNum):
        newLine = self.curText[lineNum]
        if ('=' in newLine):
            # Variable assignment detected
            newLine = newLine.split('=')
            newVar = newLine[0].strip()
            if ((newVar != '') & (' ' not in newVar)):
                self.evalExp(newLine[1], lineNum)
                try:
                    self.userSyms[newVar] = self.userSyms.pop(
                        self.symKeys[lineNum])
                except:
                    pass    # In case variable doesn't exist
                self.userSyms[newVar] = self.resText[lineNum]
                self.symKeys[lineNum] = newVar
                self.highlight.updateRules(self.symKeys)
            else:
                self.symKeys[lineNum] = 'uu' + str(lineNum)
                self.userSyms[newVar] = \
                    self.userSyms.pop(self.symKeys[lineNum])
                self.userSyms[newVar] = self.symKeys[lineNum]
        elif (' to ' in newLine):
            # Conversion detected
            newLine, resUnit = self.convUnits(newLine)
            err = self.evalExp(newLine, lineNum)
            if (err == 0):
                self.resText[lineNum] += (' ' + resUnit)
        else:
            self.evalExp(newLine, lineNum)
        return

    def evalExp(self, newExp, lineNum):
        try:
            # if 1st symbol is an operator, implicittly insert 'ans'
            # TODO: fix negative sign on first line
            if newExp[0] in ['+', '*', '<<', '>>', '^', '&', '/', '=',
                          '%', '\|']:
                newExp = 'ans' + newExp
                #self.curText[lineNum] = newExp

            # Find and replace user-defined symbols with values
            # Also recognizes 'ans' and replaced with result from previous line
            for key in self.userSyms:
                if (lineNum > 0):
                    self.userSyms['ans'] = \
                        self.resText[lineNum-1].split(' ')[0]
                else:
                    self.userSyms['ans'] = 'None'
                newExp = re.sub(r'\b'+key+r'\b', self.userSyms[key], newExp)

            # scientific notations
            newExp = re.sub(r'((?<!\d)[.])', r'0.', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(p\b)', r'(\g<1>*10**-12)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(n\b)', r'(\g<1>*10**-9)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(u\b)', r'(\g<1>*10**-6)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(m\b)', r'(\g<1>*10**-3)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(k\b)', r'(\g<1>*10**3)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(M\b)', r'(\g<1>*10**6)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(G\b)', r'(\g<1>*10**9)', newExp)

            if (self.convXorToExp == 'True'):
                newExp = re.sub('\^', '**', newExp)

            newResult = eval(newExp)
            try:

                newResult = eng_string(newResult, self.sigFigs, '%s',
                                       self.resFormat)
            except:
                pass
            newResult = str(newResult)

            # Ignore python's "Built-in Function..." warning
            if ('function' not in newResult):
                self.resText[lineNum] = newResult
            else:
                self.resText[lineNum] = ''
            error = 0
        except:
            self.resText[lineNum] = ''
            error = 1
        return error

    def convUnits(self, newLine):
        newLine = newLine.split('to')
        convFrom = newLine[0]
        convTo = newLine[1]
        newUnit = ''
        try:
            # Special case for 'C to F' and 'F to C'
            if ((' C ' in convFrom) & (' F' in convTo)):
                convFrom = re.sub(r'\b' + 'C' + r'\b', '*1.8+32', convFrom)
                convTo = re.sub(r'\b' + 'F' + r'\b', '', convTo)
                newLine = convFrom + convTo
                newUnit = 'F'
                return newLine, newUnit
            elif ((' F ' in convFrom) & (' C' in convTo)):
                convFrom = re.sub(r'\b' + 'F' + r'\b', '/1.8-17.778', convFrom)
                convTo = re.sub(r'\b' + 'C' + r'\b', '', convTo)
                newLine = convFrom + convTo
                newUnit = 'C'
                return newLine, newUnit
            else:
                for unitType in self.units:
                    for unit in unitType:
                        convFrom = re.sub(r'\b' + unit + r'\b', '*' +
                                          unitType[unit], convFrom)
                        convTo = re.sub(r'\b' + unit + r'\b', '/' +
                                        unitType[unit], convTo)
                        if ((convTo != newLine[1]) & (newUnit == '')):
                            newUnit = unit
                    if (convFrom != newLine[0]) & (convTo != newLine[1]):
                        newLine = convFrom + convTo
                        return newLine, newUnit
                    else:
                        convFrom = newLine[0]
                        convTo = newLine[1]
        except:
            pass
        return newLine,newUnit

    def funcTriggered(self):
        trigFunc = self.sender()
        funcFullText = trigFunc.text()
        funcText = funcFullText.split(':')[0] + '('
        self.textEdit.insertPlainText(funcText)
        return

    def eeTriggered(self):
        eeFunc = self.sender()
        eeFullText = eeFunc.text()
        eeText = eeFullText.split(':')[0] + '('
        self.textEdit.insertPlainText(eeText)
        return

    def symTriggered(self):
        symFunc = self.sender()
        symFullText = symFunc.text()
        symText = symFullText.split(':')[0]
        self.textEdit.insertPlainText(symText)
        return

    def unitTriggered(self):
        unitFunc = self.sender()
        unitFullText = unitFunc.text()
        unitText = unitFullText.split(':')[0]
        self.textEdit.insertPlainText(unitText)
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

    def setSigFigs(self, digits):
        try:
            self.sigFigs = digits
            self.updateResults()
        except:
            pass
        return
