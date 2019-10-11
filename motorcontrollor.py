import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from pidev.MixPanel import MixPanel
from kivy.app import App
from pidev.stepper import stepper
from kivy.lang import Builder
from time import sleep
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from kivy.uix import slider
MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)
SCREEN_MANAGER = ScreenManager()
EPIC_SCREEN = 'epic'
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

class EpicScreen(Screen):
    global x
    global dir
    global speed
    speed = 0
    dir = 0
    x = True
    def __init__(self, **kwargs):
        super(EpicScreen, self).__init__(**kwargs)
    def step(self):
        print("ayua")
        global x
        if(x == True):
            s0.run(dir, speed)
            self.ids.rie.text = "On"
            x = False
        else:
            print("freed")
            self.ids.rie.text = "Off"
            s0.softStop()
            x = True
    def direction(self):
        global dir
        global x
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
    def eee(self):
        global speed
        speed = self.ids.riseup.value
        if(x == False):
            self.step()
            self.step()
    def hardcoded(self):
        #self.ids.gamer.text = s0.get_position_in_units()
        s0.set_speed(1)
        s0.relative_move(15)
        # self.ids.gamer.text = s0.get_position_in_units()
        s0.stop()
        sleep(10)
        s0.set_speed(5)
        # self.ids.gamer.text = s0.get_position_in_units()
        s0.relative_move(10)
        s0.stop()
        sleep(8)
        # self.ids.gamer.text = s0.get_position_in_units()
        s0.goHome()
        sleep(30)
        # self.ids.gamer.text = s0.get_position_in_units()
        s0.set_speed(8)
        s0.relative_move(-100)
        s0.stop()
        # self.ids.gamer.text = s0.get_position_in_units()
        sleep(10)
        s0.goHome()
        # self.ids.gamer.text = s0.get_position_in_units()


Builder.load_file('EpicScreen.kv')
SCREEN_MANAGER.add_widget(EpicScreen(name = 'epic'))
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