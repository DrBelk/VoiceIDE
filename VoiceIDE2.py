# -*- coding: utf-8 -*-
import sys
import os
import re

import WordHandler
import soundHandler
import threading
from constants import *
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QTextEdit, QLineEdit)
from PyQt5.QtGui import (QStandardItemModel)
from PyQt5.QtGui import QFont	
from PyQt5.QtCore import Qt
		
class ActionHandler():
	"""This class keeps history and handles actions"""
	textedit = None
	statusBar = None
	
	def __init__(self, te, sb):
		self.textedit = te
		self.statusBar = sb
	
	def handle_actions(self, newText):
		self.textedit.setText(newText) # uptade text in the editor in any case

class Window(QWidget):
	"""Main VoiceIDE window"""
	wh = WordHandler.WordHandler()
	
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		QToolTip.setFont(QFont('SansSerif', 10))
		
		self.setToolTip('VoiceIDE')
		
		self.textedit = QTextEdit(self)
		self.textedit.resize(self.textedit.sizeHint())
		self.textedit.move(50, 50)
				
		self.lineedit = QLineEdit(self)
		self.lineedit.move(10, 10)
		self.lineedit.setText(PRE_TEXT)
		self.lineedit.textChanged.connect(self.sendWordIfSpace_s)
		
		self.statusview = QLineEdit(self)
		self.statusview.move(320, 50)
		
		self.ah = ActionHandler(self.textedit, self.statusview)
				
		self.setGeometry(200, 200, 600, 300)
		self.setWindowTitle('Tooltips')	
		self.lineedit.setFocus()
		self.show()
		
		listener = threading.Thread(target=self.soundHandle)
		#listener.start()
		
	def soundHandle(self):
		l = soundHandler.Listener()
		while (True):
			(word_name, word_cmd_list) = l.listen()
			word_cmd_list = word_cmd_list.lower().split()
			re.sub(' ', '_', word_name)
			print("Language: %s, recognized: %s" % ("ru-RU", word_cmd_list))
			print("Language: %s, recognized: '%s'" % ("en-US", word_name))
			for word in word_cmd_list:
				self.ah.handle_actions(self.wh.sendWord(word)) # redirect action array to action handler
		
	def sendWordIfSpace_s(self):
		if self.lineedit.text().endswith('  '):
			word_cmd_list = (self.lineedit.text()[:-1]).lower().split()
			print(word_cmd_list)
			for word in word_cmd_list:
				self.ah.handle_actions(self.wh.sendWord(word)) # redirect action array to action handler
			self.lineedit.clear()	
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Window()
	sys.exit(app.exec_())