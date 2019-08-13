import sys
from PySide import QtCore, QtGui
import os

class Sticky(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self)
		self.initUI()

	def initUI(self):
		self.backupfile = '.stickynotes-backup'
		self.configfile = '.stickynotes-config'
		self.cur_dir = os.path.dirname(__file__)

		self.note = QtGui.QTextEdit(self)
		self.pal = QtGui.QPalette()
		self.font = QtGui.QFont()
		self.font.setPointSize(15)
		self.note.setFont(self.font)
		self.others_windows = []

		self.setCentralWidget(self.note)
		self.setWindowTitle("Sticky")

		self.menu = self.menuBar()
		self.toolBar = self.addToolBar("Options")
		self.addToolBarBreak()
		self.addToolBarElements()
		self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'icons/main.png')))

		self.check_old_backups()
		old_config = self.get_old_config()
		if old_config:
			self.load_config(old_config)

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

		self.newwindow = QtGui.QAction(QtGui.QIcon(os.path.join(os.path.dirname(__file__),'icons/new.png')),"New Note",self)
		self.newwindow.setStatusTip("New Note")
		self.newwindow.triggered.connect(self.create_new_window)

		self.toolBar.addAction(self.bgcolor)
		self.toolBar.addAction(self.textcolor)
		self.toolBar.addAction(self.increasefont)
		self.toolBar.addAction(self.decreasefont)
		self.toolBar.addAction(self.newwindow)

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
		if self.note.toPlainText() == "" or not self.note.toPlainText():
			self.delete_backup_files()
			return

		self.create_backup()

	def create_new_window(self):
		w = Sticky()
		w.show()
		self.others_windows.append(w)

	def create_backup(self):
		backup_file = os.path.join(self.cur_dir, self.backupfile)
		with open(backup_file, "w") as f:
			f.write(self.note.toPlainText())

		self.save_current_config()

	def check_old_backups(self):
		backup_file = os.path.join(self.cur_dir, self.backupfile)
		if not os.path.exists(backup_file):
			return

		lines = []
		with open(backup_file, "r") as f:
			lines = f.readlines()

		self.note.setText("".join(lines))

	def save_current_config(self):
		config_file = os.path.join(self.cur_dir, self.configfile)
		config = {
			'color': {
				'bg_color': self.pal.color(QtGui.QPalette.Base).rgba(),
				'fg_color': self.pal.color(QtGui.QPalette.Text).rgba()
			},
			'font': {
				'size': self.font.pointSize()
			}
		}

		with open(config_file, "w") as f:
			f.write(str(config))

	def load_config(self, config):
		self.font.setPointSize(config['font']['size'])

		bg_color = QtGui.QColor.fromRgba(config['color']['bg_color'])
		fg_color = QtGui.QColor.fromRgba(config['color']['fg_color'])
		self.pal.setColor(QtGui.QPalette.Base, bg_color)
		self.pal.setColor(QtGui.QPalette.Text, fg_color)

		self.note.setFont(self.font)
		self.note.setPalette(self.pal)

	def get_old_config(self):
		config_file = os.path.join(self.cur_dir, self.configfile)
		if not os.path.exists(config_file):
			return

		with open(config_file, "r") as f:
			config = f.readlines()

		if config:
			import ast
			config = ast.literal_eval(config[0])
		return config

	def delete_backup_files(self):
		backup_file = os.path.join(self.cur_dir, self.backupfile)
		config_file = os.path.join(self.cur_dir, self.configfile)

		os.remove(backup_file)
		os.remove(config_file)


def run():
	app = QtGui.QApplication(sys.argv)
	notes = Sticky()
	sys.exit(app.exec_())
