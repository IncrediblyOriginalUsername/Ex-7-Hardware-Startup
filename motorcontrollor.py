import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from pidev.MixPanel import MixPanel
import spidev
import os
import RPi.GPIO as GPIO
from pidev.kivy.PassCodeScreen import PassCodeScreen
from kivy.app import App
from pidev.stepper import stepper
from threading import Thread
from kivy.event import EventDispatcher
from kivy.lang import Builder
from time import sleep
from kivy.clock import Clock
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from kivy.uix import slider
MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)
SCREEN_MANAGER = ScreenManager()
EPIC_SCREEN = 'main'
ADMIN_SCREEN_NAME = 'admin'
spi = spidev.SpiDev()
global s0
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

class MainScreen(Screen):
    global x
    global dir
    global speed
    global b
    global onsetthing
    onsetthing = False
    b = False
    global a
    speed = 0
    dir = 0
    x = True
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
    def step(self):
        global x
        global s0
        if(onsetthing == False):
           # print("ayua")
            if(x == True):
                s0.run(dir, speed)
                self.ids.rie.text = "On"
                x = False
            else:
               # print("freed")
                self.ids.rie.text = "Off"
                s0.softFree()
                x = True
        else:
            self.ids.rie.text = "Motor locked during runthing"
    def direction(self):
        global dir
        global x
        if(onsetthing == False):
            if(dir == 0):
                dir = 1
                if(x == False):
                    self.step()
                    self.step()
            else:
                dir = 0
                if (x == False):
                    self.step()
                    self.step()
        else:
            self.ids.direction.text = "Direction change locked for duration of run thing"
    def cleanup(self):
        s0.free_all()
        spi.close()
        GPIO.cleanup()
        quit()
    def eee(self):
        global speed
        if(onsetthing == False):
            speed = self.ids.riseup.value
            if(x == False):
                self.step()
                self.step()
        else:
            self.ids.sped.text = "Speed changing locked during Runthing"
    def egg(self):
        global onsetthing
        global b
        print("%d" % s0.get_position_in_units())
        s0.stop()
        s0.set_speed(1)
        s0.relative_move(15)
        self.ids.game.text = "Location in units during runthing: %d" % s0.get_position_in_units()
        print("changed")
        s0.stop()
        sleep(10)
        s0.set_speed(5)
        s0.relative_move(10)
        self.ids.game.text = "Location in units during runthing: %d" % s0.get_position_in_units()
        print("changed")
        s0.stop()
        sleep(8)
        s0.goHome()
        while (s0.is_busy() == True):
            a = 1
        sleep(30)
        self.ids.game.text = "Location in units during runthing: %d" % s0.get_position_in_units()
        print("right before fast")
        s0.set_speed(8)
        s0.relative_move(-100)
        self.ids.game.text = "Location in units during runthing: %d" % s0.get_position_in_units()
        print("changed")
        s0.stop()
        sleep(10)
        print("should be 10 seconds here")
        s0.goHome()
        while(s0.is_busy() == True):
            a = 1
        self.ids.game.text = "Location in units during runthing: %d" % s0.get_position_in_units()
        print("done")
        onsetthing = False
        self.ids.runn.text = "Run thing"
        self.ids.sped.text = "Speed"
        self.ids.direction.text = "Change direction"
        if( x == True):
            self.ids.rie.text = "Off"
        else:
            self.ids.rie.text = "On"

    def hardcoded(self):
        global onsetthing
        if(onsetthing == False):
            self.ids.game.text = "Location in units during runthing: %d"% s0.get_position_in_units()
            Thread(target=self.egg).start()
            Thread.daemon = True
            onsetthing = True
        else:
            self.ids.runn.text = "Run thing cannot run again now"
    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'
class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(EPIC_SCREEN)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = EPIC_SCREEN

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        s0.free_all()
        spi.close()
        GPIO.cleanup()
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        s0.free_all()
        spi.close()
        GPIO.cleanup()
        quit()


        


Builder.load_file('EpicScreen.kv')
SCREEN_MANAGER.add_widget(MainScreen(name = 'main'))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()