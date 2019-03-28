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

from kivy.uix.codeinput import CodeInput
from pygments.lexers.c_cpp import CppLexer

class VoiceIDE(App):
    def __init__(self):
        self.wh = WordHandler.WordHandler()
        
        listener = threading.Thread(target=self.soundHandle)
        self.code_out = CodeInput(lexer = CppLexer(), readonly = True)

        self.mic_button = Button(text='Включить микрофон')
        self.mic_button.bind(on_press = self.switchMic)

        # give init context representation
        self.code_out.text = self.wh.sendWord("")
        return super().__init__()

    def build(self):
        v_layout = BoxLayout(orientation='vertical')
        g_layout = BoxLayout(spacing = 7, size_hint = [1, .15])
        g_layout.add_widget(self.mic_button)
        
        v_layout.add_widget(g_layout)
        v_layout.add_widget(self.code_out)
        input_line = TextInput(size_hint = [1, 0.2])
        input_line.text = PRE_TEXT
        input_line.bind(text = self.sendWordIfSpace_s)
        input_line.focus = True
        v_layout.add_widget(input_line)
        return v_layout

    def sendWordIfSpace_s(self, instance, value):
        if value.endswith(' ' * 2):
            word_cmd_list = (value[:-1]).lower().split()
            print(word_cmd_list)
            for word in word_cmd_list:
                self.code_out.text = self.wh.sendWord(word)
            instance.text = ""

    def switchMic(self, instance):
        if instance.text == "Включить микрофон":
            instance.text = "Выключить микрофон"
            # listener on
            #listener.start()
        else:
            instance.text = "Включить микрофон"
            # listener off
            pass

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

if __name__ == '__main__':
    VoiceIDE().run()





