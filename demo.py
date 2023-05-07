from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.datatables import MDDataTable
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy_garden.mapview import MapView
import pandas as pd
import requests


kv = Builder.load_file('login.kv')
users = pd.read_csv('login.csv')

class WindowManager(ScreenManager):
    pass

class P(MDBoxLayout):
    pass

def popFun():
    show = P()
    window = Popup(title = "Invalid login", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()

class ParentScreen(Screen):
    def __init__(self,**kwargs):
        super(ParentScreen,self).__init__(**kwargs)
        box1 = MDBoxLayout(orientation = 'vertical',
                           size_hint = (None, None),
                           spacing = 20,
                           pos_hint = {"center_x": .5, "center_y": .5})
        
        bg_image = Image(source='assets/logo.png',
                         opacity = 0.5,
                         allow_stretch = True,
                         keep_ratio = True)
        self.add_widget(bg_image)

        #Log in Button
        button1 = MDRaisedButton(text = "Log In",
                                size_hint = (1, 1),
                                line_color = "brown",
                                md_bg_color = "brown")
        button1.bind(on_press = self.loginScreen)
        box1.add_widget(button1)

        #Sign up Button
        button2 = MDRaisedButton(text = "Sign Up",
                                size_hint = (1, 1),
                                line_color = "brown",
                                md_bg_color = "brown")
        button2.bind(on_press = self.signupScreen)
        box1.add_widget(button2)

        #Guest User Button
        button3 = MDRaisedButton(text = "Guest User",
                                size_hint = (1, 1),
                                line_color = "brown",
                                md_bg_color = "brown")
        button3.bind(on_press = self.mainScreen)
        box1.add_widget(button3)

        self.add_widget(box1)

    #fucntions to switch screen
    def loginScreen(self, instance):
        print('this work')
        self.app = MDApp.get_running_app()
        self.app.psm.current = "login"

    def signupScreen(self, instance):
        print('this work')
        self.app = MDApp.get_running_app()
        self.app.psm.current = "signup"

    def mainScreen(self, instance):
        print('this work')
        self.app = MDApp.get_running_app()
        self.app.psm.current = "main"

class LoginScreen(Screen):
    def validate(self):
        if self.email.text not in users['Email'].unique():
            popFun()
        else:
            self.app = MDApp.get_running_app()
            self.app.psm.current = 'Logdata'
            self.email.text = ""
            self.pwd.text = ""

class SignupScreen(Screen):
    def signupbtn(self):
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]],
                            columns = ['Name', 'Email', 'Password'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
                user.to_csv('login.csv',
                            mode = 'a',
                            header = False,
                            index = False)
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""

                self.app = MDApp.get_running_app()
                self.app.psm.current = 'login'
                
        else:
            popFun()

class logDataWindow(Screen):
    pass

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super_box = MDBoxLayout(orientation = 'vertical')
        csm = ScreenManager()
        
        cs1 = ChildScreen1(name = "add")
        cs2 = ProfileScreen(name = "profile")
        cs3 = ViewScreen(name = "view")
        
        csm.add_widget(cs1)
        csm.add_widget(cs2)
        csm.add_widget(cs3)
        
        csm.current = "add"
        self.csm = csm

        #Add navigation buttons
        nav_drawer = MDNavigationDrawer()
        self.nav_drawer = nav_drawer
        
        nav_box = MDBoxLayout(orientation = 'vertical',
                              size_hint = (0.1, 0.9))
        
        nav_button1 = Button(text = "Profile")
        nav_button1.bind(on_press = self.nav_change_to_profile)
        
        nav_button2 = Button(text = "Add")
        nav_button2.bind(on_press = self.nav_change_to_add)
        
        nav_button3 = Button(text = "View")
        nav_button3.bind(on_press = self.nav_change_to_view)
        
        nav_box.add_widget(nav_button1)
        nav_box.add_widget(nav_button2)
        nav_box.add_widget(nav_button3)
        
        nav_drawer.add_widget(nav_box)
        
        self.add_widget(nav_drawer)

        #add navigation toolbar
        toolbar=MDTopAppBar(title="App Toolbar", size_hint = (1, 0.1))
        toolbar.left_action_items=[["arrow-left", lambda x: nav_drawer.set_state("open")]]

        super_box.add_widget(toolbar)
        super_box.add_widget(csm)
        self.add_widget(super_box)

    def nav_change_to_profile(self, instance):
        print('inside nav_change_screen1')
        self.csm.current="profile"

    def nav_change_to_add(self, instance):
        print('inside nav_change_profile')
        self.csm.current = "add"

    def nav_change_to_view(self, instance):
        print('inside nav_change_screen1')
        self.csm.current="view"

class ChildScreen1(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # Create a box layout for the UI
        layout = GridLayout(cols = 1,
                            orientation = 'lr-tb',
                            spacing = 10)
        layout2 = FloatLayout()
        # Create a text input for the user to enter a location
        self.location_input = TextInput(hint_text ='Enter location',
                                        size_hint_y = 0.25,
                                        height = 100,
                                        pos_hint = {"x": 0, "top": 1.0})

        # Create a button to search for the entered location
        search_button = MDRectangleFlatButton(text = 'Search',
                                size_hint_y = 0.25,
                                width = 100,
                               pos_hint = {"center_x": 0.25, "top": 0.8})
        search_button.bind(on_press=self.search_location)

        #Create text input for user to add information
        self.data_input = TextInput(hint_text = 'Enter information',
                                    size_hint_y = 0.25,
                                    height = 100,
                                    pos_hint = {"x": 0.5, "top": 1.0})
        
        # Create a button to add the entered location
        add_button = MDRectangleFlatButton(text='Add',
                            size_hint_y = 0.25,
                            width = 100,
                            pos_hint = {"center_x": 0.8, "top": 0.8})
        add_button.bind(on_press = self.add_location)

        # Create a MapView widget
        self.mapview = MapView(size_hint_y = None, height = 400, zoom=11, lat=37.7749, lon=-122.4194)

        layout2.add_widget(self.location_input)
        layout2.add_widget(search_button)
        layout2.add_widget(self.data_input)
        layout2.add_widget(add_button)
        layout.add_widget(layout2)
        layout.add_widget(self.mapview)
        self.add_widget(layout)

    def search_location(self, instance):
        # Get the location input from the user
        location = self.location_input.text

        # Use a geocoding API to convert the location to latitude and longitude coordinates
        url = 'https://nominatim.openstreetmap.org/search?q={}&format=json'.format(location)
        response = requests.get(url).json()
        if len(response) > 0:
            lat = float(response[0]['lat'])
            lon = float(response[0]['lon'])

            # Update the MapView widget to center on the searched location
            self.mapview.center_on(lat, lon)
    
    def add_location(self, instance):
        info = pd.DataFrame([[self.location_input.text, self.data_input.text]],
                            columns = ['Location', 'Data'])
        if self.data_input.text != "":
                info.to_csv('info.csv',
                            mode = 'a',
                            header = False,
                            index = False)
                self.location_input.text = ""
                self.data_input.text = ""
        else:
            show = P()
            window = Popup(title = "Invalid data", content = show,
                           size_hint = (None, None), size = (300, 300))
            window.open()

class ProfileScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        box2 = MDBoxLayout(orientation ='vertical')
        box2.add_widget(MDLabel(text = "User Information",
            pos_hint={'center_x':.95}))
        self.add_widget(box2)

class ViewScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        box1 = MDBoxLayout(orientation ='vertical')
        box1.add_widget(MDLabel(text = 'Information Table',
                                pos_hint = {'center_x': .95}))
#
        #table = MDDataTable(
        #    column_data = [('Location'),
        #                   ('Information')],
        #    #row_data = pd.read_csv('info.csv')
        #)
#
        #box1.add_widget(table)
        self.add_widget(box1)

class MainApp(MDApp):
    def build(self):
        Window.clearcolor = (1, 0.9, 0.9, 0.5)
        self.MainScreen = MainScreen()
        psm = ScreenManager()
        self.psm = psm

        ps1 = ParentScreen(name = "ps1")
        psm.add_widget(ps1)
        psm.add_widget(LoginScreen(name = 'login'))
        psm.add_widget(SignupScreen(name = 'signup'))
        psm.add_widget(MainScreen(name = "main"))
        psm.add_widget(logDataWindow(name = "Logdata"))

        psm.current = "ps1"
        print(psm.screens)
        print('self.dir::::', dir(self))
        return psm

MainApp().run()