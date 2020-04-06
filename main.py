import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
import string
from ScriptMakingHelper import sentenceanager
from PyQt5 import uic
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QApplication, QWidget

main_form_class = uic.loadUiType('Form.ui')[0]


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.sectionFormat = QtGui.QTextCharFormat()
        self.sectionFormat.setForeground(QtCore.Qt.blue)
        self.errorFormat = QtGui.QTextCharFormat()
        self.errorFormat.setForeground(QtCore.Qt.red)

    def highlightBlock(self, text):
        if text.startswith('A'):
            self.setFormat(0, len(text), self.sectionFormat)
        # elif text.startswith('[ERROR]'):
        #     self.setFormat(0, len(text), self.errorFormat)


class MainWindow(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Script Maker")

        with open('__3_script.txt', 'r', encoding='UTF8') as f:
            self.scripts = f.readlines()

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.manager = sentenceanager.SentenceManager()
        self.manager.setscript(''.join(self.scripts))

        self.highlighter = Highlighter(self.textEdit_script.document())
        self.textEdit_script.setText(self.manager.sentences)

        #Callback & slot
        self.textEdit_script.textChanged.connect(self.textChanged)

        # lineEdit
        self.lineEdits = []
        self.lineEdits.append(self.lineEdit_1)
        self.lineEdits.append(self.lineEdit_2)
        self.lineEdits.append(self.lineEdit_3)
        self.lineEdits.append(self.lineEdit_4)
        self.lineEdits.append(self.lineEdit_5)
        self.lineEdits.append(self.lineEdit_6)
        self.lineEdits.append(self.lineEdit_7)
        self.lineEdits.append(self.lineEdit_8)
        self.lineEdits.append(self.lineEdit_9)
        self.lineEdits.append(self.lineEdit_0)
        self.lineEdits.append(self.lineEdit_q)
        self.lineEdits.append(self.lineEdit_w)
        self.lineEdits.append(self.lineEdit_e)
        self.lineEdits.append(self.lineEdit_r)
        self.lineEdits.append(self.lineEdit_t)
        self.lineEdits.append(self.lineEdit_y)
        self.lineEdits.append(self.lineEdit_u)
        self.lineEdits.append(self.lineEdit_i)
        self.lineEdits.append(self.lineEdit_o)
        self.lineEdits.append(self.lineEdit_p)

        # eventFilter
        self.installEventFilter(self)
        self.textEdit_script.installEventFilter(self)
        for lineEdit in self.lineEdits:
            lineEdit.installEventFilter(self)

    def textChanged(self):
        self.manager.setscript(self.textEdit_script.toPlainText())

    def keyPressEvent(self, p):
        print(p.key())

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self:
                self.label_focus_state.setText('@')
            else:
                self.label_focus_state.setText('')
        return super(MainWindow, self).eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

