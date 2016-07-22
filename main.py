#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from text_handling import *
from kivy.graphics.context_instructions import (Color)
from kivy.graphics.vertex_instructions import (Ellipse)
from kivy.graphics import *
from kivy.core.window import Window
class ZeroScreen(Screen):
    pass


class QuestionScreen(Screen):
    current_question = 0

    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.init_circles()
        self.phrases_A = ['bla A 1',
                          'bla A 2',
                          'bla A 3',
                          'bla A 4',
                          'bla A 5',
                          'bla A 6',
                          'bla A 7',
                          'bla A 8']
        self.phrases_B = ['bla B 1',
                          'bla B 2',
                          'bla B 3',
                          'bla B 4',
                          'bla B 5',
                          'bla B 6',
                          'bla B 7',
                          'bla B 8']
        self.question = 'put text like to whom do you relate?'

    def on_enter(self, *args):
        if self.current_question == 0:
            TTS.speak(['Look at these pieces. Look at these pictures. If you put the pieces together, they will make one of the pictures. Press the picture the pieces make.'])
        else:
            TTS.speak(['Press the picture the pieces make.'])
        self.current_question += 1
 #       self.init_circles()

    def init_circles(self):

        self.g_right= InstructionGroup()
        self.g_right.add(Color(0,0,1,1))
        size = (Window.width * 0.1, Window.width * 0.1)
        pos = (Window.width*0.8- size[0]*0.5, Window.height*0.6 - size[1]*0.5)
        E_right = Ellipse(pos=pos, size=size)
        self.g_right.add(E_right)
  #      self.canvas.add(self.g_right)

        self.g_left= InstructionGroup()
        self.g_left.add(Color(0,1,0,1))
        size = (Window.width * 0.1, Window.width * 0.1)
        pos = (Window.width * 0.2 - size[0] * 0.5, Window.height * 0.6 - size[1] * 0.5)
        E_left = Ellipse(pos=pos, size=size)
        self.g_left.add(E_left)
 #       self.canvas.add(self.g_left)

 #       self.canvas.ask_update()

    def right_circle(self):
        self.canvas.remove(self.g_left)
        self.canvas.remove(self.g_right)
        self.canvas.add(self.g_right)
        self.canvas.ask_update()

    def left_circle(self):
        self.canvas.remove(self.g_left)
        self.canvas.remove(self.g_right)
        self.canvas.add(self.g_left)
        self.canvas.ask_update()

    def no_circles(self):
        self.canvas.remove(self.g_left)
        self.canvas.remove(self.g_right)
        self.canvas.ask_update()

    def first_phrase(self, current_question):
        print self.phrases_A[current_question - 1]
        TTS.speak(self.phrases_A[current_question - 1], TTS.finished)

    def second_phrase(self, current_question):
        print self.phrases_B[current_question - 1]
        TTS.speak(self.phrases_B[current_question - 1], TTS.finished)

    def question_phrase(self):
        print self.question
        TTS.speak(self.question, TTS.finished)

    def enable_buttons(self):
        print 'buttons enabled'
        self.ids['A_button'].disabled = False
        self.ids['B_button'].disabled = False



class MindsetAssessmentApp(App):

    current_question = 0

    def build(self):
        # initialize logger
        KL.start([DataMode.file, DataMode.communication, DataMode.ros], self.user_data_dir)
        KL.log.insert(action=LogAction.data, obj='app', comment='mindset_assessment_app')
        # KL.start([DataMode.file], "/sdcard/curiosity/")#self.user_data_dir)
        TTS.start()
        self.sm = ScreenManager()

        self.zero_screen = ZeroScreen(name='zero_screen')
        self.sm.add_widget(self.zero_screen)

        self.question_screen = QuestionScreen(name='question_screen')
        self.sm.add_widget(self.question_screen)

        self.sm.current = 'zero_screen'
        return self.sm

    def next_question(self):
        self.current_question += 1

        self.question_screen.ids['A_button'].disabled = True
        self.question_screen.ids['B_button'].disabled = True

        self.question_screen.ids['A_button'].name = str(self.current_question-1) + '_A'
        self.question_screen.ids['B_button'].name = str(self.current_question-1) + '_B'

        self.sm.current = 'question_screen'
        Clock.schedule_once(lambda dt: self.question_screen.right_circle(), 2)
        Clock.schedule_once(lambda dt: self.question_screen.first_phrase(self.current_question), 2)

        Clock.schedule_once(lambda dt: self.question_screen.left_circle(), 3)
        Clock.schedule_once(lambda dt: self.question_screen.second_phrase(self.current_question), 3)

        Clock.schedule_once(lambda dt: self.question_screen.no_circles(), 4)

        Clock.schedule_once(lambda dt: self.question_screen.question_phrase(), 5)
   #     TTS.speak(self.question_screen.question, TTS.finished)
   #     print ('next',self.question_screen.question)
        Clock.schedule_once(lambda dt: self.question_screen.enable_buttons(), 5)
        # self.question_screen.ids['A_button'].disabled = False
        # self.question_screen.ids['B_button'].disabled = False

    def pressed(self, answer):
        print(answer)
        if self.current_question >= 7:
            self.end_game()

        self.next_question()

    def end_game(self):
        self.stop()

if __name__ == '__main__':
    MindsetAssessmentApp().run()
