import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from ScriptMakingHelper import sentenceanager
from PyQt5 import uic
from PyQt5.QtCore import QEvent, QTimer
from PyQt5.QtWidgets import QApplication, QWidget

main_form_class = uic.loadUiType('Form.ui')[0]


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.sectionFormat = QtGui.QTextCharFormat()
        self.sectionFormat.setForeground(QtCore.Qt.blue)
        self.__highlight_line = 0

    def highlightBlock(self, text):
        if self.currentBlock().firstLineNumber() == self.__highlight_line:
            self.setFormat(0, len(text), self.sectionFormat)

    def set_highlight_line(self, value):
        self.__highlight_line = value


class MainWindow(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Script Maker")

        ############################
        # TODO
        self.filename = '__3_script.txt'

        ############################

        with open(self.filename, 'r', encoding='UTF8') as f:
            self.scripts = f.readlines()

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.highlighter = Highlighter(self.textEdit_script.document())

        self.manager = sentenceanager.SentenceManager()
        self.manager.set_script(''.join(self.scripts))

        self.set_script()

        #Callback & slot
        self.textEdit_script.textChanged.connect(self.textChanged)
        self.manager.current_line_changed = self.current_line_changed
        self.manager.sentence_changed = self.set_script

        # lineEdit
        self.lineEdits = {}
        self.lineEdits['1'] = self.lineEdit_1
        self.lineEdits['2'] = self.lineEdit_2
        self.lineEdits['3'] = self.lineEdit_3
        self.lineEdits['4'] = self.lineEdit_4
        self.lineEdits['5'] = self.lineEdit_5
        self.lineEdits['6'] = self.lineEdit_6
        self.lineEdits['7'] = self.lineEdit_7
        self.lineEdits['8'] = self.lineEdit_8
        self.lineEdits['9'] = self.lineEdit_9
        self.lineEdits['0'] = self.lineEdit_0
        self.lineEdits['q'] = self.lineEdit_q
        self.lineEdits['w'] = self.lineEdit_w
        self.lineEdits['e'] = self.lineEdit_e
        self.lineEdits['r'] = self.lineEdit_r
        self.lineEdits['t'] = self.lineEdit_t
        self.lineEdits['y'] = self.lineEdit_y
        self.lineEdits['u'] = self.lineEdit_u
        self.lineEdits['i'] = self.lineEdit_i
        self.lineEdits['o'] = self.lineEdit_o
        self.lineEdits['p'] = self.lineEdit_p

        # eventFilter
        self.installEventFilter(self)
        self.textEdit_script.installEventFilter(self)
        for key, lineEdit in self.lineEdits.items():
            lineEdit.installEventFilter(self)

        # commands
        self.commands = {}
        self.commands['a'] = lambda: self.manager.decrement()
        self.commands['d'] = lambda: self.manager.increment()
        self.commands['x'] = lambda: self.manager.erase_current_line()
        self.commands['c'] = lambda: self.manager.clean()
        for key, lineEdit in self.lineEdits.items():
            self.commands[key] = (lambda e: (lambda: self.manager.set_who_is_saying(e.text())))(lineEdit)

        try:
            with open('characters.txt', 'r') as f:
                lines = []
                for line in f.readlines():
                    lines.append(line)

                for line, kv in zip(lines, self.lineEdits.items()):
                    k, v = kv
                    v.setText(line.replace('\n', '', len(line)).replace('\r','', len(line)))
        except FileNotFoundError as e:
            pass

    def closeEvent(self, QCloseEvent):
        with open('characters.txt', 'w') as f:
            for key, lineEdit in self.lineEdits.items():
                f.write(lineEdit.text() + '\n')

        with open(self.filename, 'w', encoding='UTF8') as f:
            f.write(self.manager.sentences)

    ########################################
    # callback functions
    def textChanged(self):
        self.manager.set_script(self.textEdit_script.toPlainText())

    def keyPressEvent(self, p):
        t = p.text()
        try:
            self.commands[t]()
        except Exception as e:
            print(e)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self:
                self.label_focus_state.setText('@')
            else:
                self.label_focus_state.setText('')
        return super(MainWindow, self).eventFilter(obj, event)
    # callback functions
    ########################################

    def set_script(self):
        self.textEdit_script.setText(self.manager.sentences)

    def current_line_changed(self, n):
        self.highlighter.set_highlight_line(n)
        self.highlighter.rehighlight()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

