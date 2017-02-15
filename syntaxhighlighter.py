from PyQt5.QtGui import QColor,QTextCharFormat,QFont,QSyntaxHighlighter
from PyQt5.QtCore import QRegExp

class KeywordHighlighter (QSyntaxHighlighter):

    def __init__(self, document,keywords,operators):
        QSyntaxHighlighter.__init__(self, document)

        self.keywords = keywords
        self.operators = operators

        self.styles =   {   'keyword': self.styleFormat('#7a9161', 'bold'),
                            'operators': self.styleFormat('#f2aa37'),
                            'symbols': self.styleFormat('#b077d6', 'bold')}

        rules = []
        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, self.styles['keyword'])
            for w in self.keywords]
        rules += [(r'%s' % o, 0, self.styles['operators'])
            for o in self.operators]

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

    def updateRules(self,symbols):
        newRules = []
        # User symbol rules
        newRules += [(r'\b%s\b' % w, 0, self.styles['symbols'])
                  for w in symbols]
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