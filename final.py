import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog, QFontDialog, QColorDialog
from PyQt5.QtGui import QTextCursor
import math
import XML_Editor
import ctypes
import copy
from PyQt5.QtPrintSupport import *
from PyQt5.uic import loadUiType
from prettify import *
from minify import *
from validator import *

XML_Editor, _ = loadUiType('XML_Editor.ui')


class MainApp(QMainWindow, XML_Editor):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui = XML_Editor
        font1 = QFont('Times', 12)
        self.editor.setFont(font1)
        self.path = ""
        self.setWindowTitle('XML Editor')
        self.menu_tool_bar()
        self.handle_buttons()

    global flag
    flag = 0

    def add_text(self, textadded):
        self.editor.selectAll()
        self.editor.cut()
        cursor = QTextCursor(self.editor.document())
        cursor.setPosition(0)
        self.editor.setTextCursor(cursor)
        self.editor.insertPlainText(textadded)

    def undo(self):
        self.editor.undo()
        if self.editor.toPlainText() == '':
            self.editor.undo()

    def redo(self):
        self.editor.redo()
        if self.editor.toPlainText() == '':
            self.editor.redo()

    # def creatnewwindow(self):
    #     dialog = MainApp()
    #     dialog.show()
    #     dialog.move(self.x() + 20, self.y() + 20)

    def menu_tool_bar(self):
        toolbar = QToolBar()

        self.actionNew.triggered.connect(self.file_new)
        toolbar.addAction(self.actionNew)

        self.actionOpen.triggered.connect(self.open_file)
        toolbar.addAction(self.actionOpen)

        toolbar.addAction(self.actionSave)
        self.actionSave.triggered.connect(self.saveFile)

        toolbar.addAction(self.actionSave_As)
        toolbar.addSeparator()
        self.actionSave_As.triggered.connect(self.file_saveas)

        toolbar.addAction(self.actionCopy)
        self.actionCopy.triggered.connect(self.editor.copy)

        toolbar.addAction(self.actionCut)
        self.actionCut.triggered.connect(self.editor.cut)

        toolbar.addAction(self.actionPaste)
        self.actionPaste.triggered.connect(self.editor.paste)

        toolbar.addAction(self.actionUndo)
        self.actionUndo.triggered.connect(self.undo)

        toolbar.addAction(self.actionRedo)
        self.actionRedo.triggered.connect(self.redo)
        toolbar.addSeparator()

        toolbar.addAction(self.actionFont)
        self.actionFont.triggered.connect(self.fontDialog)

        toolbar.addAction(self.actionColor)
        self.actionColor.triggered.connect(self.colorDialog)

        toolbar.addSeparator()

        toolbar.addAction(self.actionLeft)
        self.actionLeft.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))

        toolbar.addAction(self.actionCenter)
        self.actionCenter.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))

        toolbar.addAction(self.actionRight)
        self.actionRight.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        toolbar.addSeparator()

        toolbar.addAction(self.actionBold)
        self.actionBold.triggered.connect(self.boldText)

        toolbar.addAction(self.actionUnder_Line)
        self.actionUnder_Line.triggered.connect(self.underlineText)

        toolbar.addAction(self.actionItalic)
        self.actionItalic.triggered.connect(self.italicText)
        toolbar.addSeparator()

        self.actionExit.triggered.connect(self.close)

        # Check Errors
        self.action1.triggered.connect(self.op1)
        # Solve Errors
        self.action2.triggered.connect(self.op2)
        # Prettify
        self.action3.triggered.connect(self.op3)
        # Convert To JSON
        self.action4.triggered.connect(self.op4)
        # Minify
        self.action5.triggered.connect(self.op5)
        # Compress
        self.action6.triggered.connect(self.op6)

        self.addToolBar(toolbar)

    def italicText(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not state)

    def underlineText(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not state)

    def boldText(self):

        if self.editor.fontWeight() == QFont.Bold:

            self.editor.setFontWeight(QFont.Normal)

        else:

            self.editor.setFontWeight(QFont.Bold)

    def fontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.editor.setFont(font)

    def colorDialog(self):
        color = QColorDialog.getColor()
        self.editor.setTextColor(color)

    def saveFile(self):
        if self.path == '':
            self.file_saveas()
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)

    def file_saveas(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", self.path,
                                                   "XML File (*.xml);;Text files (*.txt);;JSON Files "
                                                   "(*.json);;All files (*.*)")
        if self.path == '':
            return
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()

        except Exception as e:
            print(e)

    def file_new(self):
        dialog = MainApp()
        global flag
        flag = flag + 1
        if flag == 1:
            dialog.close()
        dialog.show()
        dialog.move(self.x() + 20, self.y() + 20)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', "")

        if filename[0]:
            f = open(filename[0], 'r')

            with f:
                full_data = f.read()
                data = full_data[:1000]
                row = self.editor.toPlainText()
                if len(row) != 0:
                    dialog = MainApp()
                    global flag
                    flag = flag + 1
                    if flag == 1:
                        dialog.close()

                    dialog.show()
                    dialog.move(self.x() + 20, self.y() + 20)
                    dialog.editor.setText(data)
                else:
                    self.editor.setText(data)

    def closeEvent(self, event):
        global flag
        if flag == 1:
            event.accept()
            flag = flag+1
            print("flag")

        else:
            close = QMessageBox()
            close.setWindowTitle("Close")
            close.setText("Do you want to save changes to this file?\n")
            close.setIcon(QMessageBox.Question)
            close.setStandardButtons(QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel)
            close.setDefaultButton(QMessageBox.Save)
            close = close.exec_()

            if close == QMessageBox.Save:
                self.saveFile()
            elif close == QMessageBox.Close:
                event.accept()
            else:
                event.ignore()

    def handle_buttons(self):
        # Check Errors
        self.pushButton.clicked.connect(lambda: self.op1())
        # Solve Errors
        self.pushButton_2.clicked.connect(lambda: self.op2())
        # Prettify
        self.pushButton_3.clicked.connect(lambda: self.op3())
        # Convert To JSON
        self.pushButton_4.clicked.connect(lambda: self.op4())
        # Minify
        self.pushButton_5.clicked.connect(lambda: self.op5())
        # Compress
        self.pushButton_6.clicked.connect(lambda: self.op6())

    # Check Errors
    def op1(self):
        print("op1")
        self.add_text(error2(self.editor.toPlainText()))

    # Solve Errors
    def op2(self):
        print("op2")

    # Prettify
    def op3(self):
        print("op3")
        self.add_text(prettify_data(scrape_data(self.editor.toPlainText())))

    # Convert To JSON
    def op4(self):
        print("op4")

    # Minify
    def op5(self):
        print("op5")
        self.add_text(Minify(self.editor.toPlainText()))

    # Compress
    def op6(self):
        print("op6")


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    input()


if __name__ == '__main__':
    main()
