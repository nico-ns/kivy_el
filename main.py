# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 11:11:46 2022

@author: nicos
"""

import requests
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ListProperty ,StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
# from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dropdownitem import MDDropDownItem
from datetime import datetime
import json
from functools import partial

def printlog(message):
    with open('./log.txt','a') as f: 
        f.write(str(message)+"\n")
        
class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        global USER
        payload = {"username": self.username.text, "password": self.password.text}
        r = requests.post("http://192.168.1.147:5056", data=payload)
        if r.status_code == 200:
            USER = self.username.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def reset(self):
        self.username.text = ""
        self.password.text = ""

class MainWindow(Screen):
    #Variable definition - Fields to be compiled by user and submitted for Activity registration
    #int_category = MDDropDownItem()    
    int_category = Spinner()
    int_hours = Spinner()
    int_minutes = Spinner()
    int_customer = Spinner()
    int_customer_text = ObjectProperty()
    int_ETA_hours = Spinner()
    int_ETA_minutes = Spinner()
    int_description = ObjectProperty()
    int_products = ObjectProperty()
    int_user1 = Spinner()
    int_user2 = Spinner()
    int_user3 = Spinner()

    
    #Variable definition - Fields to be compiled by user and submitted for Expense registration
    exp_brand = ObjectProperty()
    exp_model = ObjectProperty()
    exp_cost = ObjectProperty()
    exp_customer = Spinner()
    exp_quantity = ObjectProperty()
    exp_description = ObjectProperty()
    exp_customer_text = ObjectProperty()
    exp_customer = ObjectProperty()

    
    
    ELEMENTS_P = 6. #Number of elements per page
    ELEMENTS_T = 12. #Total number of elements (length of server response)    
    users = [] #Emplyees (obtained by querying the db)

    #Variable definition for main screen
    view = ObjectProperty(None)
    layout = GridLayout(cols=5, pos_hint={"top":0.9}, size_hint_y=(ELEMENTS_T*0.1 + 1))#, id="grid")
    

    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_inputs()
        
    def get_data_act(self):
        url = URL + "act"
        try:
            resp = requests.get(url, timeout=TIMEOUT)
            print(resp)
            display_data = json.loads(resp.text)
            self.fuck_on_enter(display_data)
        except:
            self.fuck_on_enter()
    
    def btn_get_data_act(self, instance):
        self.layout.clear_widgets()
        url = URL + "act"
        try:
            resp = requests.get(url, timeout=TIMEOUT)
            print(resp)
            display_data = json.loads(resp.text)
            self.fuck_on_enter(display_data)
        except:
            self.fuck_on_enter()
    
    def add_inputs(self):
        scrollview = ScrollView(size_hint=(1, 0.9), size=(Window.width, Window.height))
        scrollview.add_widget(self.layout)
        self.view.add_widget(scrollview)
        self.get_data_act()
    
    def btnAssign(self, *args):
        data = args[0]
        index = args[1]
        print(data)
        print(index)
        sm.current = "assign"
        self.manager.get_screen("assign").ids.details.text = str(data[index]["details"])
        self.manager.get_screen("assign").ids.ass_id.text = str(data[index]["id"])
    
    def fuck_on_enter(self, resp_d=[]):
        items_N = len(resp_d)
        if items_N>0:
            for i in range(len(resp_d)):
                
#                label = Label(text=f"{resp_d[i]['id']['Nome']}", color="#000000", size_hint_y=0.07, height=40)
                label2 = Label(text=f"{resp_d[i]['details']}", color="#000000", size_hint_x=0.57, height=40)
                label2.bind(width=lambda *x: label2.setter('text_size')(label2, (label2.width, None)),
                          texture_size=lambda *x: label2.setter('height')(label2, label2.texture_size[1]))
#                label3 = Label(text=f"{resp_d[i]['status']}", color="#000000", size_hint_y=0.07, height=40)
                label1 = Label(text="", size_hint_x=0)
                label3 = Label(text="", size_hint_x=0)
                
                self.manager.some_value.append(resp_d)
#                button = Button(text="Vedi dettagli", size_hint_y=None, text_size=(button.width, None), height=texture_size[1])
                button = Button(text="Vedi \ndettagli", size_hint_x=0.2, height=40)
                buttoncallback = partial(btnViewDetails, resp_d, i)
                button.bind(on_press=buttoncallback)
                
                button2 = Button(text="Assegna \nattività", size_hint_x=0.2, height=40)
                buttoncallback2 = partial(self.btnAssign, resp_d, i)
                button2.bind(on_press=buttoncallback2)
                
                
                self.layout.add_widget(label1)
                self.layout.add_widget(label3)
                self.layout.add_widget(label2)
                self.layout.add_widget(button)
                self.layout.add_widget(button2)
        else:
            label = Label(text="There is some problems connecting to the server\nPress the button to refresh", 
                            color="#000000", halign="center", valign="top")#, pos_hint=(0.5,0.7), size=(0.05, 0.1))
            button = Button(text="Refresh", halign="center", valign="middle")#, pos_hint=(0.5,0.65), size=(0.05, 0.05))
            button.bind(on_release=partial(self.btn_get_data_act))

            self.layout.add_widget(Label(text=""))
            self.layout.add_widget(Label(text=""))


            self.layout.add_widget(label)

            self.layout.add_widget(Label(text=""))
            self.layout.add_widget(Label(text=""))
            self.layout.add_widget(Label(text=""))
            self.layout.add_widget(Label(text=""))

            self.layout.add_widget(button)

            self.layout.add_widget(Label(text=""))
            self.layout.add_widget(Label(text=""))
            for i in range(15):
                self.layout.add_widget(Label(text=""))
                

    def get_date(self, date):
        printlog("get_date")
        printlog(date)
    
    def show_date_picker(self):
        
        date_dialog = MDDatePicker(
            callback=self.get_date,
            year=datetime.today().year,
            month=datetime.today().month,
            day=datetime.today().day,
        )
        date_dialog.bind(on_save=self.picked_date)
        date_dialog.open()
        
    def picked_date(self, instance, value, date_range):
        printlog("picked_date")
        printlog(instance, value, date_range)
    
    
    def drop(self):
        return ['Home', 'Work', 'Other', 'Custom']
    
    def drop_sector(self):
        print("THIS IS THE CENTRAL SCRUTINIZER")
        return '["manutenzioe ordinaria", "installazione", "manutenzione speciale", "cantiere"]'
    
    def drop_customers(self, flag: bool):
        if flag is True:
            return ["gesù", "al", "re artù"]
        else:
            self.ids.int_customer.values = ["bono", "fratone",
                                            self.ids.int_customer_text.text]

    def drop_team(self):
        return ["nick", "nich", "nico"]
    
        
    def actSubmitBtn(self):
        url = URL +"act"
        payload = {
            "int_category": self.int_category.text,
            "int_hours": self.int_hours.text,
            "int_minutes": self.int_minutes.text,
            "int_customer": self.int_customer.text,
            "int_customer_text": self.int_customer_text.text,
            "int_ETA_hours": self.int_ETA_hours.text,
            "int_ETA_minutes": self.int_ETA_minutes.text,
            "int_description": self.int_description.text,
            "int_products": self.int_products.text,
            "int_user1": self.int_user1.text,
            "int_user2": self.int_user2.text,
            "int_user3": self.int_user3.text,
        }
        printlog("ahahah THIS IS THE CENTRAL SCRUTINIZER")

        r = requests.post(url , json=payload)
        printlog(r)
        print(r)

        self.reset()
        sm.current = "submitted"

    def expSubmitBtn(self):
        url = URL +"act"
        payload = {
            "exp_brand": self.exp_brand.text,
            "exp_model": self.exp_model.text,
            "exp_cost": self.exp_cost.text,
            "exp_customer": self.exp_customer.text,
            "exp_quantity": self.exp_quantity.text,
            "exp_description": self.exp_description.text,
            "exp_customer_text": self.exp_customer_text.text,
            "exp_customer": self.exp_customer.text
        }
        printlog("ahahah THIS IS THE CENTRAL SCRUTINIZER")

        r = requests.post(url , json=payload)
        printlog(r)
        print(r)
        
        sm.current = "submitted"
        
    def reset(self):
        self.int_category.text = ""

        
class SubmittedWindow(Screen):
    k = ObjectProperty(None)
    # k.text = "bhbhbhbhbhb"

    def goBack(self):
        sm.current = "main"
        
class AssignmentWindow(Screen):
    ass_id = ObjectProperty(None)
    details = ObjectProperty(None)
    
    def get_data_ass(self):
        url = URL + "ass"
        try:
            req = requests.get(url, timeout=TIMEOUT)
            res = json.loads(req.text)
            print(res)
            users = res.values()
            return users
        except:
            return []
    
    def assign(self):
        url = URL + "ass"
        data = {"id": 1, "usr": ["gregorio", "andrea"]}
        r = requests.post(url , json=data, timeout=TIMEOUT)
        print(r)
        if r.status_code == 200:
            assignmentSuccessful()
        else:
            assignmentUnsuccessful()
        
    def goBack(self):
        sm.current = "main"

class WindowManager(ScreenManager):
    some_value = []
    pass

def invalidLogin():
    pop = Popup(title='Invalid Login', content=Label(
        text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()
    
def btnViewDetails(*args):
    data = args[0]
    index = args[1]
    # print(len(*args))
    pop = Popup(title="Details",
                content=Label(text=json.dumps(data[index], indent=4)),
                  size_hint=(None, None))#, size=(400, 400))

    pop.open()

        
def serverProblem():
    pop = Popup(title='Server Problem',
                  content=Label(text='There are some problems reaching the server.\nTry again later'),
                  
                  size_hint=(None, None), size=(400, 400))

    pop.open()
    
def assignmentSuccessful():
    pop = Popup(title='Server Problem',
                  content=Label(text='Assegnato con successo'),
                  
                  size_hint=(None, None), size=(400, 400))

    pop.open()

def assignmentUnsuccessful():
    pop = Popup(title='Server Problem',
                  content=Label(text='Assegnato senza successo\n Riprova'),
                  
                  size_hint=(None, None), size=(400, 400))

    pop.open()


class MyMainApp(MDApp):
    def build(self):
        self.root = Builder.load_file("my3.kv")
        
        screens = [AssignmentWindow(name="assign"), SubmittedWindow(name="submitted"),
                   MainWindow(name="main"), LoginWindow(name="login")]
        for screen in screens:
            sm.add_widget(screen)
        
        sm.current = "login"
        return sm
    
TIMEOUT = 2.5
USER = ""
#URL = "http://192.168.1.147:5056/"
URL = "http://spotapp.hopto.org:5056/"

sm = WindowManager()

if __name__ == "__main__":
    MyMainApp().run()