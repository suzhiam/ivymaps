from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd

class windowManager(ScreenManager):
    pass

kv = Builder.load_file('login.kv')
sm = windowManager()
     
class PopupWindow(Widget):
    def btn(self):
        popFun()


class P(FloatLayout):
    pass


def popFun():
    show = P()
    window = Popup(title = "Invalid login", content = show,
                size_hint = (None, None), size = (300, 300))
    window.open()

class firstWindow(Screen):
    pass

class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def validate(self):
        if self.email.text not in users['Email'].unique():
            popFun()
        else:
            sm.current = 'logdata'
            self.email.text = ""
            self.pwd.text = ""


class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def signupbtn(self):
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]],
                            columns = ['Name', 'Email', 'Password'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
                user.to_csv('login.csv', mode = 'a', header = False, index = False)
                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
        else:
            popFun()

class logDataWindow(Screen):
    pass

class mapWindow(Screen):
    pass

users=pd.read_csv('login.csv')

sm.add_widget(firstWindow(name = 'First'))
sm.add_widget(loginWindow(name = 'Login'))
sm.add_widget(signupWindow(name = 'Signup'))
sm.add_widget(logDataWindow(name = 'Logdata'))
sm.add_widget(mapWindow(name = 'Map'))

class MainApp(App):
        def build(self):
                return kv

if __name__=="__main__":
    MainApp().run()