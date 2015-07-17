"""
Threading test: runs tilt detection constantly in the background
prints heading every second
"""
import time
from threading import Thread as thread
import tiltcompass as tc


class Compassing():

    def __init__(self):
        self.navAGM = tc.NavioCompass()

        #starts thread
        tilt_thread = thread(target=self.navAGM.runcompass)

        #makes thread stop running when script does
        tilt_thread.isDaemon()

        #starts thread
        tilt_thread.start()

    def printdata(self):
        """
        prints bearing twice per second
        from same instance of NavioCompass class as the thread is running
        """
        while True:
            self.navAGM.printcompass()
            time.sleep(0.5)

a = Compassing()
a.printdata()
