import sys
import os
import ctypes
import keywords
import toolButtons
from math import pi, log2, ceil, floor, e
from cmath import sqrt, sin, cos, tan, asin, acos, atan, exp, log, log10
from cmath import phase, polar, rect
from math import radians as rad
from math import degrees as deg
from scipy.stats import norm
from PySide2.QtWidgets import QTextEdit, QGridLayout, QWidget, QLabel
from PySide2.QtWidgets import QToolButton, QAction, QSplitter
from PySide2.QtGui import QPixmap, QIcon, QFont, QTextBlock
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
        self.funcs = keywords.funcs
        self.operators = keywords.operators
        self.prefix = keywords.prefix
        self.suffix = keywords.suffix
        self.tweener = keywords.tweener
        self.symbols = keywords.symbols
        self.unusual_syms = keywords.unusual_syms

        self.units = keywords.unitsList
        self.unitKeys = keywords.unitKeys

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
        self.resFormat = 'si'

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
        funcs = toolButtons.populateFuncButton(self.funcTool)
        for action in funcs:
            if (":" in action.text()):
                action.triggered.connect(self.funcTriggered)
            self.funcTool.addAction(action)
        self.funcTool.setPopupMode(QToolButton.InstantPopup)

        # EE Tool Button
        ees = toolButtons.populateEEButton(self.eeTool)
        for action in ees:
            if (":" in action.text()):
                action.triggered.connect(self.eeTriggered)
            self.eeTool.addAction(action)
        self.eeTool.setPopupMode(QToolButton.InstantPopup)

        # Symbols Tool Button
        syms = toolButtons.populateSymButton(self.symTool)
        for action in syms:
            if (":" in action.text()):
                action.triggered.connect(self.symTriggered)
            self.symTool.addAction(action)
        self.symTool.setPopupMode(QToolButton.InstantPopup)

        # Units Tool Button
        units = toolButtons.populateUnitButton(self.unitTool)
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
        #self.splitEdit.setStretchFactor(0, 1)  # better to leave editor/display same width
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
            else:
                newVar = 'uu' + str(lineNum)
                self.userSyms.pop(self.symKeys[lineNum])
                self.symKeys[lineNum] = newVar
                #self.userSyms[newVar] = \
                
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

            # Find and replace user-defined symbols with values
            # Also recognizes 'ans' and replaced with result from previous line
            for key in self.userSyms:
                if (lineNum > 0):
                    self.userSyms['ans'] = \
                        self.resText[lineNum-1].split(' ')[0]
                else:
                    self.userSyms['ans'] = 'None'
                newExp = re.sub(r'\b'+key+r'\b', ('('+self.userSyms[key]+')'), newExp)

            # scientific notations
            newExp = re.sub(r'((?<!\d)[.])', r'0.', newExp)
            #newExp = re.sub(r'(\d+[.,]?\d*)(y\b)', r'(\g<1>*10**-24)', newExp) # yocto
            #newExp = re.sub(r'(\d+[.,]?\d*)(z\b)', r'(\g<1>*10**-21)', newExp) # zepto
            #newExp = re.sub(r'(\d+[.,]?\d*)(a\b)', r'(\g<1>*10**-18)', newExp) # atto
            #newExp = re.sub(r'(\d+[.,]?\d*)(f\b)', r'(\g<1>*10**-15)', newExp) # femto
            newExp = re.sub(r'(\d+[.,]?\d*)(p\b)', r'(\g<1>*10**-12)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(n\b)', r'(\g<1>*10**-9)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(u\b)', r'(\g<1>*10**-6)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(m\b)', r'(\g<1>*10**-3)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(k\b)', r'(\g<1>*10**3)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(M\b)', r'(\g<1>*10**6)', newExp)
            newExp = re.sub(r'(\d+[.,]?\d*)(G\b)', r'(\g<1>*10**9)', newExp)
            #newExp = re.sub(r'(\d+[.,]?\d*)(T\b)', r'(\g<1>*10**12)', newExp) # tera
            #newExp = re.sub(r'(\d+[.,]?\d*)(P\b)', r'(\g<1>*10**15)', newExp) # Peta
            #newExp = re.sub(r'(\d+[.,]?\d*)(E\b)', r'(\g<1>*10**18)', newExp) # Exa
            #newExp = re.sub(r'(\d+[.,]?\d*)(Z\b)', r'(\g<1>*10**21)', newExp) # Zetta
            #newExp = re.sub(r'(\d+[.,]?\d*)(Y\b)', r'(\g<1>*10**24)', newExp) # Yotta

            if (self.convXorToExp == 'True'):
                newExp = re.sub('\^', '**', newExp)

            newExp = newExp.replace("cdf(", "norm.cdf(")
            newExp = newExp.replace("pdf(", "norm.pdf(")

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
        return

    def setSigFigs(self, digits):
        try:
            self.sigFigs = digits
            self.updateResults()
        except:
            pass
        return
