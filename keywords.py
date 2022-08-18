#################################################################
# Units
#################################################################

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

unitsList = [unitsLen, unitsVol, unitsMass, unitsForce]
unitKeys = lenKeys + volKeys + massKeys + forceKeys + tempKeys

#################################################################
# Functions and Symbols
#################################################################
# Supported functions and symbols
funcs = ['floor', 'ceil', 'sqrt', 'log', 'log10', 'log2', 'exp',
         'sin', 'cos', 'tan', 'abs', 'asin', 'acos', 'atan',
         'rad', 'deg', 'polar', 'rect', 'phase', 'cdf', 'pdf',
         'hex', 'bin', 'min', 'max', 'sum', 'bitget', 'a2h',
         'h2a', 'findres', 'findrdiv', 'rpar', 'vdiv']
operators = ['\+', '-', '\*', '<<', '>>', '\^', '\&', '/', '=',
             '%', '\|']
prefix = ['0x', '0b']
suffix = ['p', 'n', 'u', 'm', 'k', 'M', 'G']
tweener = ['e']
symbols = ['ans', 'pi', 'e']
unusual_syms = ['to']