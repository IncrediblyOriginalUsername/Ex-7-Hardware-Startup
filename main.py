import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import spidev
import os
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
spi = spidev.SpiDev()
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
global servof
servof = True
cyprus.initialize()


#cyprus.setup_servo(1)

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


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    global x
    global x2
    x2 = False
    x = False
    global riseup
    riseup = 1
    def bs(self):
        global x
        while x:
            if(cyprus.read_gpio() & 0b0001):
                sleep(.1)
                if (cyprus.read_gpio() & 0b0001):
                    cyprus.set_servo_position(1, 0)
                    print("a")
            else:
                cyprus.set_servo_position(1, 1)
                print("f")
    def bs2(self):
        global x2
        while x2:
            if (cyprus.read_gpio() & 0b0001):
                sleep(.1)
                if (cyprus.read_gpio() & 0b0001):
                    cyprus.set_pwm_values(1, period_value=100000, compare_value=50000,
                                          compare_mode=cyprus.LESS_THAN_OR_EQUAL)
                    cyprus.set_servo_position(1, 1)
                    print("r")
            else:
                cyprus.set_servo_position(1, .5)
                print("b")
    def presseds(self):
        global x
        if(x == False):
            self.ids.MyNameIsYoshikageKira.text = "Toggle switch control: ON"
            x = True
            Thread(target=self.bs).start()
            Thread.daemon = True
        else:
            self.ids.MyNameIsYoshikageKira.text = "Toggle switch control: OFF"
            x = False
    def presseda(self):
        global x2
        if(x2 == False):
            self.ids.AAAA.text = "Toggle dc talon switch control: ON"
            x2 = True
            Thread(target=self.bs2).start()
            Thread.daemon = True
        else:
            self.ids.AAAA.text = "Toggle dc talon switch control: OFF"
            x2 = False
    def pressedF(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        cyprus.set_pwm_values(1, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        cyprus.set_servo_position(1, 0)
        sleep(5)
        print("a")
        cyprus.set_servo_position(1, .5)
        sleep(5)
        print("b")
        cyprus.set_pwm_values(1, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        cyprus.set_servo_position(1, 1)
        sleep(5)
        cyprus.set_servo_position(1, .5)
        print("c")
    def gamerrise(self):
        global b
        b = 1
        global speder
        speder = 0
        cyprus.set_servo_position(1,.5)
        while(b<=200):
            speder = .5 + .5 * b/200
            print("%s" % speder)
            cyprus.set_pwm_values(1, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            cyprus.set_servo_position(1, speder)
            sleep(.1)
            b = b + 1
    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        global riseup
        if(riseup == 1):
            cyprus.set_servo_position(1, 0)
            riseup = 0
            print("ad")
            # 2 specifies port P5, i is a float that specifies speed
        else:
            cyprus.set_servo_position(1, 1)
            riseup = 1
            print("af")


    def cleanup(self):
        cyprus.set_servo_position(1,.5)
        cyprus.close()
        spi.close()
        GPIO.cleanup()
        quit()
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
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


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
