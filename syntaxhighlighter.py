from PyQt5.QtGui import QColor,QTextCharFormat,QFont,QSyntaxHighlighter
from PyQt5.QtCore import QRegExp

class KeywordHighlighter (QSyntaxHighlighter):

    def __init__(self, document,funcs,operators,syms,suffix,prefix,tweener,units):
        QSyntaxHighlighter.__init__(self, document)

        self.funcs = funcs
        self.operators = operators
        self.syms = syms
        self.suffix = suffix
        self.prefix = prefix
        self.units = units
        self.tweener = tweener

        self.styles =   {   'funcs': self.styleFormat('#7a9161', 'bold'),
                            'operators': self.styleFormat('#f2aa37'),
                            'userSyms': self.styleFormat('#b077d6', 'bold'),
                            'symbols': self.styleFormat('#d15152')}

        rules = []
        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, self.styles['funcs'])
            for w in self.funcs]
        rules += [(r'%s' % o, 0, self.styles['operators'])
            for o in self.operators]
        rules += [(r'\b%s\b' % x, 0, self.styles['symbols'])
                  for x in self.syms]
        rules += [(r'(\d)(%s\b)' % s, 2, self.styles['symbols'])
                  for s in self.suffix]
        rules += [(r'\b%s' % p, 0, self.styles['symbols'])
                  for p in self.prefix]
        rules += [(r'(\d)(%s)' % t, 2, self.styles['symbols'])
                  for t in self.tweener]
        rules += [(r'\b%s\b' % u, 0, self.styles['symbols'])
                  for u in self.units]

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

    def updateRules(self,userSyms):
        newRules = []
        # User symbol rules
        newRules += [(r'\b%s\b' % w, 0, self.styles['userSyms'])
                  for w in userSyms]
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