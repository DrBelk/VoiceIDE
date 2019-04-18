# -*- coding: utf-8 -*-
import sys
import os
import re

import WordHandler
import soundHandler
import threading
from constants import *

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from kivy.uix.codeinput import CodeInput
from pygments.lexers.c_cpp import CppLexer

from kivy.config import Config
Config.set('graphics', 'width', '250')
Config.set('graphics', 'height', '500')

class VoiceIDE(App):
    def __init__(self):
        self.wh = WordHandler.WordHandler()
        
        self.listen = False
        self.listener = threading.Thread(target=self.soundHandle)
        self.listener.start()
        self.code_out = CodeInput(lexer = CppLexer(), readonly = True)

        self.mic_button = Button(text='Включить микрофон')
        self.mic_button.bind(on_press = self.switchMic)

        # give init context representation
        self.code_out.text = self.wh.sendWord("")
        self.beauty_block = False
        return super().__init__()

    def build(self):
        v_layout = BoxLayout(orientation='vertical')
        g_layout = BoxLayout(spacing = 7, size_hint = [1, .15])
        g_layout.add_widget(self.mic_button)
        
        v_layout.add_widget(g_layout)
        v_layout.add_widget(self.code_out)
        self.input_line = TextInput(size_hint = [1, 0.2])
        self.input_line.text = PRE_TEXT
        self.input_line.bind(text = self.sendWordIfSpace_s)
        self.input_line.focus = True
        v_layout.add_widget(self.input_line)
        return v_layout

    def sendWordIfSpace_s(self, instance, value):
        if '  ' in value:
            to_process = ' '.join(value.lower().split('  ')[:-1])
            word_cmd_list = to_process.split()
            for word in word_cmd_list:
                self.code_out.text = self.wh.sendWord(word)
            self.input_line.unbind(text = self.sendWordIfSpace_s)
            self.input_line.text = value[len(to_process) + 2:]
            self.input_line.bind(text = self.sendWordIfSpace_s)

    def switchMic(self, instance):
        num = NUM
        with open("tests/text_based/" + str(num) + "/input.txt", "w") as text_file:
            text_file.write(PRE_TEXT)
        with open("tests/text_based/" + str(num) + "/output.txt", "w") as text_file:
            text_file.write(self.code_out.text)        
        return # TODO: kill me before release
        if not self.listen:
            instance.text = "Выключить микрофон"
            self.listen = True
        else:
            instance.text = "Включить микрофон"
            self.listen = False
            pass

    def soundHandle(self):
        l = soundHandler.Listener()
        while (True):
            while self.listen:
                word_cmd_list = l.listen()
                word_cmd_list = word_cmd_list.lower().split()
                for word in word_cmd_list:
                    print("Recognized: '%s'" % word)
                    self.code_out.text = self.wh.sendWord(word)

if __name__ == '__main__':
    VoiceIDE().run()
