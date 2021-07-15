import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QFontDialog, QColorDialog
from PyQt5.QtGui import QTextCursor
import XML_Editor
from PyQt5.uic import loadUiType
from prettify import *
from minify import *
from consistancy import *
from compression import *
from xmltojson_v2 import *
from json_display import *

XML_Editor, _ = loadUiType('XML_Editor.ui')


################
class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parnet):
        super().__init__(parnet)
        self._highlight_lines = {}

    def highlight_line(self, line_num):
        fmt = QTextCharFormat()
        fmt.setBackground(QColor('blue'))
        if isinstance(line_num, int) and line_num >= 0 and isinstance(fmt, QTextCharFormat):
            self._highlight_lines[line_num] = fmt
            block = self.document().findBlockByLineNumber(line_num)
            self.rehighlightBlock(block)

    def clear_highlight(self):
        self._highlight_lines = {}
        self.rehighlight()

    def highlightBlock(self, text):
        blockNumber = self.currentBlock().blockNumber()
        fmt = self._highlight_lines.get(blockNumber)
        if fmt is not None:
            self.setFormat(0, len(text), fmt)


################
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
        self.highlighter = SyntaxHighlighter(self.editor)  ##############

    global flag
    flag = 0

    # def update_title(self):
    #     self.setWindowTitle(file_name[0])

    def add_text(self, textadded):
        self.editor.selectAll()
        self.editor.cut()
        cursor = QTextCursor(self.editor.document())
        cursor.setPosition(0)
        self.editor.setTextCursor(cursor)
        self.editor.insertPlainText(textadded)
        cursor.setPosition(0)

    def undo(self):
        self.editor.undo()
        self.highlighter.clear_highlight()
        if self.editor.toPlainText() == '':
            self.editor.undo()

    def redo(self):
        self.editor.redo()
        if self.editor.toPlainText() == '':
            self.editor.redo()


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
        # De_Compress
        self.actionDecompress.triggered.connect(self.op7)

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
            with open(self.path, 'w', encoding='utf-8') as f:
                f.write(text)
                s = QFileInfo(self.path).fileName()
                self.setWindowTitle(s)

        except Exception as e:

            print(e)

    def file_saveas(self):

        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "test",
                                                   "XML File (*.xml);;Text files (*.txt);;JSON Files "
                                                   "(*.json);;All files (*.*)")

        if self.path == '':
            return
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                f.write(text)
                s = QFileInfo(self.path).fileName()
                self.setWindowTitle(s)

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
        filename = QFileDialog.getOpenFileName(self, 'Open File', "test")

        if filename[0]:
            f = open(filename[0], 'r', encoding='utf-8')

            with f:
                full_data = f.read()
                data = full_data[:5000]
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
                    s = QFileInfo(filename[0]).fileName()
                    dialog.setWindowTitle(s)
                else:
                    self.editor.setText(data)
                    s = QFileInfo(filename[0]).fileName()
                    self.setWindowTitle(s)

    def closeEvent(self, event):
        global flag
        if flag == 1:
            event.accept()
            flag = flag + 1

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
        # De_Compress
        self.pushButton_7.clicked.connect(lambda: self.op7())

    def get_line_by_char(self, char_no):
        '''
        Takes a string and a number as input and determines the line number this character belongs to.
        '''
        counter = 0
        line = 0
        string = self.editor.toPlainText()
        for i in string.splitlines():
            if counter < char_no:
                counter += len(i)
                line += 1
        #    print( string.splitlines())
        return line

    # check error
    def op1(self):
        # self.highlighter.clear_highlight()
        if self.editor.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle("error")
            msg.setText("File is empty! \n")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        else:
            try:
                self.highlighter.clear_highlight()
                print("op1")
                # self.add_text(error2(self.editor.toPlainText()))
                x = self.get_line_by_char(503)
                self.highlighter.highlight_line(x - 1)
                msg = QMessageBox()
                msg.setWindowTitle("Detect Errors")
                msg.setText("Highlighted tags are not complete \n")
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()
            except:
                # msg = QMessageBox()
                # msg.setWindowTitle("error")
                # msg.setText("Input Error \n")
                # msg.setIcon(QMessageBox.Critical)
                # x = msg.exec_()
                print("op")

    # solve errors
    def op2(self):
        if self.editor.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle("error")
            msg.setText("File is empty! \n")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        else:
            try:
                print("op2")
                self.highlighter.clear_highlight()
                # self.add_text(prettify_data(scrape_data(self.editor.toPlainText())))
            except:
                msg = QMessageBox()
                msg.setWindowTitle("error")
                msg.setText("Input Error \n")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()

    # Prettify
    def op3(self):
        if self.editor.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle("error")
            msg.setText("File is empty! \n")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        else:
            try:
                print("op3")
                self.add_text(prettify_data(scrape_data(self.editor.toPlainText())))
                self.highlighter.clear_highlight()
            except:
                msg = QMessageBox()
                msg.setWindowTitle("error")
                msg.setText("Input Error \n")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()

    # Convert To JSON
    def op4(self):
        if self.editor.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle("error")
            msg.setText("File is empty! \n")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        else:
            try:
                print("op4")
                self.highlighter.clear_highlight()
                json_text = jsonify(scrape_data(self.editor.toPlainText()))
                self.add_text(display_json(json_text))
            except:
                msg = QMessageBox()
                msg.setWindowTitle("error")
                msg.setText("Input Error \n")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()

    # Minify
    def op5(self):
        if self.editor.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle("error")
            msg.setText("File is empty! \n")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        else:
            try:
                print("op5")
                self.highlighter.clear_highlight()
                self.add_text(Minify(self.editor.toPlainText()))
            except:
                msg = QMessageBox()
                msg.setWindowTitle("error")
                msg.setText("Input Error \n")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()

    # Compress
    def op6(self):
        if self.editor.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle("error")
            msg.setText("File is empty! \n")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        else:
            try:
                print("op6")
                self.highlighter.clear_highlight()
                # self.add_text(Minify(self.editor.toPlainText()))
                original_data = Minify(self.editor.toPlainText())
                # original_data = Minify("ABCDADADA")
                hashing_table = generate_hash_table(original_data)
                binary_stream = string_to_binary(original_data, hashing_table)
                encoded_text = encode(binary_stream)
                self.add_text(encoded_text)
                with open('hash-table.txt', 'w', encoding='utf-8') as f:
                    f.write(str(hashing_table))
            except:
                msg = QMessageBox()
                msg.setWindowTitle("error")
                msg.setText("Input Error \n")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()

    # De_Compress
    def op7(self):
        if self.editor.toPlainText() == '':
            msg = QMessageBox()
            msg.setWindowTitle("error")
            msg.setText("File is empty! \n")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        else:
            try:
                print("op7")
                self.highlighter.clear_highlight()
                with open('hash-table.txt', 'r', encoding='utf-8') as f:
                    string_hash_table = f.read()
                new_hash_table = eval(string_hash_table)
                # print(new_hash_table)
                decoded_string = decode(self.editor.toPlainText())
                # print (decoded_string)
                reconstructed_string = binary_to_string(decoded_string, new_hash_table)
                # reconstructed_string = prettify_data(reconstructed_string)
                # print(reconstructed_string)
                self.add_text(reconstructed_string)
                # self.add_text(prettify_data(scrape_data(self.editor.toPlainText())))
                with open('hash-table.txt', 'w', encoding='utf-8') as fs:
                    fs.write('')
            except:
                msg = QMessageBox()
                msg.setWindowTitle("error")
                msg.setText("Please Compress the file first \n")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    input()


if __name__ == '__main__':
    main()
