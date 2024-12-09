from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from re import findall


# class for scrollable label
class ScrollLabel(QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 70);")
        self.resize(300, 300)
        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)

        self.label = QLabel(content)
        self.label.setWordWrap(True)
        self.label.resize(300, 300)

        lay = QVBoxLayout(content)
        lay.addWidget(self.label)

    def setText_custom(self, text, chars_per_line=20):
        lines = findall(r'.{1,' + str(chars_per_line) + r'}', text)
        self.label.setText('\n'.join(lines))

    def setStyleSheet_custom(self, style_sheet):
        self.label.setStyleSheet(style_sheet)
