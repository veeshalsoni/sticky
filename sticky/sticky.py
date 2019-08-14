import sys
from PySide import QtCore, QtGui
import os

windows = []
cur_dir = os.path.dirname(__file__)
backup_file = '.stickynotes-backup'
backup_progress = False

class Sticky(QtGui.QMainWindow):
	def __init__(self, on_create, on_close, on_delete, text=None, config=None):
		QtGui.QMainWindow.__init__(self)
		self.on_create = on_create
		self.on_close = on_close
		self.on_delete = on_delete
		self.text = text
		self.config = config
		self.deleted = False
		self.initUI()

	def initUI(self):
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

		if self.text:
			self.note.setText(self.text)

		if self.config:
			self.load_config(self.config)

		self.show()

	def addToolBarElements(self):
		self.bgcolor = QtGui.QAction("B", self)
		self.bgcolor.setToolTip("Background Color")
		self.bgcolor.triggered.connect(self.changeBgColor)

		self.textcolor = QtGui.QAction("F", self)
		self.textcolor.setToolTip("Text Color")
		self.textcolor.triggered.connect(self.changeTextColor)

		self.increasefont = QtGui.QAction("+", self)
		self.increasefont.setToolTip("Increase Text Size")
		self.increasefont.triggered.connect(self.increaseFontSize)

		self.decreasefont = QtGui.QAction("-", self)
		self.decreasefont.setToolTip("Decrease Text Size")
		self.decreasefont.triggered.connect(self.decreaseFontSize)

		self.newwindow = QtGui.QAction("N", self)
		self.newwindow.setToolTip("New Note")
		self.newwindow.triggered.connect(self.create_new_window)

		self.deleteWindow = QtGui.QAction("D", self)
		self.deleteWindow.setToolTip("Delete Note")
		self.deleteWindow.triggered.connect(self.delete_window)

		self.toolBar.addAction(self.bgcolor)
		self.toolBar.addAction(self.textcolor)
		self.toolBar.addAction(self.increasefont)
		self.toolBar.addAction(self.decreasefont)
		self.toolBar.addAction(self.newwindow)
		self.toolBar.addAction(self.deleteWindow)

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

	def closeEvent(self, event):
		self.on_close()

	def create_new_window(self):
		self.on_create()

	def delete_window(self):
		self.on_close = self.on_delete
		self.deleted = True
		self.close()

	def load_config(self, config):
		self.font.setPointSize(config['font']['size'])

		bg_color = QtGui.QColor.fromRgba(config['color']['bg_color'])
		fg_color = QtGui.QColor.fromRgba(config['color']['fg_color'])
		self.pal.setColor(QtGui.QPalette.Base, bg_color)
		self.pal.setColor(QtGui.QPalette.Text, fg_color)

		self.note.setFont(self.font)
		self.note.setPalette(self.pal)

	def get_current_text(self):
		return self.note.toPlainText()

	def get_current_config(self):
		config = {
			'color': {
				'bg_color': self.pal.color(QtGui.QPalette.Base).rgba(),
				'fg_color': self.pal.color(QtGui.QPalette.Text).rgba()
			},
			'font': {
				'size': self.font.pointSize()
			}
		}

		return config


def create_new_window(text=None, config=None):
	global windows
	w = Sticky(create_new_window, create_backup, delete_window, text, config)
	w.show()
	windows.append(w)


def create_backup():
	global windows
	global backup_progress
	if not len(windows) or backup_progress:
		return

	backup_progress = True
	backups = []
	for window in windows:
		window_text = window.get_current_text()
		if valid_note(window_text):
			window_config = window.get_current_config()
			backup = {
				'text': window_text,
				'config': window_config
			}

			backups.append(backup)

		window.close()

	windows = []
	if len(backups):
		save_backup(backups)

	backup_progress = False


def valid_note(window_text):
	if window_text == "" or not window_text:
		return False

	return True


def save_backup(backups):
	global cur_dir
	global backup_file

	_backup_file = os.path.join(cur_dir, backup_file)

	with open(_backup_file, "w") as f:
		f.write(str(backups))


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


def initiate_notes():
	global cur_dir
	global backup_file

	_backup_file = os.path.join(cur_dir, backup_file)

	if not os.path.exists(_backup_file):
		create_new_window()
		return

	with open(_backup_file, "r") as f:
		backups = f.readlines()

	import ast
	backup_list = ast.literal_eval(backups[0])
	for backup in backup_list:
		create_new_window(backup['text'], backup['config'])

	os.remove(backup_file)


def delete_window():
	global windows
	windows = [window for window in windows if not window.deleted]


def run():
	app = QtGui.QApplication(sys.argv)
	initiate_notes()
	sys.exit(app.exec_())
