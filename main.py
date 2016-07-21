#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from text_handling import *


class ZeroScreen(Screen):
    pass


class QuestionScreen(Screen):
    current_question = 0

    def on_enter(self, *args):
        if self.current_question == 0:
            TTS.speak(['Look at these pieces. Look at these pictures. If you put the pieces together, they will make one of the pictures. Press the picture the pieces make.'])
        else:
            TTS.speak(['Press the picture the pieces make.'])
        self.current_question += 1


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

        self.question_screen.ids['A_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question*2).zfill(2) + '_A.jpg'
        self.question_screen.ids['B_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question*2).zfill(2) + '_B.jpg'
        self.question_screen.ids['C_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question*2).zfill(2) + '_C.jpg'
        self.question_screen.ids['D_button'].background_normal = 'images/CMTT_A_Order1_Page_' + \
                                                                 str(self.current_question*2).zfill(2) + '_D.jpg'
        self.question_screen.ids['pieces'].source = 'images/CMTT_A_Order1_Page_' + \
                                                    str(self.current_question*2+1).zfill(2) + '.jpg'

        # because log goes after this, the name is changed to (real number - 1)
        self.question_screen.ids['A_button'].name = str(self.current_question-1) + '_A'
        self.question_screen.ids['B_button'].name = str(self.current_question-1) + '_B'
        self.question_screen.ids['C_button'].name = str(self.current_question-1) + '_C'
        self.question_screen.ids['D_button'].name = str(self.current_question-1) + '_D'

        self.sm.current = 'question_screen'

    def pressed(self, answer):
        print(answer)
        if self.current_question >= 32:
            self.end_game()

        self.next_question()

    def end_game(self):
        self.stop()

if __name__ == '__main__':
    MindsetAssessmentApp().run()
