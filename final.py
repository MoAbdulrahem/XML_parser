import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog, QFontDialog, QColorDialog
import math
import XML_Editor
import ctypes
import copy
from PyQt5.QtPrintSupport import *
from PyQt5.uic import loadUiType
from prettify import *
from minify import *


XML_Editor, _ = loadUiType('XML_Editor.ui')


class MainApp(QMainWindow, XML_Editor):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui = XML_Editor
        # self.fontSizeBox = QSpinBox()
        font1 = QFont('Times', 12)
        self.editor.setFont(font1)
        self.path = ""
        self.setWindowTitle('XML Editor')
        self.menu_tool_bar()
        self.handle_buttons()

    def menu_tool_bar(self):
        toolbar = QToolBar()

        self.actionNew.triggered.connect(self.file_new)
        toolbar.addAction(self.actionNew)

        self.actionOpen.triggered.connect(self.open_file)
        toolbar.addAction(self.actionOpen)

        toolbar.addAction(self.actionSave)
        self.actionSave.triggered.connect(self.saveFile)

        # toolbar.addAction(self.actionSave_As)
        toolbar.addSeparator()
        self.actionSave_As.triggered.connect(self.file_saveas)

        toolbar.addAction(self.actionCopy)
        self.actionCopy.triggered.connect(self.editor.copy)

        toolbar.addAction(self.actionCut)
        self.actionCut.triggered.connect(self.editor.cut)

        toolbar.addAction(self.actionPaste)
        self.actionPaste.triggered.connect(self.editor.paste)

        toolbar.addAction(self.actionUndo)
        self.actionUndo.triggered.connect(self.editor.undo)

        toolbar.addAction(self.actionRedo)
        self.actionRedo.triggered.connect(self.editor.redo)
        toolbar.addSeparator()

        toolbar.addAction(self.actionFont)
        self.actionFont.triggered.connect(self.fontDialog)

        toolbar.addAction(self.actionColor)
        self.actionColor.triggered.connect(self.colorDialog)

        # self.fontBox = QComboBox(self)
        # self.fontBox.addItems(
        #     ["Courier Std", "Hellentic Typewriter Regular", "Helvetica", "Arial", "SansSerif", "Helvetica", "Times",
        #      "Monospace"])
        # self.fontBox.activated.connect(self.setFont)
        # toolbar.addWidget(self.fontBox)
        #
        # self.fontSizeBox.setValue(12)
        # self.fontSizeBox.valueChanged.connect(self.setFontSize)
        # toolbar.addWidget(self.fontSizeBox)
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

        # self.actionExit.triggered.connect(self.close)
        self.actionExit.triggered.connect(self.show_close_msg_box)

        self.action1.triggered.connect(self.op1)
        self.action2.triggered.connect(self.op2)
        self.action3.triggered.connect(self.op3)
        self.action4.triggered.connect(self.op4)
        self.action5.triggered.connect(self.op5)

        self.addToolBar(toolbar)

    # def setFontSize(self):
    #     value = self.fontSizeBox.value()
    #     self.editor.setFontPointSize(value)
    #
    # def setFont(self):
    #     font = self.fontBox.currentText()
    #     self.editor.setCurrentFont(QFont(font))

    def italicText(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not (state))

    def underlineText(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not (state))

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
        print(self.path)
        if self.path == '':
            self.file_saveas()
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
                print("save flag")
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

        msg = QMessageBox()
        msg.setWindowTitle("Save File")
        msg.setText("File Saved Successfully\n")
        s = msg.exec_()
        # self.saveFile()

    def file_new(self):
        dialog = MainApp()
        dialog.show()
        dialog.move(self.x() + 20, self.y() + 20)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', "")

        if filename[0]:
            f = open(filename[0], 'r')

            with f:
                # if len(self.editor.toPlainText()) > 1:
                dialog = MainApp()
                dialog.show()
                dialog.move(self.x() + 20, self.y() + 20)
                full_data = f.read()
                data = full_data[:1000]
                # data = f.read()
                dialog.editor.setText(data)

    def show_close_msg_box(self):
        msg = QMessageBox()
        msg.setWindowTitle("Close")
        msg.setText("Do you want to save changes to this file?\n")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Save)

        msg.buttonClicked.connect(self.handle_close_msg_box_buttons)

        x = msg.exec_()

    def handle_close_msg_box_buttons(self, i):
        x = i.text()
        if x == "Save":
            self.saveFile()
            self.close()
            # if flag != 0:
            #    self.close()
        elif x == "Close":
            self.close()

    # def closeEvent(self, event):
    #     x = event.text()
    #     if x == "Save":
    #         self.saveFile()
    #         # if flag != 0:
    #         #    event.accept()
    #     elif x == "Close":
    #         event.accept()
    #     else:
    #         event.ignore()

    # def msg_action_save(self):
    #     self.saveFile()
    #
    # def msg_action_close(self):
    #     self.close()

    # def closeEvent(self, *event, **ddd):
    #     print("fff")
    #
    #     reply = QMessageBox.Question(self, 'Window Close', 'Save Changes to this File?', QMessageBox.Save |
    #                                  QMessageBox.Yes, QMessageBox.Save)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    # msgbox = QMessageBox()
    # msgbox.setWindowTitle("Close")
    # msgbox.setText("Do you want to save changes to this file?\n")
    # savebtn = msgbox.addButton("Save", msgbox.YesRole)
    # Nobtn = msgbox.addButton(msgbox.No)
    # cancel_bttn = msgbox.addButton("       Cancel      ", msgbox.NoRole)
    # bttn = msgbox.exec_()
    # msgbox.close()
    # savebtn.clicked.connect(lambda: self.msg_action_save())
    # Nobtn.clicked.connect(lambda: self.msg_action_close())
    # print("gg")
    # self.saveFile()
    # event.ignore()

    # print("5")
    # event.acccept()
    # applyCompaction.clicked.connect(lambda: self.msg_action())
    # bttn = msgbox.exec_()
    # msgbox.close()

    def handle_buttons(self):
        self.pushButton.clicked.connect(lambda: self.op1())
        self.pushButton_2.clicked.connect(lambda: self.op2())
        # Prettify
        self.pushButton_3.clicked.connect(lambda: self.op3())
        self.pushButton_4.clicked.connect(lambda: self.op4())
        # Minify
        self.pushButton_5.clicked.connect(lambda: self.op5())

    def op1(self):
        print("op1")

    def op2(self):
        print("op2")

    def op3(self):
        print("op3")
        # prettify_data(scrape_data(self.editor.toPlainText()))
        self.editor.setText(prettify_data(scrape_data(self.editor.toPlainText())))

    def op4(self):
        print("op4")

    def op5(self):
        print("op5")
        self.editor.setText(Minify(self.editor.toPlainText()))




def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    input()


if __name__ == '__main__':
    main()
