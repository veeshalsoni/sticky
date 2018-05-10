import sys
from PySide import QtCore, QtGui 
import os
import sys

class Sticky(QtGui.QMainWindow):
    def __init__(self,parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.initUI()

    def initUI(self):
        self.note = QtGui.QTextEdit(self)
        self.pal = QtGui.QPalette()
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.note.setFont(self.font)

        self.setCentralWidget(self.note)
        self.setGeometry(30,30,300,300)
        self.setWindowTitle("Sticky")

        self.menu = self.menuBar()
        self.toolBar = self.addToolBar("Options")
        self.addToolBarBreak()
        self.addToolBarElements()

        self.show()

    def addToolBarElements(self):
		self.bgcolor = QtGui.QAction(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'icons/bgcolor.png')),"Change Background Color",self)
		self.bgcolor.setStatusTip("Background Color")
		self.bgcolor.triggered.connect(self.changeBgColor)

		self.textcolor = QtGui.QAction(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'icons/color.png')),"Select Text Color",self)
		self.textcolor.setStatusTip("Text Color")
		self.textcolor.triggered.connect(self.changeTextColor)

		self.increasefont = QtGui.QAction(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'icons/increase.png')),"Select Text Color",self)
		self.increasefont.setStatusTip("Text Color")
		self.increasefont.triggered.connect(self.increaseFontSize)

		self.decreasefont = QtGui.QAction(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'icons/decrease.png')),"Select Text Color",self)
		self.decreasefont.setStatusTip("Text Color")
		self.decreasefont.triggered.connect(self.decreaseFontSize)

		self.toolBar.addAction(self.bgcolor)
		self.toolBar.addAction(self.textcolor)
		self.toolBar.addAction(self.increasefont)
		self.toolBar.addAction(self.decreasefont)

    def changeBgColor(self):
        selectedcolor = QtGui.QColorDialog.getColor()
        if QtGui.QColor.isValid(selectedcolor):
        	self.pal.setColor(QtGui.QPalette.Base,selectedcolor)
        	self.note.setPalette(self.pal)

    def changeTextColor(self):
    	selectedcolor = QtGui.QColorDialog.getColor()
        if QtGui.QColor.isValid(selectedcolor):
        	self.pal.setColor(QtGui.QPalette.Text,selectedcolor)
        	self.note.setPalette(self.pal)

    def increaseFontSize(self):
    	current = self.note.currentFont().pointSize()
    	if current < 30:
			cursor = self.note.textCursor()
			self.note.selectAll()
			self.font.setPointSize(current+1)
			self.note.setFont(self.font)
			self.note.setTextCursor(cursor)

    def decreaseFontSize(self):
    	current = self.note.currentFont().pointSize()
    	if current > 1:
	    	cursor = self.note.textCursor()
	    	self.note.selectAll()
	    	self.font.setPointSize(current-1)
	        self.note.setFont(self.font)
	        self.note.setTextCursor(cursor)

    def closeEvent(self,event):
		reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()        		

def run():
    app = QtGui.QApplication(sys.argv)
    Journal = Sticky()
    sys.exit(app.exec_())