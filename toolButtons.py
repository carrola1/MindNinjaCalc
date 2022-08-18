from PySide2.QtWidgets import QToolButton, QAction
from PySide2.QtGui import QFont


titleFont = QFont()
titleFont.setBold(True)
titleFont.setPixelSize(16)


# Function Tool Button
def populateFuncButton(funcTool: QToolButton):
    funcT0 = QAction('GENERAL MATH', funcTool)
    func0 = QAction('floor:  Round down', funcTool)
    func1 = QAction('ceil:   Round up', funcTool)
    func2 = QAction('min:    Return list min', funcTool)
    func3 = QAction('max:    Return list max', funcTool)
    func4 = QAction('sum:    Return list sum', funcTool)
    func5 = QAction('sqrt:   Square root', funcTool)
    func6 = QAction('abs:    Absolute value', funcTool)
    func7 = QAction('log:    Log base e', funcTool)
    func8 = QAction('log10:  Log base 10', funcTool)
    func9 = QAction('log2:   Log base 2', funcTool)
    func10 = QAction('exp:    Exponential (e**x)', funcTool)
    func11 = QAction('phase:  Phase of complex #', funcTool)
    func12 = QAction('rect:   Complex polar to rect (mag,ang)', funcTool)
    func13 = QAction('polar:  Complex rect to polar', funcTool)
    funcT1 = QAction('GEOMETRY', funcTool)
    func14 = QAction('sin:    Sine', funcTool)
    func15 = QAction('cos:    Cosine', funcTool)
    func16 = QAction('tan:    Tangent', funcTool)
    func17 = QAction('asin:   Arc-Sine', funcTool)
    func18 = QAction('acos:   Arc-Cosine', funcTool)
    func19 = QAction('atan:   Arc-Tangent', funcTool)
    func20 = QAction('rad:    Convert deg to rad', funcTool)
    func21 = QAction('deg:    Convert rad to deg', funcTool)
    funcT2 = QAction('PROBABILITY', funcTool)
    func22 = QAction('cdf:    Normal cumulative distribution (std_dev)', funcTool)
    func23 = QAction('pdf:    Normal probability distribution (std_dev)', funcTool)

    funcs = [funcT0, func0, func1, func2, func3, func4, func5, func6,
             func7, func8, func9, func10, func11, func12, func13, funcT1,
             func14, func15, func16, func17, func18, func19,
             func20, func21, funcT2, func22, func23]

    funcT0.setFont(titleFont)
    funcT1.setFont(titleFont)
    funcT2.setFont(titleFont)

    return funcs


# EE Tool Button
def populateEEButton(eeTool: QToolButton):
    eeT0 = QAction('ELECTRICAL', eeTool)
    ee0 = QAction('findres: Closest std value (target, tol)', eeTool)
    ee1 = QAction('vdiv: Calc voltage divider out (vin, R1, R2)', eeTool)
    ee2 = QAction('rpar: Parallel resistor calc (R1, R2, R3...)', eeTool)
    ee3 = QAction('findrdiv: Best R divider values (vin, vout, tol)', eeTool)
    eeT1 = QAction('PROGRAMMING', eeTool)
    ee4 = QAction('hex:    Convert to hex', eeTool)
    ee5 = QAction('bin:    Convert to bin', eeTool)
    ee6 = QAction('bitget: Bit slice (value,msb,lsb)', eeTool)
    ee7 = QAction('a2h:    Convert ASCII \'str\' to hex', eeTool)
    ee8 = QAction('h2a:    Convert hex to ASCII', eeTool)

    eeT0.setFont(titleFont)
    eeT1.setFont(titleFont)
    ees = [eeT0, ee0, ee1, ee2, ee3, eeT1, ee4, ee5, ee6, ee7, ee8]

    return ees


# Symbol Tool Button
def populateSymButton(symTool: QToolButton):
    symT0 = QAction('MISC', symTool)
    sym0 = QAction('ans:   Result from previous line', symTool)
    sym1 = QAction('to:    Unit conversion (ex. 5 mm to in)', symTool)
    symT1 = QAction('MATH', symTool)
    sym2 = QAction('**:    Power (ex. 2**3 = 8)', symTool)
    sym3 = QAction('%:     Modulus (ex. 5 % 2 = 1)', symTool)
    sym4 = QAction('e:     Exponent (ex. 5e-3 = 0.005)', symTool)
    symT2 = QAction('PROGRAMMING', symTool)
    sym5 = QAction('0x:    Hex (ex. 0x12 = 18)', symTool)
    sym6 = QAction('0b:    Binary (ex. 0b101 = 5)', symTool)
    sym7 = QAction('<<:    Shift left (ex. 2 << 2 = 8)', symTool)
    sym8 = QAction('>>:    Shift right (ex. 8 >> 2 = 2)', symTool)
    sym9 = QAction('|:     Bitwise OR (ex. 8 | 1 = 9)', symTool)
    sym10 = QAction('&&:     Bitwise AND (ex. 5 & 1 = 1)', symTool)
    sym11 = QAction('^:     Bitwise XOR (ex. 5 ^ 1 = 4)', symTool)
    symT3 = QAction('SCIENTIFIC NOTATION', symTool)
    sym12 = QAction('p:     Pico (ex. 1p = 1e-12)', symTool)
    sym13 = QAction('n:     Nano (ex. 1n = 1e-9)', symTool)
    sym14 = QAction('u:     Micro (ex. 1u = 1e-6)', symTool)
    sym15 = QAction('m:     Milli (ex. 1m = 1e-3)', symTool)
    sym16 = QAction('k:     Killo (ex. 1k = 1e3)', symTool)
    sym17 = QAction('M:     Mega (ex. 1M = 1e6)', symTool)
    sym18 = QAction('G:     Giga (ex. 1G = 1e9)', symTool)

    symT0.setFont(titleFont)
    symT1.setFont(titleFont)
    symT2.setFont(titleFont)
    symT3.setFont(titleFont)

    syms = [symT0, sym0, sym1, symT1, sym2, sym3, sym4, symT2, sym5, sym6,
            sym7, sym8, sym9, sym10, sym11, symT3, sym12, sym13, sym14,
            sym15, sym16, sym17, sym18]

    return syms


# Unit Tool Button
def populateUnitButton(unitTool: QToolButton):
    unitT0 = QAction('LENGTH', unitTool)
    unit0 = QAction('mm:    Millimeters', unitTool)
    unit1 = QAction('cm:    Centimeters', unitTool)
    unit2 = QAction('m:     Meters', unitTool)
    unit3 = QAction('km:    Killometers', unitTool)
    unit4 = QAction('mil:   Thousandths of an inch', unitTool)
    unit5 = QAction('in:    Inches', unitTool)
    unitT1 = QAction('VOLUME', unitTool)
    unit6 = QAction('mL:    Milliliter', unitTool)
    unit7 = QAction('L:     Liter', unitTool)
    unit8 = QAction('tsp:   Teaspoon', unitTool)
    unit9 = QAction('tbl:   Tablespoon', unitTool)
    unit10 = QAction('oz:    Fluid ounce', unitTool)
    unit11 = QAction('pt:    Pint', unitTool)
    unit12 = QAction('qt:    Quart', unitTool)
    unit13 = QAction('gal:   Gallon', unitTool)
    unitT2 = QAction('MASS', unitTool)
    unit14 = QAction('mg:    Milligram', unitTool)
    unit15 = QAction('g:     Gram', unitTool)
    unit16 = QAction('kg:    Killogram', unitTool)
    unit17 = QAction('oz:    Ounce', unitTool)
    unit18 = QAction('lbs:   Pound', unitTool)
    unitT3 = QAction('FORCE', unitTool)
    unit19 = QAction('N:     Newton', unitTool)
    unit20 = QAction('kN:    Killonewton', unitTool)
    unit21 = QAction('lbf:   Pound force', unitTool)
    unitT4 = QAction('TEMPERATURE', unitTool)
    unit22 = QAction('C:     Degrees celsius', unitTool)
    unit23 = QAction('F:     Degrees farenheit', unitTool)

    unitT0.setFont(titleFont)
    unitT1.setFont(titleFont)
    unitT2.setFont(titleFont)
    unitT3.setFont(titleFont)
    unitT4.setFont(titleFont)

    units = [unitT0, unit0, unit1, unit2, unit3, unit4, unit5, unitT1,
             unit6, unit7, unit8, unit9, unit10, unit11, unit12, unit13,
             unitT2, unit14, unit15, unit16, unit17, unit18, unitT3,
             unit19, unit20, unit21, unitT4, unit22, unit23]

    return units
