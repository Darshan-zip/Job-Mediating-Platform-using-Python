import os
import tkinter as tk
from tkinter import filedialog
import connectivity_file
import Mail_functions
import mysql.connector
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager,Screen,SlideTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.clock import Clock
import threading
from functools import partial
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image as PILImage
from kivy.uix.image import AsyncImage
from kivy.clock import mainthread
import socketio
import threading
sio = socketio.Client()

inputs_jobseeker = []
inputs_recruiter = []
Data=["" for i in range(26)]
recruiter_record=[]
jobseeker_record=[]
otp=0
SQLpassword ="Darshan"  # CHANGE PASSWORD FOR SQL DATABASE HERE
current_username= ''
profile_pic_path='' 
profile_path = ''

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        bg_image = Image(source='Login_BG.png', size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg_image)
        user_portal_label = Label(text='USER PORTAL', font_size=60, bold=True, size_hint=(None, None), size=(200, 50), pos_hint={'right': 0.85, 'center_y': 0.65})
        layout.add_widget(user_portal_label)
        job_seeker_button = Button(text='Job Seeker',color = (0.8, 1.0, 0.0), size_hint=(None, None), size=(300, 50), pos_hint={'right': 0.875, 'center_y': 0.5}, on_press=self.open_job_seeker_login, bold=True)
        job_seeker_button.background_color = (0, 0, 1, 1) 
        layout.add_widget(job_seeker_button)
        recruiter_button = Button(text='Recruiter',color = (0.8, 1.0, 0.0), size_hint=(None, None), size=(300, 50), pos_hint={'right': 0.875, 'center_y': 0.4}, on_press=self.open_recruiter_login, bold=True)
        recruiter_button.background_color = (0, 0, 1, 1)  
        layout.add_widget(recruiter_button)      
        self.add_widget(layout)
    def open_job_seeker_login(self, instance):
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'job_seeker_login'
    def open_recruiter_login(self, instance):
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'recruiter_login'

""" MODULES RELATED TO JOB SEEKERS """

class JobSeekerLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(JobSeekerLoginScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        background = Image(source='JS_Login.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        self.box_layout = BoxLayout(orientation='horizontal', padding=(50, 0, 0, 0))
        layout = GridLayout(cols=1, padding=(0, 0, 0, 0))
        title_layout = GridLayout(cols=1, padding=(0,0,0,0))
        title_layout.add_widget(Label(text="JOB SEEKER LOGIN", bold=True, color=(0.8, 1.0, 0.0), font_size=50, height=250, size_hint_y=None))
        layout.add_widget(title_layout)
        username_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        username_layout.add_widget(Label(text="Enter username:", font_size=30, bold=True, size_hint_x=None, width=200))
        self.username_input = TextInput(hint_text='Username', size_hint_x=None, width=525, height=200,foreground_color=(1, 1, 1, 1), background_color=(0, 0, 0.5, 1))
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        password_layout.add_widget(Label(text="Enter password:", font_size=30, bold=True, size_hint_x=None, width=200))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525, height=200,foreground_color=(1, 1, 1, 1), background_color=(0, 0, 0.5, 1))
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        sub_grid_layout = GridLayout(cols=2, padding=(20, 10, 20, 10), spacing=(10, 15), size_hint=(None, None), size=(450, 80))
        sub_grid_layout.add_widget(Label(text="Forgot Password ?", bold=True, font_size=20))
        sub_grid_layout.add_widget(Button(text="Get OTP", bold=True, font_size=18, size=(190, 30), on_press=self.Get_OTP, background_color=(0, 0, 0.5, 1)))
        login_button_layout = BoxLayout(size_hint_y=None, height=100, padding=(20, 10, 20, 10))
        login_button = Button(text='Sign in', bold=True, size_hint=(None, None), size=(250, 50), on_press=self.login, background_color=(0, 0, 0.5, 1))
        login_button_layout.add_widget(login_button)
        layout.add_widget(login_button_layout)
        layout.add_widget(sub_grid_layout)
        button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='back', bold=True, size_hint=(None, None), size=(250, 50), background_color=(0, 0, 0.5, 1), pos_hint={'center_x': 0.8, 'center_y': 0.5}, on_press=self.back_page)
        button_layout.add_widget(back_button)
        sub_layout = GridLayout(cols=2, padding=(20, 10, 20, 10), spacing=(10, 15), size_hint=(None, None), size=(450, 80))
        sub_layout.add_widget(Label(text="Don't have an account ?", bold=True, font_size=20))
        sub_layout.add_widget(Button(text="Sign up", bold=True, font_size=18, on_press=self.register, background_color=(0, 0, 0.5, 1)))
        layout.add_widget(sub_layout)
        layout.add_widget(button_layout)
        self.box_layout.add_widget(layout)
        self.add_widget(self.box_layout)
    def on_leave(self, *args):
        if self.box_layout:
            self.remove_widget(self.box_layout)
            self.box_layout = None
    def Get_OTP(self, instance):
        self.manager.current = 'forgot_password_jobseeker'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'login'
    def login(self, instance):
        global current_username
        current_username = self.username_input.text
        username = self.username_input.text
        password = self.password_input.text
        if connectivity_file.check_existence_jobseeker(username) == 1:
            jobseeker_record.extend(connectivity_file.get_record(username))
            if password == connectivity_file.verify_password_jobseeker(username):
                self.show_success_popup()
                self.manager.transition = SlideTransition(direction ="left")
                self.manager.current = 'job_seeker_home_page'
    def show_success_popup(self):
        # Create the pop-up content
        popup_content = BoxLayout(orientation='vertical')
        message_label = Label(text="Logged in successfully")
        ok_button = Button(text="OK", size_hint_y=None, height=50)       
        # Add the label and button to the pop-up content
        popup_content.add_widget(message_label)
        popup_content.add_widget(ok_button)        
        # Create the pop-up
        popup = Popup(title="Success",
                      content=popup_content,
                      size_hint=(None, None), size=(300, 200),
                      auto_dismiss=False)
        ok_button.bind(on_release=popup.dismiss)
        popup.open()
    def register(self, instance):
        self.manager.current = 'register_part_1'

class ForgotPasswordJobSeeker(Screen):
    def __init__(self, **kwargs):
        super(ForgotPasswordJobSeeker, self).__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)       
        title_label = Label(text='Forgot Password ?', bold=True, color=(0.8, 1.0, 0.0), font_size=50, size_hint=(None, None), size=(400, 50), pos_hint={'center_x': 0.5, 'top': 0.9})
        layout.add_widget(title_label)       
        Email_layout = FloatLayout(size_hint=(None, None), size=(600, 200), pos_hint={'center_x': 0.5, 'top': 0.6})       
        email_label = Label(text="Enter Email ID:", font_size=30, bold=True, size_hint=(None, None), size=(200, 50), pos_hint={'x': 0, 'top': 1.5})
        Email_layout.add_widget(email_label)        
        self.Email_input = TextInput(hint_text='Email ID', size_hint=(None, None), size=(550, 80), pos_hint={'center_x': 0.45, 'top': 1}, background_color=(0.8, 0.85, 1.0, 1.0))
        Email_layout.add_widget(self.Email_input)  
        layout.add_widget(Email_layout) 
        self.message_label = Label(text="", size_hint=(None, None), bold=True, color=(0.8, 0.0, 0.0), size=(200, 50), pos_hint={'center_x': 0.3,'top':0.5}) 
        layout.add_widget(self.message_label) 
        OTP_layout = FloatLayout(size_hint=(None, None), size=(600, 200), pos_hint={'center_x': 0.475, 'top': 0.5})           
        get_otp_button = Button(text="Get OTP", color=(0.8, 1.0, 0.0), bold=True, font_size=23, size_hint=(None, None), size=(175, 50), pos_hint={'center_x': 0.75, 'top': 1},on_press=self.send_OTP)
        OTP_layout.add_widget(get_otp_button)  
        getotp_label = Label(text="Enter OTP:", font_size=30, bold=True, size_hint=(None, None), size=(200, 50), pos_hint={'x': 0, 'top': 0.6})
        OTP_layout.add_widget(getotp_label)        
        self.OTP_input = TextInput(hint_text='OTP', size_hint=(None, None), size=(250, 65), pos_hint={'center_x': 0.25, 'top': 0.3}, background_color=(0.8, 0.85, 1.0, 1.0))
        OTP_layout.add_widget(self.OTP_input)     
        layout.add_widget(OTP_layout) 
        verify_button = Button(text = "Verify", color=(0.8,1.0,0.0),bold = True,font_size = 23,size_hint = (None,None),size = (175,50),pos_hint = {'center_x' :0.55,'top': 0.3255},on_press = self.verify)
        layout.add_widget(verify_button)  
        back_button = Button(text = 'Back',bold = True,color=(0.8,1.0,0.0),font_size = 23,size_hint = (None,None),size = (175,50),pos_hint = {'center_x':0.315,'top': 0.2},on_press = self.back_page) 
        layout.add_widget(back_button)   
        self.add_widget(layout)       
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size  
    def send_OTP(self, instance):
        self.message_label.text = "OTP sent"
        instance.text = "Resend OTP" 
        global otp
        otp=otp+Mail_functions.send_otp(self.Email_input.text)
        
    def verify(self,instance):
        global otp
        self.OTP=self.OTP_input.text
        if int(self.OTP)==otp:
            self.manager.current = 'change_password_jobseeker'
    def back_page(self, instance):
        self.manager.current = 'job_seeker_login'

class RegisterScreenPart1(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreenPart1, self).__init__(**kwargs)
        self.fields = [
            ("PERSONAL DETAILS", Label(text=" ", font_size=20)),
            ("Name:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Age:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Date of Birth:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("ADDRESS FOR COMMUNICATION", Label(text=" ", font_size=20)),
            ("Door No. & Residence Name:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Street:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Area:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("District:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("City:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("State:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Pincode:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0)))
        ]
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text='REGISTER',bold=True, font_size=50, size_hint=(None, None), size=(200, 50),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},color = (0.8, 1.0, 0.0))
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        form_layout = GridLayout(cols=2, spacing=10)
        for label, widget in self.fields:
            if label == "ADDRESS FOR COMMUNICATION" or label == "PERSONAL DETAILS":
                label_widget = Label(text=label,bold = True, font_size=23, color=(1, 0, 1, 1))
                form_layout.add_widget(label_widget)
            else:
                form_layout.add_widget(Label(text=label,bold = True, font_size=23))
            form_layout.add_widget(widget)
        layout.add_widget(form_layout)
        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='Next',bold = True, size_hint=(None, None), size=(250, 75),
                             pos_hint={'center_x': 0.75, 'center_y': 0.5},color = (0.8, 1.0, 0.0),background_color=(0.9, 0.95, 1.0, 1.0), on_press=self.next_page)
        back_button = Button(text='Back',bold = True, size_hint=(None, None), size=(250, 75),
                             pos_hint={'center_x': 0.25, 'center_y': 0.5},color = (0.8, 1.0, 0.0),background_color=(0.9, 0.95, 1.0, 1.0),on_press=self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(button_layout)
        self.add_widget(layout)
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next_page(self, instance):
        input_values = []
        for label, widget in self.fields:
            if isinstance(widget, TextInput):
                input_values.append(widget.text)
        for value in input_values:
            inputs_jobseeker.append(value)
            print(value)
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'register_part_2'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'login'

class RegisterScreenPart2(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreenPart2, self).__init__(**kwargs)
        self.fields_page_2 = [
            ("Educational Qualification:", TextInput(multiline=True,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Email:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Mobile No.:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Nationality:", TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Previous Experience:", TextInput(background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Years of Experience:", TextInput(background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Salary Obtained:", TextInput(background_color=(0.8, 0.85, 1.0, 1.0))),
            ("Salary Expected:", TextInput(background_color=(0.8, 0.85, 1.0, 1.0)))
        ]       
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text='REGISTER',bold = True,font_size=50, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5},color = (0.8, 1.0, 0.0))
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)       
        form_layout = GridLayout(cols=2, spacing=10)
        for label, widget in self.fields_page_2:
            form_layout.add_widget(Label(text=label,bold = True,font_size=23))
            form_layout.add_widget(widget)
        layout.add_widget(form_layout)       
        button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='Back',bold = True, size_hint=(None, None), size=(250, 75),color = (0.8, 1.0, 0.0),pos_hint={'center_x': 0.25, 'center_y': 0.5},background_color=(0.9, 0.95, 1.0, 1.0), on_press=self.back_page)
        next_button = Button(text='Next',bold = True, size_hint=(None, None), size=(250, 75),color = (0.8, 1.0, 0.0), pos_hint={'center_x': 0.75, 'center_y': 0.5},background_color=(0.9, 0.95, 1.0, 1.0), on_press=self.next_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(button_layout)         
        self.add_widget(layout)      
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next_page(self, instance):
        input_values = []
        for label, widget in self.fields_page_2:
            if isinstance(widget, TextInput):
                input_values.append(widget.text)
        for value in input_values:
            inputs_jobseeker.append(value)
            print(value)
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'register_part_3'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'register_part_1'

class RegisterScreenPart3(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreenPart3, self).__init__(**kwargs)
        self.additional_skills = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.projects_handled = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.certifications = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.reference = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.convenient_mode = ""
        self.job_style = ""
        self.profile_picture_path = TextInput(multiline=False, readonly=True, background_color=(0.8, 0.85, 1.0, 1.0))
        
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text='REGISTER', bold=True, color=(0.8, 1.0, 0.0), font_size=50, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        
        form_layout = GridLayout(cols=2, spacing=10)
        dropdown_fields = [
            ("Convenient Mode of Working ", ["Online", "Offline", "Both"]),
            ("Job Style ", ["Part-time", "Full-time"])
        ]
        self.dropdowns = {}
        for label, options in dropdown_fields:
            dropdown = self.build_dropdown_content(options)
            dropdown_button = Button(text='-Select-', color=(0.8, 1.0, 0.0), bold=True, size_hint=(None, None), size=(100, 44), background_color=(0.8, 0.85, 1.0, 1.0))
            dropdown_button.bind(on_release=lambda btn, dropdown=dropdown: dropdown.open(btn))
            dropdown.bind(on_select=lambda instance, x, button=dropdown_button, label=label: self.on_dropdown_select(label, x, button))
            form_layout.add_widget(Label(text=label, font_size=23, bold=True))
            form_layout.add_widget(dropdown_button)
            self.dropdowns[label] = dropdown 
        
        # Add Profile Picture field and Choose button
        form_layout.add_widget(Label(text="Profile Picture:", font_size=23, bold=True))
        form_layout.add_widget(self.profile_picture_path)
        form_layout.add_widget(Label(text = " "))
        choose_picture_button = Button(text='Choose', bold=True, color=(0.8, 1.0, 0.0), size_hint=(None, None), size=(200, 45), background_color=(0.8, 0.85, 1.0, 1.0), on_press=self.choose_profile_picture)
        form_layout.add_widget(choose_picture_button)
        
        fields = [
            ("Additional Skills:", self.additional_skills),
            ("Projects Handled:", self.projects_handled),
            ("Certifications:", self.certifications),
            ("Reference:", self.reference)
        ]
        
        for label, widget in fields:
            form_layout.add_widget(Label(text=label, bold=True, font_size=23))
            form_layout.add_widget(widget)
        
        layout.add_widget(form_layout)
        
        button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='Back', bold=True, color=(0.8, 1.0, 0.0), size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5}, background_color=(0.9, 0.95, 1.0, 1.0), on_press=self.back_page)
        register_button = Button(text='Register', bold=True, color=(0.8, 1.0, 0.0), size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5}, background_color=(0.9, 0.95, 1.0, 1.0), on_press=self.register)
        
        button_layout.add_widget(back_button)
        button_layout.add_widget(register_button)
        
        layout.add_widget(button_layout)
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def build_dropdown_content(self, options):
        dropdown = DropDown()
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, option=option, dropdown=dropdown: dropdown.select(option))
            dropdown.add_widget(btn)
        return dropdown
    
    def on_dropdown_select(self, label, value, button):
        button.text = value 
        if label == "Convenient Mode of Working ":
            self.convenient_mode = value
        elif label == "Job Style ":
            self.job_style = value
    
    def choose_profile_picture(self, instance):
        try:
            # Create a temporary Tk root to hide the main window
            root = tk.Tk()
            root.withdraw()
            
            # Open file dialog to select image file
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
            
            if file_path:
                self.profile_picture_path.text = file_path
                global profile_pic_path
                profile_pic_path = file_path
        except Exception as e:
            print(f"Error: {e}")
    
    def register(self, instance):
        inputs_jobseeker.extend([self.convenient_mode, self.job_style, self.additional_skills.text, self.projects_handled.text, self.certifications.text, self.reference.text])
        print("Convenient Mode:", self.convenient_mode)
        print("Job Style:", self.job_style)
        print("Additional Skills:", self.additional_skills.text)
        print("Projects Handled:", self.projects_handled.text)
        print("Certifications:", self.certifications.text)
        print("Reference:", self.reference.text)
        
        # Adjust the input list as needed
        inputs_jobseeker[1] = int(inputs_jobseeker[1])
        inputs_jobseeker[3] = inputs_jobseeker[3] + ',' + inputs_jobseeker[4] + ',' + inputs_jobseeker[5] + ',' + inputs_jobseeker[6] + ',' + inputs_jobseeker[7] + ',' + inputs_jobseeker[8] + ',' + inputs_jobseeker[9]
        del inputs_jobseeker[4:10]
        
        print(inputs_jobseeker)
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'Username_jobseeker'
    
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'register_part_2'

class UsernamePasswordJobSeeker(Screen):
    def __init__(self, **kwargs):
        super(UsernamePasswordJobSeeker, self).__init__(**kwargs)
        background = Image(source='UP_Jobseeker.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        box_layout = BoxLayout(orientation='horizontal', padding=(50, 0, 0, 0))
        layout = GridLayout(cols=1, padding=(50, 0, 0, 0))  
        title_layout = GridLayout(cols=1, padding=(0,0,0,0))
        title_layout.add_widget(Label(text="CREATE USERNAME AND PASSWORD",bold = True,color = (0.8, 1.0, 0.0),font_size = 50,height = 250,size_hint_y=None))
        layout.add_widget(title_layout)
        username_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        username_layout.add_widget(Label(text="Create Username:",font_size = 30,bold=True,size_hint_x=None, width=200))
        self.username_input = TextInput(hint_text='Username',size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0)) 
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        password_layout.add_widget(Label(text="Create Password:",font_size = 30,bold = True, size_hint_x=None,width=200))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0))
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        confirm_password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        confirm_password_layout.add_widget(Label(text="Confirm Password:",font_size = 30,bold = True, size_hint_x=None, width=200))
        self.confirm_password = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200,background_color=(0.8, 0.85, 1.0, 1.0))  
        confirm_password_layout.add_widget(self.confirm_password)
        layout.add_widget(confirm_password_layout)
        self.message_label = Label(size_hint=(None, None),bold = True,color = (0.8, 0.0, 0.0), size=(200, 50), pos_hint={'center_x': 0.5})  
        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='confirm',bold = True,size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5},on_press = self.check_passwords)
        back_button = Button(text='Back',bold = True, size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5},on_press = self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(self.message_label)
        layout.add_widget(button_layout) 
        self.add_widget(layout)
    def check_passwords(self, instance):
        if self.password_input.text != self.confirm_password.text:
            self.message_label.text = "Passwords do not match"
        else:
            self.message_label.text = ""
            username = self.username_input.text
            password = self.password_input.text
            inputs_jobseeker.extend([username,password])
            connectivity_file.jobseeker_insert(inputs_jobseeker,profile_pic_path)
            print(inputs_jobseeker)
            self.manager.transition = SlideTransition(direction ="left")
            self.manager.current = 'job_seeker_login'
    def back_page(self,instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'register_part_3'

class ChangePasswordJobseeker(Screen):
    def __init__(self, **kwargs):
        super(ChangePasswordJobseeker, self).__init__(**kwargs)
        background = Image(source='UP_Jobseeker.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        box_layout = BoxLayout(orientation='horizontal', padding=(50, 0, 0, 0))
        layout = GridLayout(cols=1, padding=(50, 0, 0, 0))  
        title_layout = GridLayout(cols=1, padding=(0,0,0,0))
        title_layout.add_widget(Label(text="CHANGE PASSWORD",bold = True,color = (0.8, 1.0, 0.0),font_size = 50,height = 250,size_hint_y=None))
        layout.add_widget(title_layout)
        username_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        username_layout.add_widget(Label(text="Enter Username:",font_size = 30,bold=True,size_hint_x=None, width=200))
        self.username_input = TextInput(hint_text='Username',size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0)) 
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        password_layout.add_widget(Label(text="New Password:",font_size = 30,bold = True, size_hint_x=None,width=200))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0))
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        confirm_password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        confirm_password_layout.add_widget(Label(text="Confirm Password:",font_size = 30,bold = True, size_hint_x=None, width=200))
        self.confirm_password = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200,background_color=(0.8, 0.85, 1.0, 1.0))  
        confirm_password_layout.add_widget(self.confirm_password)
        layout.add_widget(confirm_password_layout)
        self.message_label = Label(size_hint=(None, None),bold = True,color = (0.8, 0.0, 0.0), size=(200, 50), pos_hint={'center_x': 0.5})  
        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='confirm',bold = True,size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5},on_press = self.check_passwords)
        back_button = Button(text='Back',bold = True, size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5},on_press = self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(self.message_label)
        layout.add_widget(button_layout) 
        self.add_widget(layout)
    def check_passwords(self, instance):
        if self.password_input.text != self.confirm_password.text:
            self.message_label.text = "Passwords do not match"
        else:
            self.message_label.text = ""
            username = self.username_input.text
            password = self.password_input.text
            connectivity_file.change_password_jobseeker(username,password)
            self.manager.transition = SlideTransition(direction ="left")
            self.manager.current = 'job_seeker_login'
    def back_page(self,instance):
            self.manager.transition = SlideTransition(direction ="right")
            self.manager.current = 'forgot_password_jobseeker'

class JobSeeker_Recommendations_Card(FloatLayout):
    def __init__(self, home_screen, username="Name", rec_perc="__", profile_picture="", **kwargs):
        super(JobSeeker_Recommendations_Card, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 180  # Increase the height of the card
        with self.canvas.before:
            Color(0.2, 0.7, 0.9, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)    
        self.bind(size=self._update_rect, pos=self._update_rect)
        # Profile Picture
        self.profile_picture = AsyncImage(source=profile_picture, size_hint=(None, None), size=(100, 85), pos_hint={'center_x': 0.1, 'center_y': 0.5})
        self.add_widget(self.profile_picture)
        # Name Label
        name_label = Label(text=f"{username}", size_hint=(None, None), bold=True, size=(120, 50), pos_hint={'x': 0.04, 'y': 0.02}, valign='bottom', color=(0, 0, 0, 1))
        self.add_widget(name_label)
        match_per = Label(text=f"{rec_perc}%", bold=True,font_size=50,size_hint=(None, None), size=(60, 50), pos_hint={'right': 0.625, 'top': 0.6}, valign='middle', color=(0, 0.5, 0, 1))
        self.add_widget(match_per)
        # Matches Label
        matches_label = Label(text=f"Requirements Matched", bold=True, size_hint=(None, None), size=(300, 50), pos_hint={'right': 0.925, 'top': 0.8}, valign='middle', color=(0, 0, 0, 1))
        self.add_widget(matches_label)
        # View Profile Button
        view_profile_button = Button(text="View Profile",color=(0.57, 1, 0.57, 1), size_hint=(None, None),bold=True, size=(175, 50), pos_hint={'right': 0.875, 'top': 0.4},background_color=(0.53, 0.81, 0.92, 1))
        view_profile_button.bind(on_press=lambda instance: self._view_profile(home_screen, username))
        self.add_widget(view_profile_button)
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size    
    def _view_profile(self, home_screen, username):
        L = connectivity_file.get_record_recruiter(username)
        date_obj = L[1]
        date_str = date_obj.strftime('%D')
        L[1] = date_str
        for i in range(len(L)):
            Data[i] = L[i]
        print("Data:", Data)
        recruiter_record.extend(Data)
        home_screen.manager.transition = SlideTransition(direction="left")
        home_screen.manager.current = 'recruiter_resume_1'
        home_screen.manager.get_screen('recruiter_resume_1').clear_widgets()
        home_screen.manager.get_screen('recruiter_resume_1').disp_resume(Data[0], Data[1], Data[2], Data[3], Data[4], Data[5], Data[6], Data[7], Data[8], Data[9], Data[25],Data[11],Data[12],Data[13],Data[14],Data[15],Data[16],Data[17],Data[18],Data[19],Data[20],Data[21])

class JobSeeker_RecommendationsPage(ScrollView):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        scroll_layout = GridLayout(cols=1, 
                                   spacing=10, 
                                   size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        scroll_layout.add_widget(Label(text=" "))
        scroll_layout.add_widget(Label(text=" "))
        scroll_layout.add_widget(Label(text="RECOMMENDATIONS",bold = True,color=(1, 0, 0, 1)))
        scroll_layout.add_widget(Label(text=" "))
        connectivity_file.count_set0_recruiter()
        L=connectivity_file.get_reccommended_recruiters(jobseeker_record[18])

        for _name, _perc in L:
            x=connectivity_file.get_record_recruiter(_name)
     
            scroll_layout.add_widget(JobSeeker_Recommendations_Card(home_screen=home_screen, username = _name,rec_perc =round((_perc/6)*100,2),profile_picture=x[25]))

        self.add_widget(scroll_layout)

'''class JobSeeker_SearchPage(ScrollView):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.home_screen = home_screen
        
        # Search input
        self.search_input = TextInput(hint_text="Enter username to be searched", 
                                      multiline=False, 
                                      size_hint=(0.8, 0.1), 
                                      pos_hint={'x': 0.1, 'y': 0.9})
        self.layout.add_widget(self.search_input)
        
        # Search button
        search_button = Button(text="Search", 
                               size_hint=(0.2, 0.1), 
                               background_color=(0.53, 0.81, 0.92, 1),
                               pos_hint={'x': 0.4, 'y': 0.6})
        search_button.bind(on_press=lambda instance: self.search(self.search_input.text))
        
        # Spinner for Age
        age_spinner = Spinner(
            text='Select Working hours',
            values=('0-2', '2-4', '4-6', '6-8', '8-10'),
            background_color=(0.53, 0.81, 0.92, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.8})
        self.layout.add_widget(age_spinner)

        # Spinner for Expected Salary
        salary_spinner = Spinner(
            text='Expected Salary',
            values=('₹0-₹30000', '₹30000-₹50000', '₹50000-₹70000', '₹70000-₹100000', '₹100000-₹150000'),
            bold = True,
            background_color=(0.53, 0.81, 0.92, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.8})
        self.layout.add_widget(salary_spinner)

        # Spinner for Mode of Working
        mode_spinner = Spinner(
            text='Mode of Working',
            values=('Offline', 'Online', 'Both'),
            bold = True,
            size_hint=(0.4, 0.1),
            background_color=(0.53, 0.81, 0.92, 1),
            pos_hint={'x': 0.1, 'y': 0.7})
        self.layout.add_widget(mode_spinner)

        # Spinner for Job Style
        job_style_spinner = Spinner(
            text='Job Style',
            values=('Full-time', 'Part-time'),
            bold = True,
            size_hint=(0.4, 0.1),
            background_color=(0.53, 0.81, 0.92, 1),
            pos_hint={'x': 0.5, 'y': 0.7})
        self.layout.add_widget(job_style_spinner)

        self.layout.add_widget(search_button)

    def search(self, username):
        pass'''

class JobSeeker_SearchPage(ScrollView):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.home_screen = home_screen
        
        self.search_input = TextInput(hint_text="Enter username to be searched", 
                                      multiline=False, 
                                      size_hint=(0.8, 0.1), 
                                      pos_hint={'x': 0.1, 'y': 0.9})
        self.layout.add_widget(self.search_input)
        
        search_button = Button(text="Search", 
                               size_hint=(0.2, 0.1), 
                               pos_hint={'x': 0.4, 'y': 0.8},
                               background_color = (0.53, 0.81, 0.92, 1))
        search_button.bind(on_press=self.on_search_button_pressed)
        self.layout.add_widget(search_button)
        
        self.age_spinner = Spinner(
            text='Select Working Hours',
            values=('0-2','2-4','4-6','6-8','8-10'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.7},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.age_spinner)

        self.salary_spinner = Spinner(
            text='Expected Salary',
            values=('₹0-₹30000', '₹30000-₹50000', '₹50000-₹70000', '₹70000-₹100000', '₹100000-₹150000'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.7},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.salary_spinner)

        self.mode_spinner = Spinner(
            text='Mode of Working',
            values=('Offline', 'Online', 'Both'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.6},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.mode_spinner)

        self.job_style_spinner = Spinner(
            text='Job Style',
            values=('Full-time', 'Part-time'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.6},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.job_style_spinner)

    def on_search_button_pressed(self, instance):
        self.search(home_screen=self.home_screen, 
                    textEntered=self.search_input.text, 
                    age=self.age_spinner.text, 
                    salary=self.salary_spinner.text, 
                    mode=self.mode_spinner.text, 
                    job_style=self.job_style_spinner.text)

    def search(self, home_screen, textEntered, age, salary, mode, job_style):
        home_screen.manager.current = 'jobseeker_searchresults'
        search_results_screen = home_screen.manager.get_screen('jobseeker_searchresults')
        search_results_screen.home_screen = home_screen
        search_results_screen.textEntered = textEntered
        search_results_screen.age = age
        search_results_screen.salary = salary
        search_results_screen.mode = mode
        search_results_screen.job_style = job_style

class JobSeeker_SearchResults(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.home_screen = None
        self.layout = ''
        self.textEntered = ''
        self.age=''
        self.salary=''
        self.mode=''
        self.jobstyle=''
        
    def on_enter(self):
        self.layout = GridLayout(cols=1, 
                                   spacing=10, 
                                   size_hint_y=None)
        self.button_layout = FloatLayout()
        self.layout.bind(minimum_height=self.layout.setter('height'))
        print("PRINTINTG:",self.textEntered,self.salary,self.mode,self.age,self.jobstyle)
        L=connectivity_file.search_recruiters_byfilter(self.textEntered,self.salary,self.mode,self.age,self.jobstyle)
        for _name, _perc,path in L:
            self.layout.add_widget(JobSeeker_Recommendations_Card(home_screen=self.home_screen, username = _name,rec_perc = round((_perc/6)*100,2),profile_picture=path ) )
        back_button = Button(text='<--',bold = True,size_hint=(None, None),
                             size=(250, 50),background_color=(0, 0, 0.5, 1), 
                             pos_hint={'center_x': 0.1, 'center_y': 0.925},
                             on_press = self.back_page)
        self.button_layout.add_widget(back_button)
        self.add_widget(self.layout) 
        self.add_widget(self.button_layout) 

    def on_leave(self, *args):
        self.remove_widget(self.layout)
        self.remove_widget(self.button_layout)
        self.layout = None

    def back_page(self,instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current='job_seeker_home_page'

class JobSeekerEditPage1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=SQLpassword,
            database="db1"
        )
        self.cursor = self.db.cursor()

        # Initialize TextInput fields for first screen
        self.name_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.age_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.dob_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.address_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.edu_qualifications_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.email_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.mob_no_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.nationality_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.prev_exp_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.exp_years_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))

        # Layout setup using GridLayout for first screen
        layout = GridLayout(cols=1, spacing=5, padding=[15,20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text='EDIT PROFILE', bold=True, font_size=40, size_hint=(0.5, None), size=(400, 50),
                            color=(0.8, 1.0, 0.0))
        layout.add_widget(title_label)

        fields = [
            (" ", Label(text=" ", font_size=20)),
            ("Name:", self.name_input),
            ("Age:", self.age_input),
            ("Date of Birth:", self.dob_input),
            ("Address:", self.address_input),
            ("Educational Qualifications:", self.edu_qualifications_input),
            ("Email:", self.email_input),
            ("Mobile Number:", self.mob_no_input),
            ("Nationality:", self.nationality_input),
            ("Previous Experience:", self.prev_exp_input),
            ("Years of Experience:", self.exp_years_input),
        ]
        form_layout=GridLayout(cols=2, spacing=10)
        for label, widget in fields:
            if label == "JOB SEEKER DETAILS":
                label_widget = Label(text=label, font_size=26, bold=True, color=(1, 0, 1, 1))
                form_layout.add_widget(label_widget)
            else:
                label_widget = Label(text=label, font_size=23, bold=True)
                form_layout.add_widget(label_widget)
            form_layout.add_widget(widget)

        # Load existing data from the database for first screen
        jobseeker_data = self.edit_jobseeker_profile(current_username)
        if jobseeker_data:
            self.set_hint_text(self.name_input, jobseeker_data[0])
            self.set_hint_text(self.age_input, str(jobseeker_data[1]) if jobseeker_data[1] else '')
            self.set_hint_text(self.dob_input, jobseeker_data[2].strftime('%Y-%m-%d') if jobseeker_data[2] else '')
            self.set_hint_text(self.address_input, jobseeker_data[3])
            self.set_hint_text(self.edu_qualifications_input, jobseeker_data[4])
            self.set_hint_text(self.email_input, jobseeker_data[5])
            self.set_hint_text(self.mob_no_input, str(jobseeker_data[6]) if jobseeker_data[6] else '')
            self.set_hint_text(self.nationality_input, jobseeker_data[7])
            self.set_hint_text(self.prev_exp_input, jobseeker_data[8])
            self.set_hint_text(self.exp_years_input, str(jobseeker_data[9]) if jobseeker_data[9] else '')

        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='Next', color=(0.8, 1.0, 0.0), bold=True, font_size=22,
                     size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.85,'center_y':0.5},
                     on_press=self.save_changes)
        back_button = Button(text='Back', color=(0.8, 1.0, 0.0), bold=True, font_size=22,
                     size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.15,'center_y':0.5},
                     on_press=self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(form_layout)
        layout.add_widget(button_layout)
        self.add_widget(layout)

    def back_page(self,instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'job_seeker_home_page'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def edit_jobseeker_profile(self, username):
        self.cursor.execute("SELECT * FROM jobseeker WHERE username=%s", (username,))
        result = self.cursor.fetchone()
        return result if result else None

    def set_hint_text(self, input_field, hint_text):
        input_field.hint_text = hint_text if hint_text else ""  # Ensure hint_text is not None
        input_field.hint_text_color = (0, 0, 0, 1)  # Black color for hint text

    def go_to_next_screen(self, instance):
        self.manager.current = 'jobseeker_edit_page2'  # Make sure this matches the name of JobSeekerEditPage2

    def save_changes(self, instance):
        name = self.name_input.text if self.name_input.text else self.name_input.hint_text
        age = self.age_input.text if self.age_input.text else self.age_input.hint_text
        dob = self.dob_input.text if self.dob_input.text else self.dob_input.hint_text
        address = self.address_input.text if self.address_input.text else self.address_input.hint_text
        edu_qualifications = self.edu_qualifications_input.text if self.edu_qualifications_input.text else self.edu_qualifications_input.hint_text
        email = self.email_input.text if self.email_input.text else self.email_input.hint_text
        mob_no = self.mob_no_input.text if self.mob_no_input.text else self.mob_no_input.hint_text
        nationality = self.nationality_input.text if self.nationality_input.text else self.nationality_input.hint_text
        prev_exp = self.prev_exp_input.text if self.prev_exp_input.text else self.prev_exp_input.hint_text
        exp_years = self.exp_years_input.text if self.exp_years_input.text else self.exp_years_input.hint_text

        updated_details = [
            name, age, dob, address, edu_qualifications, email, mob_no, nationality, prev_exp, exp_years
        ]
        query = """
        UPDATE jobseeker
        SET name = %s, age = %s, dob = %s, address = %s, educational_qualifications = %s, email = %s,
            mobno = %s, nationality = %s, prev_exp = %s, exp_years = %s
        WHERE username = %s
        """
        self.cursor.execute(query, (*updated_details, current_username))
        self.db.commit()
        print("Changes saved successfully!")
        """except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:"""
        self.cursor.close()
        self.db.close()
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'jobseeker_edit_page2'

class JobSeekerEditPage2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=SQLpassword,
            database="db1"
        )
        self.cursor = self.db.cursor()
        
        # Initialize TextInput fields for second screen
        self.prev_sal_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.expected_sal_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.mow_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.job_style_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.additional_skills_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.projects_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.certifications_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.ref_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.profile_picture_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))

        # Layout setup using GridLayout for second screen
        layout = GridLayout(cols=1, spacing=10, padding=[15,20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text='EDIT PROFILE', bold=True, font_size=40, size_hint=(0.5, None), size=(400, 50),
                            color=(0.8, 1.0, 0.0))
        layout.add_widget(title_label)
        form_layout = GridLayout(cols=2, spacing=10)
        fields = [
            (" ", Label(text=" ", font_size=20)),
            ("Previous Salary:", self.prev_sal_input),
            ("Expected Salary:", self.expected_sal_input),
            ("Mode of Work:", self.mow_input),
            ("Job Style:", self.job_style_input),
            ("Additional Skills:", self.additional_skills_input),
            ("Projects:", self.projects_input),
            ("Certifications:", self.certifications_input),
            ("References:", self.ref_input),
            ("Profile Picture Path:", self.profile_picture_input)
        ]

        for label, widget in fields:
            if label == "PREVIOUS AND EXPECTED SALARY":
                label_widget = Label(text=label, font_size=26, bold=True, color=(1, 0, 1, 1))
                form_layout.add_widget(label_widget)
            else:
                label_widget = Label(text=label, font_size=23, bold=True)
                form_layout.add_widget(label_widget)
            form_layout.add_widget(widget)
        # Load existing data from the database for second screen
        jobseeker_data = self.edit_jobseeker_profile(current_username)
        if jobseeker_data:
            self.set_hint_text(self.prev_sal_input, str(jobseeker_data[10]) if jobseeker_data[10] else '')
            self.set_hint_text(self.expected_sal_input, str(jobseeker_data[11]) if jobseeker_data[11] else '')
            self.set_hint_text(self.mow_input, jobseeker_data[12])
            self.set_hint_text(self.job_style_input, jobseeker_data[13])
            self.set_hint_text(self.additional_skills_input, jobseeker_data[14])
            self.set_hint_text(self.projects_input, jobseeker_data[15])
            self.set_hint_text(self.certifications_input, jobseeker_data[16])
            self.set_hint_text(self.ref_input, jobseeker_data[17])
            self.set_hint_text(self.profile_picture_input, jobseeker_data[21])
        button_layout = FloatLayout(size_hint_y=None, height=100)
        save_button = Button(text='Save Changes', color=(0.8, 1.0, 0.0), bold=True, font_size=22,
                     size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.85,'center_y':0.5},
                     on_press=self.save_changes)
        back_button = Button(text='Back',bold = True, size_hint=(None, None), size=(250, 75),
                             pos_hint={'center_x': 0.15, 'center_y': 0.5},color = (0.8, 1.0, 0.0),background_color=(0.9, 0.95, 1.0, 1.0),on_press=self.back_page)
        choose_button = Button(text='Choose', bold=True, size_hint=(None, None), size=(100, 50),
                               pos_hint={'center_x': 0.85, 'center_y': 0.5}, on_press=self.open_file_dialog)
        button_layout.add_widget(back_button)
        button_layout.add_widget(save_button)
        form_layout.add_widget(Label(text=" "))
        form_layout.add_widget(choose_button)
        layout.add_widget(form_layout)
        layout.add_widget(button_layout)
        self.add_widget(layout)
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'jobseeker_edit_page1'
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def edit_jobseeker_profile(self, username):
        self.cursor.execute("SELECT * FROM jobseeker WHERE username=%s", (username,))
        result = self.cursor.fetchone()
        return result if result else None
    def set_hint_text(self, input_field, hint_text):
        input_field.hint_text = hint_text if hint_text else " "  # Ensure hint_text is not None
        input_field.hint_text_color = (0, 0, 0, 1)  # Black color for hint text
    def save_changes(self, instance):
        prev_sal = self.prev_sal_input.text if self.prev_sal_input.text else self.prev_sal_input.hint_text
        expected_sal = self.expected_sal_input.text if self.expected_sal_input.text else self.expected_sal_input.hint_text
        mow = self.mow_input.text if self.mow_input.text else self.mow_input.hint_text
        job_style = self.job_style_input.text if self.job_style_input.text else self.job_style_input.hint_text
        additional_skills = self.additional_skills_input.text if self.additional_skills_input.text else self.additional_skills_input.hint_text
        projects = self.projects_input.text if self.projects_input.text else self.projects_input.hint_text
        certifications = self.certifications_input.text if self.certifications_input.text else self.certifications_input.hint_text
        ref = self.ref_input.text if self.ref_input.text else self.ref_input.hint_text
        profile_picture = self.profile_picture_input.text if self.profile_picture_input.text else self.profile_picture_input.hint_text
        global profile_path
        updated_details = [
            prev_sal, expected_sal, mow, job_style, additional_skills, projects, certifications, ref, profile_path
        ]
        query = """
        UPDATE jobseeker
        SET prev_sal = %s, expected_sal = %s, mow = %s, job_style = %s, additional_skills = %s, projects = %s, 
            certifications = %s, ref = %s, profile_picture_path= %s
        WHERE username = %s
        """
        self.cursor.execute(query, (*updated_details, current_username))
        self.db.commit()
        print("Changes saved successfully!")
    def open_file_dialog(self, instance):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        if file_path:
            self.profile_picture_input.text = file_path
            global profile_path
            profile_path = self.profile_picture_input.text

class JobSeeker_ChatPage(BoxLayout):
    def __init__(self, **kwargs):
        super(JobSeeker_ChatPage, self).__init__(**kwargs)
        self.clear_widgets()
        self.layout = BoxLayout(orientation='vertical', padding=[30], spacing=10)
        with self.layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.88, 0.93, 1, 1)  # sky blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)
        
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.message_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.message_list.bind(minimum_height=self.message_list.setter('height'))
        self.scroll_view.add_widget(self.message_list)
    
        self.input_box = BoxLayout(size_hint=(1, 0.1))
        self.text_input = TextInput(size_hint=(0.8, 1), hint_text="Chat with Admin")
        self.send_button = Button(text='Send', font_size=20, size_hint=(0.2, 1), color=[0.8, 0.8, 0.8, 1], background_color=[0, 0, 139, 1])
        self.send_button.bind(on_press=self.send_message)
        self.back_button = Button(text='back', font_size=20, size_hint=(0.1, 1), color=[0.8, 0.8, 0.8, 1], background_color=[0, 0, 139, 1])
        self.back_button.bind(on_press=self.go_back)
        self.input_box.add_widget(self.text_input)
        self.input_box.add_widget(self.send_button)
        self.input_box.add_widget(self.back_button) 
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.input_box)
        self.sent_msg= self.text_input.text
        sio.disconnect()
        threading.Thread(target=self.connect_to_server, daemon=True).start()
        self.add_widget(self.layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_back(self, instance):
        self.manager.current = 'job_seeker_home_page'
    
    def connect_to_server(self):
        try:
            sio.connect('http://127.0.0.1:5000/')  # Use your actual server URL
            sio.on('connect', self.on_connect)
            sio.on('disconnect', self.on_disconnect)
            sio.on('message', self.receive_message)
        except Exception as e:
            print(f"Connection error: {e}")

    def on_connect(self):
        print("Connected to server")
        self.is_connected = True

    def on_disconnect(self):
        print("Disconnected from server")
        self.is_connected = False

    def send_message(self, instance):
        message = self.text_input.text
        self.sent_msg = message
        if message:
            sio.send(message)
            self.text_input.text = ''
        boxlay = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        label = Button(text=f"{current_username} : {message}", 
                      font_size=20, 
                      size_hint_x=0.5, 
                      size_hint_y=None, 
                      height=40, 
                      halign='right', 
                      #valign='right', 
                      color=[1, 1, 1, 1],
                      background_color=[0, 0, 139, 1] )
        label2 = Label(text='', size_hint_x=0.5, size_hint_y=None, height=40)
        boxlay.add_widget(label2)
        boxlay.add_widget(label)
        
        self.message_list.add_widget(boxlay)
        self.scroll_view.scroll_to(label)

    def receive_message(self, msg):
        if self.sent_msg:
            if self.sent_msg == msg:
                self.sent_msg = ''
                return
        self.add_message_to_ui("Admin : "+msg, "received")

    @mainthread
    def add_message_to_ui(self, msg, msg_type):
        if msg_type == "received":
            boxlay = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            label = Button(text=msg, 
                           font_size=20, 
                           size_hint_x=0.5, 
                           size_hint_y=None,
                           height=40, 
                           halign='left', 
                           #valign='left', 
                           color=[1, 1, 1, 1],
                           background_color=[0, 1, 1, 1])
            label2 = Label(text='', size_hint_x=0.5, size_hint_y=None, height=40, halign='left', valign='center')
            boxlay.add_widget(label)
            boxlay.add_widget(label2)
        self.message_list.add_widget(boxlay)
        self.scroll_view.scroll_to(label)

class JobSeekerHomePage(Screen):
    def __init__(self, **kwargs):
        super(JobSeekerHomePage, self).__init__(**kwargs)

    def on_enter(self):
        with self.canvas.before:
            Color(0.88, 0.93, 1, 1)  # Whitish sky blue color
            self.rect = Rectangle(size=self.size, pos=self.pos)  
        self.homepage_layout = BoxLayout(orientation='vertical')
        self.homepage_layout.add_widget(Label(text="WELCOME      "+str(current_username)+" !!!!",
                                      bold=True,
                                      font_size='35',
                                      size_hint=(1, 0.1),
                                      color=(1, 0, 0, 1),
                                      font_name='Roboto-BoldItalic'))
        
        navbar_layout = BoxLayout(size_hint=(1, 0.1))

        self.recommendationpage = JobSeeker_RecommendationsPage(home_screen=self)
        self.searchpage = JobSeeker_SearchPage(home_screen=self)
        self.chatpage = JobSeeker_ChatPage()
        self.current_page = self.recommendationpage

        navbar_layout.add_widget(
            Button(text='Recommendations', 
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   bold = True,
                   on_press=lambda instance: self.switch_page(self.recommendationpage),
                   )
            )
        navbar_layout.add_widget(
            Button(text='Search Bar',
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   bold = True,
                   on_press=lambda instance: self.switch_page(self.searchpage),
                   )
            )
        
        navbar_layout.add_widget(
            Button(text='Chat Page',
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   bold = True,
                   on_press=lambda instance: self.switch_page(self.chatpage),
                   )
            )
        
        navbar_layout.add_widget(
            Button(text='Edit Profile',
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   bold = True,
                   on_press=lambda instance: self.gotoEditPage(),
                   )
            )
        

        self.button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='Logout', bold=True, size_hint=(None, None), size=(250, 50), background_color=(0, 0, 0.5, 1), pos_hint={'center_x': 0.8, 'center_y': 0.5}, on_press=self.back_page)
        self.button_layout.add_widget(back_button)

        self.homepage_layout.add_widget(navbar_layout)
        self.homepage_layout.add_widget(self.current_page)
        self.homepage_layout.add_widget(self.button_layout)  
        self.add_widget(self.homepage_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_leave(self, *args):
        if self.homepage_layout:
            self.remove_widget(self.homepage_layout)
            self.homepage_layout = None

    def switch_page(self, to_page):
        self.homepage_layout.remove_widget(self.current_page)
        self.homepage_layout.remove_widget(self.button_layout)
        self.current_page = to_page
        self.homepage_layout.add_widget(self.current_page)
        self.homepage_layout.add_widget(self.button_layout)

    def gotoEditPage(self):
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'jobseeker_edit_page1'

    def back_page(self, instance):
        jobseeker_record.clear()
        recruiter_record.clear()
        self.manager.current = 'job_seeker_login'

class Display_JobSeeker_Resume_1(Screen):
    def __init__(self, **kwargs):
        super(Display_JobSeeker_Resume_1, self).__init__(**kwargs)
        print("going into jobseeker resume page: ")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def disp_resume(self, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15):
        print("Data1:", Data1)

        # Create main layout with padding to ensure no content touches the borders
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20, 50, 20])  # Add padding: left, top, right, bottom

        with layout.canvas.before:
            Color(0.88, 0.93, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text=' ', bold=True, color=(0.8, 1.0, 0.0, 1), font_size=40, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        self.add_widget(layout)

        profile_picture = Image(source=str(Data11), size=(100, 100), size_hint=(None, None), pos_hint={'center_x': 0.1, 'top': 1})
        print(Data11)
        self.add_widget(profile_picture)

        form_layout = GridLayout(cols=1, spacing=10, size_hint_x=0.8, size_hint_y=None, height=800, padding=[20, 20, 20, 20])  # Added padding for inner layout

        # Helper function to create properly aligned labels
        def create_label(text, color, bold, height=30):
            label = Label(text=text, color=color, bold=bold, size_hint_y=None, height=height, halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))
            return label

        # Adding labels
        form_layout.add_widget(create_label("{}".format(Data1), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("DOB: {}".format(Data3), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data4), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}     {}".format(Data6, Data7), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("Educational Qualifications:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data5), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("Previous Experience:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{} for {} years".format(Data9, Data10), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("Additional skills:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data12), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("Projects Handled:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data13), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("Certifications:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data14), color=(0, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("Reference:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data15), color=(0, 0, 0, 1), bold=True))

        # Add some spacing
        for _ in range(4):
            form_layout.add_widget(Label(text=""))

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=250, padding=[20, 10, 20, 10])  # Horizontal BoxLayout for buttons

        back_button = Button(text='Back', color=(0.8, 1.0, 0.0, 1), bold=True, font_size=23, size_hint=(None, None), size=(200, 75), on_press=self.back_page)
        download_button = Button(text='Download', color=(0.8, 1.0, 0.0, 1), bold=True, font_size=23, size_hint=(None, None), size=(200, 75))
        download_button.bind(on_press=partial(self.download_resume, Data1, Data3, Data4, Data6, Data7, Data5, Data9, Data10, Data12, Data13, Data14, Data15, Data11))
        hire_button = Button(text='Hire', color=(0.8, 1.0, 0.0, 1), bold=True, font_size=23, size_hint=(None, None), size=(200, 75), on_press=self.hire_candidate)

        button_layout.add_widget(back_button)
        button_layout.add_widget(download_button)
        button_layout.add_widget(hire_button)

        layout.add_widget(form_layout)
        self.add_widget(button_layout)
    
    def download_resume(self, Data1, Data3, Data4, Data6, Data7, Data5, Data9, Data10, Data12, Data13, Data14, Data15, Data11, instance=None):
        # Use Tkinter file dialog to get the save location
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            # Generate the PDF using reportlab
            pdf_path = self.generate_pdf(file_path, Data1, Data3, Data4, Data6, Data7, Data5, Data9, Data10, Data12, Data13, Data14, Data15, Data11)
            if pdf_path:
                # Optionally show a success message or handle further actions
                print(f"Resume saved successfully as: {pdf_path}")
            else:
                print("Failed to save resume as PDF.")

    def hire_candidate(self, instance):
        # Implement your hiring logic here
        print(jobseeker_record)
        print(recruiter_record)
        x=Mail_functions.Hire_email_r2j(jobseeker_record,recruiter_record)
        if x==1:
            print("Job offer sent!")#shld be in label text
            print("Candidate hired!")
        # You can call your email function here or any other actions related to hiring

    def generate_pdf(self, file_path, Data1, Data3, Data4, Data6, Data7, Data5, Data9, Data10, Data12, Data13, Data14, Data15, Data11):
        # Create a PDF document using ReportLab
        c = canvas.Canvas(file_path, pagesize=letter)        
        # Set font and color
        c.setFont("Helvetica-Bold", 13)
        c.setFillColorRGB(0, 0, 0)  # Black color        
        # Draw background color
        c.setFillColorRGB(0.88, 0.93, 1)
        c.rect(0, 0, letter[0], letter[1], fill=1)
        # Draw profile picture
        if Data11:
            try:
                c.drawInlineImage(Data11, 100, 650, width=75, height=75)  # Adjust width and height as needed
            except Exception as e:
                print(f"Error drawing image: {e}")
        # Draw text content
        y_position = 600  # Start y position for text content below the image
        c.setFillColorRGB(0, 0, 0)  # Reset to black color
        c.drawString(100, y_position, f"Name: {Data1}")
        y_position -= 20
        c.drawString(100, y_position, f"DOB: {Data3}")
        y_position -= 20
        c.drawString(100, y_position, f"Email: {Data4}")
        y_position -= 20
        c.drawString(100, y_position, f"Address: {Data6}     {Data7}")
        y_position -= 30       
        # Draw educational qualifications
        c.setFillColorRGB(1, 0, 0)  # Red color
        c.drawString(100, y_position, "Educational Qualifications:")
        y_position -= 20
        c.setFillColorRGB(0, 0, 0) 
        c.drawString(100, y_position, f"{Data5}")
        y_position -= 30       
        # Draw previous experience
        c.setFillColorRGB(1, 0, 0)  # Red color
        c.drawString(100, y_position, "Previous Experience:")
        y_position -= 20
        c.setFillColorRGB(0, 0, 0) 
        c.drawString(100, y_position, f"{Data9} for {Data10} years")
        y_position -= 30       
        # Draw additional skills
        c.setFillColorRGB(1, 0, 0)  # Red color
        c.drawString(100, y_position, "Additional skills:")
        y_position -= 20
        c.setFillColorRGB(0, 0, 0) 
        c.drawString(100, y_position, f"{Data12}")
        y_position -= 30       
        # Draw projects handled
        c.setFillColorRGB(1, 0, 0)  # Red color
        c.drawString(100, y_position, "Projects Handled:")
        y_position -= 20
        c.setFillColorRGB(0, 0, 0) 
        c.drawString(100, y_position, f"{Data13}")
        y_position -= 30       
        # Draw certifications
        c.setFillColorRGB(1, 0, 0)  # Red color
        c.drawString(100, y_position, "Certifications:")
        y_position -= 20
        c.setFillColorRGB(0, 0, 0) 
        c.drawString(100, y_position, f"{Data14}")
        y_position -= 30       
        # Draw reference
        c.setFillColorRGB(1, 0, 0)  # Red color
        c.drawString(100, y_position, "Reference:")
        y_position -= 20
        c.setFillColorRGB(0, 0, 0) 
        c.drawString(100, y_position, f"{Data15}")
        c.save()
        return file_path  # Return the path where the PDF was saved

    def back_page(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'recruiter_home_page'

""" MODULES RELATED TO RECRUITERS """

class UsernamePasswordRecruiter(Screen):
    def __init__(self, **kwargs):
        super(UsernamePasswordRecruiter, self).__init__(**kwargs)
        background = Image(source='UP_Recruiter.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        box_layout = BoxLayout(orientation='horizontal', padding=(50, 0, 0, 0))
        layout = GridLayout(cols=1, padding=(50, 0, 0, 0))  
        title_layout = GridLayout(cols=1, padding=(0,0,0,0))
        title_layout.add_widget(Label(text="CREATE USERNAME AND PASSWORD",bold = True,color = (0.8, 1.0, 0.0),font_size = 50,height = 250,size_hint_y=None))
        layout.add_widget(title_layout)
        username_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        username_layout.add_widget(Label(text="Create Username:",font_size = 30,bold=True,size_hint_x=None, width=200))
        self.username_input = TextInput(hint_text='Username',size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0)) 
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        password_layout.add_widget(Label(text="Create Password:",font_size = 30,bold = True, size_hint_x=None,width=200))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0))
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        confirm_password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        confirm_password_layout.add_widget(Label(text="Confirm Password:",font_size = 30,bold = True, size_hint_x=None, width=200))
        self.confirm_password = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200,background_color=(0.8, 0.85, 1.0, 1.0))  
        confirm_password_layout.add_widget(self.confirm_password)
        layout.add_widget(confirm_password_layout)
        self.message_label = Label(size_hint=(None, None),bold = True,color = (0.8, 0.0, 0.0), size=(200, 50), pos_hint={'center_x': 0.5})  
        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='confirm',bold = True,size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5},on_press = self.check_passwords)
        back_button = Button(text='Back',bold = True, size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5},on_press = self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(self.message_label)
        layout.add_widget(button_layout) 
        #layout.add_widget(box_layout)
        self.add_widget(layout)
    def check_passwords(self, instance):
        if self.password_input.text != self.confirm_password.text:
            self.message_label.text = "Passwords do not match"
        else:
            self.message_label.text = ""
            username = self.username_input.text
            password = self.password_input.text
            inputs_recruiter.extend([username,password])
            inputs_recruiter[2]=inputs_recruiter[2]+','+inputs_recruiter[3]+','+inputs_recruiter[4]+','+inputs_recruiter[5]+','+inputs_recruiter[6]+','+inputs_recruiter[7]+','+inputs_recruiter[8]
            del inputs_recruiter[3:9]
            print(inputs_recruiter)
            print("Entering connectivity")
            connectivity_file.recruiter_insert(inputs_recruiter,profile_pic_path)
            self.manager.transition = SlideTransition(direction ="left")
            self.manager.current = 'recruiter_login'
    def back_page(self,instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_register_4'

class RecruiterLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(RecruiterLoginScreen, self).__init__(**kwargs)

    def on_enter(self):
        background = Image(source='Recruiter_Login.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        self.box_layout = BoxLayout(orientation='horizontal', padding=(50, 0, 0, 0))
        layout = GridLayout(cols=1, padding=(0, 0, 0, 0))  
        title_layout = GridLayout(cols=1, padding=(0,0,0,0))
        title_layout.add_widget(Label(text="RECRUITER LOGIN", bold=True, color=(0.8, 1.0, 0.0), font_size=50, height=250, size_hint_y=None))
        layout.add_widget(title_layout)
        username_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        username_layout.add_widget(Label(text="Enter username:", font_size=30, bold=True, size_hint_x=None, width=200))
        self.username_input = TextInput(hint_text='Username', size_hint_x=None, width=525, height=200, background_color=(0.8, 0.85, 1.0, 1.0))
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        password_layout.add_widget(Label(text="Enter password:", font_size=30, bold=True, size_hint_x=None, width=200))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525, height=200, background_color=(0.8, 0.85, 1.0, 1.0))
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        sub_grid_layout = GridLayout(cols=2, padding=(20, 10, 20, 10), spacing=(10, 15), size_hint=(None, None), size=(450, 80))
        sub_grid_layout.add_widget(Label(text="Forgot Password ?", bold=True, font_size=20))
        sub_grid_layout.add_widget(Button(text="Get OTP", bold=True, font_size=18, size=(190, 30), on_press=self.Get_OTP, background_color=(0.8, 0.8, 1.0, 1.0)))
        login_button_layout = BoxLayout(size_hint_y=None, height=100, padding=(20, 10, 20, 10))
        login_button = Button(text='Sign in', bold=True, size_hint=(None, None), size=(250, 50), on_press=self.login, background_color=(0.8, 0.8, 1.0, 1.0))
        login_button_layout.add_widget(login_button)
        layout.add_widget(login_button_layout)
        layout.add_widget(sub_grid_layout)  
        button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='back', bold=True, size_hint=(None, None), size=(250, 50), background_color=(0.8, 0.8, 1.0, 1.0), pos_hint={'center_x': 0.8, 'center_y': 0.5}, on_press=self.back_page)
        button_layout.add_widget(back_button)
        sub_layout = GridLayout(cols=2, padding=(20, 10, 20, 10), spacing=(10, 15), size_hint=(None, None), size=(450, 80))
        sub_layout.add_widget(Label(text="Don't have an account ?", bold=True, font_size=20))
        sub_layout.add_widget(Button(text="Sign up", bold=True, font_size=18, on_press=self.register, background_color=(0.8, 0.8, 1.0, 1.0)))
        layout.add_widget(sub_layout)  
        layout.add_widget(button_layout)
        self.box_layout.add_widget(layout)
        self.add_widget(self.box_layout)   
    def on_leave(self, *args):
        if self.box_layout:
            self.remove_widget(self.box_layout)
            self.box_layout = None
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'login'   
    def Get_OTP(self, instance):
        self.manager.current = 'forgot_password_recruiter'    
    def login(self, instance):
        global current_username
        current_username = self.username_input.text
        username = self.username_input.text
        password = self.password_input.text
        if connectivity_file.check_existence_recruiter(username) == 1:
            recruiter_record.extend(connectivity_file.get_record_recruiter(username))
            if password == connectivity_file.verify_password_recruiter(username):
                self.show_success_popup()
                self.manager.current = 'recruiter_home_page'
    def show_success_popup(self):
        # Create the pop-up content
        popup_content = BoxLayout(orientation='vertical')
        message_label = Label(text="Logged in successfully")
        ok_button = Button(text="OK", size_hint_y=None, height=50)        
        # Add the label and button to the pop-up content
        popup_content.add_widget(message_label)
        popup_content.add_widget(ok_button)       
        # Create the pop-up
        popup = Popup(title="Success",
                      content=popup_content,
                      size_hint=(None, None), size=(300, 200),
                      auto_dismiss=False)       
        # Bind the OK button to dismiss the pop-up
        ok_button.bind(on_release=popup.dismiss)      
        # Open the pop-up
        popup.open()   
    def register(self, instance):
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'recruiter_register_1'

class ForgotPasswordRecruiter(Screen):
    def __init__(self, **kwargs):
        super(ForgotPasswordRecruiter, self).__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)       
        title_label = Label(text='Forgot Password ?', bold=True, color=(0.8, 1.0, 0.0), font_size=50, size_hint=(None, None), size=(400, 50), pos_hint={'center_x': 0.5, 'top': 0.9})
        layout.add_widget(title_label)       
        Email_layout = FloatLayout(size_hint=(None, None), size=(600, 200), pos_hint={'center_x': 0.5, 'top': 0.6})       
        email_label = Label(text="Enter Email ID:", font_size=30, bold=True, size_hint=(None, None), size=(200, 50), pos_hint={'x': 0, 'top': 1.5})
        Email_layout.add_widget(email_label)        
        self.Email_input = TextInput(hint_text='Email ID', size_hint=(None, None), size=(550, 80), pos_hint={'center_x': 0.45, 'top': 1}, background_color=(0.8, 0.85, 1.0, 1.0))
        Email_layout.add_widget(self.Email_input)  
        layout.add_widget(Email_layout) 
        self.message_label = Label(text="", size_hint=(None, None), bold=True, color=(0.8, 0.0, 0.0), size=(200, 50), pos_hint={'center_x': 0.3,'top':0.5}) 
        layout.add_widget(self.message_label) 
        OTP_layout = FloatLayout(size_hint=(None, None), size=(600, 200), pos_hint={'center_x': 0.475, 'top': 0.5})           
        get_otp_button = Button(text="Get OTP", color=(0.8, 1.0, 0.0), bold=True, font_size=23, size_hint=(None, None), size=(175, 50), pos_hint={'center_x': 0.75, 'top': 1}, on_press=self.send_OTP)
        OTP_layout.add_widget(get_otp_button)  
        getotp_label = Label(text="Enter OTP:", font_size=30, bold=True, size_hint=(None, None), size=(200, 50), pos_hint={'x': 0, 'top': 0.6})
        OTP_layout.add_widget(getotp_label)        
        self.OTP_input = TextInput(hint_text='OTP', size_hint=(None, None), size=(250, 65), pos_hint={'center_x': 0.25, 'top': 0.3}, background_color=(0.8, 0.85, 1.0, 1.0))
        OTP_layout.add_widget(self.OTP_input)     
        layout.add_widget(OTP_layout) 
        verify_button = Button(text = "Verify", color=(0.8,1.0,0.0),bold = True,font_size = 23,size_hint = (None,None),size = (175,50),pos_hint = {'center_x' :0.55,'top': 0.3255},on_press = self.verify)
        layout.add_widget(verify_button)  
        back_button = Button(text = 'Back',bold = True,color=(0.8,1.0,0.0),font_size = 23,size_hint = (None,None),size = (175,50),pos_hint = {'center_x':0.315,'top': 0.2},on_press = self.back_page) 
        layout.add_widget(back_button)   
        self.add_widget(layout)       
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size  
    def send_OTP(self, instance):
        self.message_label.text = "OTP sent"
        instance.text = "Resend OTP"  
        global otp
        otp=otp+Mail_functions.send_otp(self.Email_input.text)
    def verify(self,instance):
        global otp
        self.OTP=self.OTP_input.text
        if int(self.OTP)==otp:  
            self.manager.transition = SlideTransition(direction ="left")
            self.manager.current = 'change_password_recruiter'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_login'

class ChangePasswordRecruiter(Screen):
    def __init__(self, **kwargs):
        super(ChangePasswordRecruiter, self).__init__(**kwargs)
        background = Image(source='UP_Recruiter.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        box_layout = BoxLayout(orientation='horizontal', padding=(50, 0, 0, 0))
        layout = GridLayout(cols=1, padding=(50, 0, 0, 0))  
        title_layout = GridLayout(cols=1, padding=(0,0,0,0))
        title_layout.add_widget(Label(text="CHANGE PASSWORD",bold = True,color = (0.8, 1.0, 0.0),font_size = 50,height = 250,size_hint_y=None))
        layout.add_widget(title_layout)
        username_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        username_layout.add_widget(Label(text="Enter Username:",font_size = 30,bold=True,size_hint_x=None, width=200))
        self.username_input = TextInput(hint_text='Username',size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0)) 
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        password_layout.add_widget(Label(text="New Password:",font_size = 30,bold = True, size_hint_x=None,width=200))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200, background_color=(0.8, 0.85, 1.0, 1.0))
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        confirm_password_layout = GridLayout(cols=1, padding=(20, 10, 20, 10), spacing=(10, 10))
        confirm_password_layout.add_widget(Label(text="Confirm Password:",font_size = 30,bold = True, size_hint_x=None, width=200))
        self.confirm_password = TextInput(hint_text='Password', password=True, size_hint_x=None, width=525,height = 200,background_color=(0.8, 0.85, 1.0, 1.0))  
        confirm_password_layout.add_widget(self.confirm_password)
        layout.add_widget(confirm_password_layout)
        self.message_label = Label(size_hint=(None, None),bold = True,color = (0.8, 0.0, 0.0), size=(200, 50), pos_hint={'center_x': 0.5})  
        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='confirm',bold = True,size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5},on_press = self.check_passwords)
        back_button = Button(text='Back',bold = True, size_hint=(None, None),color = (0.8, 1.0, 0.0), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5},on_press = self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(self.message_label)
        layout.add_widget(button_layout) 
        self.add_widget(layout)
    def check_passwords(self, instance):
        if self.password_input.text != self.confirm_password.text:
            self.message_label.text = "Passwords do not match"
        else:
            self.message_label.text = ""
            username = self.username_input.text
            password = self.password_input.text
            connectivity_file.change_password_recruiter(username,password)
            print(inputs_recruiter)
            self.manager.transition = SlideTransition(direction ="left")
            self.manager.current = 'recruiter_login'
    def back_page(self,instance):
            self.manager.transition = SlideTransition(direction ="right")
            self.manager.current = 'forgot_password_recruiter'

class RecruiterRegisterPart1(Screen):
    def __init__(self, **kwargs):
        super(RecruiterRegisterPart1, self).__init__(**kwargs)
        self.name_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.dob_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.address_no_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.street_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.area_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.district_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.city_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.state_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.pincode_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text='REGISTER',bold = True, font_size=50, size_hint=(None, None), size=(200, 50),color = (0.8, 1.0, 0.0),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        form_layout = GridLayout(cols=2, spacing=10)
        fields = [
            ("RECRUITER DETAILS", Label(text=" ", font_size=20)),
            ("Name:", self.name_input),
            ("Date of Birth:", self.dob_input),
            ("COMPANY ADDRESS", Label(text=" ", font_size=20)),
            ("No.:", self.address_no_input),
            ("Place/street:", self.street_input),
            ("Area:", self.area_input),
            ("District:", self.district_input),
            ("City:", self.city_input),
            ("State:", self.state_input),
            ("Pincode:", self.pincode_input)
        ]
        for label, widget in fields:
            if label == "COMPANY ADDRESS" or label == "RECRUITER DETAILS":
                label_widget = Label(text=label, font_size=26,bold = True, color=(1, 0, 1, 1))
                form_layout.add_widget(label_widget)
            else:
                form_layout.add_widget(Label(text=label, font_size=23,bold = True))
            form_layout.add_widget(widget)
        layout.add_widget(form_layout)
        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='Next',color = (0.8, 1.0, 0.0),bold=True,font_size = 22, size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5},
                             on_press=self.next_page)
        back_button = Button(text='Back',color = (0.8, 1.0, 0.0),bold=True,font_size = 22,size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5},
                             on_press=self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(button_layout)
        self.add_widget(layout)
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next_page(self, instance):
        name = self.name_input.text
        dob = self.dob_input.text
        address_no = self.address_no_input.text
        street = self.street_input.text
        area = self.area_input.text
        district = self.district_input.text
        city = self.city_input.text
        state = self.state_input.text
        pincode = self.pincode_input.text
        inputs_recruiter.extend([name,dob,address_no,street,area,district,city,state,pincode])
        print("Name:", name)
        print("Date of Birth:", dob)
        print("Address No.:", address_no)
        print("Street:", street)
        print("Area:", area)
        print("District:", district)
        print("City:", city)
        print("State:", state)
        print("Pincode:", pincode)
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'recruiter_register_2'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_login'

class RecruiterRegisterPart2(Screen):
    def __init__(self, **kwargs):
        super(RecruiterRegisterPart2, self).__init__(**kwargs)
        self.designation_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.department_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.experience_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.mobile_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.email_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.job_designation_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.qualifications_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.additional_requirements_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        self.candidate_location_input = TextInput(multiline=False,background_color=(0.8, 0.85, 1.0, 1.0))
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text='REGISTER',bold = True,color = (0.8, 1.0, 0.0), font_size=50, size_hint=(None, None), size=(200, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        form_layout = GridLayout(cols=2, spacing=10)
        fields = [
            ("RECRUITER DETAILS", Label(text=" ", font_size=20)),
            ("Designation:", self.designation_input),
            ("Department:", self.department_input),
            ("Years of Experience: ", self.experience_input),
            ("Mobile No.:", self.mobile_input),
            ("Email:", self.email_input),
            ("RECRUITING JOB DETAILS", Label(text=" ", font_size=20)),
            ("Job Designation:", self.job_designation_input),
            ("Qualifications:", self.qualifications_input),
            ("Additional Requirements:", self.additional_requirements_input),
            ("Company Name:", self.candidate_location_input)
        ]
        for label, widget in fields:
            if label == "RECRUITER DETAILS" or label == "RECRUITING JOB DETAILS":
                label_widget = Label(text=label, font_size=26,bold = True, color=(1, 0, 1, 1))
                form_layout.add_widget(label_widget)
            else:
                form_layout.add_widget(Label(text=label, font_size=23,bold = True))
            form_layout.add_widget(widget)
        layout.add_widget(form_layout)
        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='Next',color = (0.8, 1.0, 0.0),bold = True,font_size=23, size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5},
                             on_press=self.next_page)
        back_button = Button(text='Back',color = (0.8, 1.0, 0.0),bold=True,font_size=23, size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5},
                             on_press=self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(button_layout)
        self.add_widget(layout)
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next_page(self, instance):
        # Get values from TextInput fields
        designation = self.designation_input.text
        department = self.department_input.text
        experience = self.experience_input.text
        mobile = self.mobile_input.text
        email = self.email_input.text
        job_designation = self.job_designation_input.text
        qualifications = self.qualifications_input.text
        additional_requirements = self.additional_requirements_input.text
        candidate_location = self.candidate_location_input.text
        inputs_recruiter.extend([designation,department,experience,mobile,email,job_designation,qualifications,additional_requirements,candidate_location])
        print("Designation:", designation)
        print("Department:", department)
        print("Years of Experience:", experience)
        print("Mobile No.:", mobile)
        print("Email:", email)
        print("Job Designation:", job_designation)
        print("Qualifications:", qualifications)
        print("Additional Requirements:", additional_requirements)
        print("Company Name:", candidate_location)
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'recruiter_register_3'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_register_1'

class RecruiterRegisterPart3(Screen):
    def __init__(self, **kwargs):
        super(RecruiterRegisterPart3, self).__init__(**kwargs)
        self.additional_qualifications_input = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.basic_pay_input = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.certifications_input = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.years_experience_input = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        self.industrial_sector = ""
        self.mode = ""
        self.job_style = ""
        self.Gender = ""
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text='REGISTER',bold=True,font_size=50,color = (0.8, 1.0, 0.0), size_hint=(None, None), size=(200, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        form_layout = GridLayout(cols=2, spacing=10)
        self.dropdowns = {}
        dropdown_fields = [
            ("Industrial Sector", ["Finance", "Sales", "Transport", "Health", "Agri", "IT"]),
            ("Mode of Working ", ["Online", "Offline", "Both"]),
            ("Job Style ", ["Part-time", "Full-time"]),
            ("Gender Specification", ["Male", "Female", "Both"])
        ]
        for label, options in dropdown_fields:
            dropdown, dropdown_button, label = self.build_dropdown_content(options, label)
            self.dropdowns[label] = {'dropdown': dropdown, 'button': dropdown_button}  
            form_layout.add_widget(Label(text=label,bold=True,font_size=23))
            form_layout.add_widget(dropdown_button)
        fields = [
            ("Additional Qualifications(if any):", self.additional_qualifications_input),
            ("Basic Pay:", self.basic_pay_input),
            ("Certifications required :", self.certifications_input),
            ("Required years of experience:", self.years_experience_input)
        ]
        for label, widget in fields:
            form_layout.add_widget(Label(text=label,bold=True,font_size=23))
            form_layout.add_widget(widget)
        layout.add_widget(form_layout)
        button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='Back',bold=True,color = (0.8, 1.0, 0.0),font_size=26,size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.25, 'center_y': 0.5},
                             on_press=self.back_page)
        next_button = Button(text='next',bold=True,color = (0.8, 1.0, 0.0),font_size=26,size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.75, 'center_y': 0.5},
                             on_press=self.next_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(button_layout)
        self.add_widget(layout)
    def build_dropdown_content(self, options, label):
        dropdown = DropDown()
        dropdown_button = Button(text='-Select-',bold=True,color = (0.8, 1.0, 0.0),size_hint=(None, None), size=(100, 44))
        dropdown_button.bind(on_release=dropdown.open)
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, option=option, label=label: self.on_dropdown_select(label, option, dropdown_button))
            dropdown.add_widget(btn)
        return dropdown, dropdown_button, label  
    def on_dropdown_select(self, label, value, dropdown_button):
        if label == "Industrial Sector":
            self.industrial_sector = value
        elif label == "Mode of Working ":
            self.mode = value
        elif label == "Job Style ":
            self.job_style = value 
        elif label == "Gender Specification":
            self.Gender = value
        dropdown_button.text = value
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def next_page(self, instance):
        additional_qualifications = self.additional_qualifications_input.text
        basic_pay = self.basic_pay_input.text
        certifications = self.certifications_input.text
        years_experience = self.years_experience_input.text
        sector = self.industrial_sector
        mode = self.mode
        style = self.job_style
        gender = self.Gender
        inputs_recruiter.extend([basic_pay,certifications,years_experience,sector,mode,style])
        print("Additional Qualifications:", additional_qualifications)
        print("Basic Pay:", basic_pay)
        print("Certifications required:", certifications)
        print("Required years of experience:", years_experience)
        print("Job Sector: ", sector)
        print("Job Mode: ", mode)
        print("Job Style: ", style)
        print("Gender: ", gender)
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'recruiter_register_4'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_register_2'

class RecruiterRegisterPart4(Screen):
    def __init__(self, **kwargs):
        super(RecruiterRegisterPart4, self).__init__(**kwargs)
        self.age_constraint = ""
        self.shift = ""
        self.working_hours = ""
        self.job_description = ""
        self.profile_picture_path = ""
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        title_layout = FloatLayout(size_hint_y=None, height=70)
        title_label = Label(text='REGISTER', bold=True, font_size=50, color=(0.8, 1.0, 0.0),
                            size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_layout.add_widget(title_label)
        layout.add_widget(title_layout)
        form_layout = GridLayout(cols=2, spacing=10)

        dropdown_fields = [
            ("Age constraint", ['25-30', '35-40', '45-50', '55-60', "above"]),
            ("Shift", ["Day", "Night", "Swing", "Rotational"]),
            ("Working Hours", ['6', '7', '8', '9'])
        ]
        self.dropdowns = {}
        for label, options in dropdown_fields:
            dropdown, dropdown_button = self.build_dropdown_content(options, label)
            self.dropdowns[label] = dropdown
            form_layout.add_widget(Label(text=label, bold=True, font_size=23))
            form_layout.add_widget(dropdown_button)

        # Add profile picture path field
        # Choose button for profile picture
        choose_button = Button(text="Choose", bold=True, color=(0.8, 1.0, 0.0), size_hint=(None, None), size=(100, 44))
        choose_button.bind(on_press=self.choose_profile_picture)

        # Job description input
        form_layout.add_widget(Label(text="Overall Job Description", bold=True, font_size=23))
        self.job_description_input = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        form_layout.add_widget(self.job_description_input)
        form_layout.add_widget(Label(text="Profile Picture Path", bold=True, font_size=23))
        self.profile_picture_input = TextInput(background_color=(0.8, 0.85, 1.0, 1.0))
        form_layout.add_widget(self.profile_picture_input)
        form_layout.add_widget(Label(text=" "))
        form_layout.add_widget(choose_button)
        layout.add_widget(form_layout)
        button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='Back', bold=True, color=(0.8, 1.0, 0.0), size_hint=(None, None), size=(250, 75),
                             pos_hint={'center_x': 0.25, 'center_y': 0.5}, on_press=self.back_page)
        register_button = Button(text='Register', bold=True, color=(0.8, 1.0, 0.0), size_hint=(None, None), size=(250, 75),
                                 pos_hint={'center_x': 0.75, 'center_y': 0.5}, on_press=self.register)
        button_layout.add_widget(back_button)
        button_layout.add_widget(register_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def build_dropdown_content(self, options, label):
        dropdown = DropDown()
        dropdown_button = Button(text='-Select-', bold=True, color=(0.8, 1.0, 0.0), size_hint=(None, None), size=(100, 44))
        dropdown_button.bind(on_release=dropdown.open)
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, option=option, label=label: self.on_dropdown_select(label, option, dropdown_button))
            dropdown.add_widget(btn)
        return dropdown, dropdown_button

    def on_dropdown_select(self, label, value, dropdown_button):
        if label == "Age constraint":
            self.age_constraint = value
        elif label == "Shift":
            self.shift = value
        elif label == "Working Hours":
            self.working_hours = value
        dropdown_button.text = value

    def choose_profile_picture(self, instance):
        # Open the file chooser in a separate thread to avoid blocking the Kivy UI
        threading.Thread(target=self.open_file_dialog).start()

    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        root.destroy()  # Close the Tkinter window

        # Update the TextInput field on the main Kivy thread
        if file_path:
            self.profile_picture_path = file_path
            global profile_path
            profile_path=self.profile_picture_path
            print(profile_path)
            Clock.schedule_once(self.update_profile_picture_input, 0)

    def update_profile_picture_input(self, dt):
        self.profile_picture_input.text = self.profile_picture_path 

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def register(self, instance):
        self.job_description = self.job_description_input.text
        inputs_recruiter.extend([self.age_constraint, self.shift, self.working_hours, self.job_description])
        print("Age Constraint:", self.age_constraint)
        print("Shift:", self.shift)
        print("Working Hours:", self.working_hours)
        print("Job Description:", self.job_description)
        print("Profile Picture Path:", self.profile_picture_path)
        print(inputs_recruiter)
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'Username_recruiter'
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_register_3'

class Recruiter_Recommendations_Card(FloatLayout):
    def __init__(self, home_screen, username="Name", rec_perc="__", profile_picture="", **kwargs):
        super(Recruiter_Recommendations_Card, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 180  # Increase the height of the card
        with self.canvas.before:
            Color(0.2, 0.7, 0.9, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)    
        self.bind(size=self._update_rect, pos=self._update_rect)
        # Profile Picture
        self.profile_picture = AsyncImage(source=profile_picture, size_hint=(None, None), size=(100, 85), pos_hint={'center_x': 0.1, 'center_y': 0.5})
        self.add_widget(self.profile_picture)
        # Name Label
        name_label = Label(text=f"{username}", size_hint=(None, None), bold=True, size=(120, 50), pos_hint={'x': 0.04, 'y': 0.02}, valign='bottom', color=(0, 0, 0, 1))
        self.add_widget(name_label)
        match_per = Label(text=f"{rec_perc}%", bold=True,font_size=50,size_hint=(None, None), size=(60, 50), pos_hint={'right': 0.625, 'top': 0.6}, valign='middle', color=(0, 0.5, 0, 1))
        self.add_widget(match_per)
        # Matches Label
        matches_label = Label(text=f"Requirements Matched", bold=True, size_hint=(None, None), size=(300, 50), pos_hint={'right': 0.925, 'top': 0.8}, valign='middle', color=(0, 0, 0, 1))
        self.add_widget(matches_label)
        # View Profile Button
        view_profile_button = Button(text="View Profile",color=(0.57, 1, 0.57, 1), size_hint=(None, None),bold=True, size=(175, 50), pos_hint={'right': 0.875, 'top': 0.4},background_color=(0.53, 0.81, 0.92, 1))
        view_profile_button.bind(on_press=lambda instance: self._view_profile(home_screen, username))
        self.add_widget(view_profile_button)
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size    
    def _view_profile(self, home_screen, username):
        L = connectivity_file.get_record(username)
        date_obj = L[2]
        date_str = date_obj.strftime('%D')
        L[2] = date_str
        for i in range(len(L)):
            Data[i] = L[i]
        print("Data:", Data)
        jobseeker_record.extend(Data)
        home_screen.manager.transition = SlideTransition(direction="left")
        home_screen.manager.current = 'jobseeker_resume_1'
        home_screen.manager.get_screen('jobseeker_resume_1').clear_widgets()
        home_screen.manager.get_screen('jobseeker_resume_1').disp_resume(Data[0], Data[1], Data[2], Data[3], Data[4], Data[5], Data[6], Data[7], Data[8], Data[9], Data[21],Data[14],Data[15],Data[16],Data[17])

class Recruiter_RecommendationsPage(ScrollView):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.home_screen = home_screen
        scroll_layout = GridLayout(cols=1, 
                                   spacing=10, 
                                   size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        scroll_layout.add_widget(Label(text=" "))
        scroll_layout.add_widget(Label(text=" "))
        scroll_layout.add_widget(Label(text="RECOMMENDATIONS",bold = True,color=(1, 0, 0, 1) ))
        scroll_layout.add_widget(Label(text=" "))
        print(recruiter_record[22])
        connectivity_file.count_set0()
        L=connectivity_file.get_reccommended_jobseekers(recruiter_record[22])
        print("Recruiter Record:",recruiter_record)
        print("Recommended list:",L)
        for _name, _perc in L:
            x=connectivity_file.get_record(_name)
            profile_picture_path = x[21] 
            scroll_layout.add_widget(Recruiter_Recommendations_Card(home_screen=self.home_screen, username = _name,rec_perc = round((_perc/6)*100,2),profile_picture=profile_picture_path ) )       
        self.add_widget(scroll_layout)

'''class Recruiter_SearchPage(ScrollView):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.home_screen = home_screen
        
        self.search_input = TextInput(hint_text="Enter username to be searched", 
                                      multiline=False, 
                                      size_hint=(0.8, 0.1), 
                                      pos_hint={'x': 0.1, 'y': 0.9})
        self.layout.add_widget(self.search_input)
        
        search_button = Button(text="Search", 
                               size_hint=(0.2, 0.1), 
                               pos_hint={'x': 0.4, 'y': 0.8},
                               background_color = (0.53, 0.81, 0.92, 1))
        search_button.bind(on_press=lambda instance: self.search(home_screen=home_screen, textEntered=self.search_input.text))
        self.layout.add_widget(search_button)
        
        age_spinner = Spinner(
            text='Select Age',
            values=('18-25', '26-35', '36-45', '46-60', '60+'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.7},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(age_spinner)
       
        

        salary_spinner = Spinner(
            text='Expected Salary',
            values=('$0-$30k', '$30k-$50k', '$50k-$70k', '$70k-$100k', '$100k+'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.7},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(salary_spinner)

        mode_spinner = Spinner(
            text='Mode of Working',
            values=('Remote', 'On-site', 'Hybrid'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.6},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(mode_spinner)

        job_style_spinner = Spinner(
            text='Job Style',
            values=('Full-time', 'Part-time', 'Freelance', 'Internship'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.6},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(job_style_spinner)

    def search(self, home_screen, textEntered):
        home_screen.manager.current = 'recruiter_searchresults'
        search_results_screen = home_screen.manager.get_screen('recruiter_searchresults')
        search_results_screen.home_screen = home_screen
        search_results_screen.textEntered = textEntered'''

class Recruiter_SearchPage(ScrollView):
    def __init__(self, home_screen, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.home_screen = home_screen
        
        self.search_input = TextInput(hint_text="Enter username to be searched", 
                                      multiline=False, 
                                      size_hint=(0.8, 0.1), 
                                      pos_hint={'x': 0.1, 'y': 0.9})
        self.layout.add_widget(self.search_input)
        
        search_button = Button(text="Search", 
                               size_hint=(0.2, 0.1), 
                               pos_hint={'x': 0.4, 'y': 0.8},
                               background_color = (0.53, 0.81, 0.92, 1))
        search_button.bind(on_press=self.on_search_button_pressed)
        self.layout.add_widget(search_button)
        
        self.age_spinner = Spinner(
            text='Select Age',
            values=('18-25', '26-35', '36-45', '46-60', '60-70'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.7},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.age_spinner)

        self.salary_spinner = Spinner(
            text='Expected Salary',
            values=('₹0-₹30000', '₹30000-₹50000', '₹50000-₹70000', '₹70000-₹100000', '₹100000-₹150000'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.7},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.salary_spinner)

        self.mode_spinner = Spinner(
            text='Mode of Working',
            values=('Offline', 'Online', 'Both'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.6},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.mode_spinner)

        self.job_style_spinner = Spinner(
            text='Job Style',
            values=('Full-time', 'Part-time'),
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.6},
            background_color = (0.53, 0.81, 0.92, 1))
        self.layout.add_widget(self.job_style_spinner)

    def on_search_button_pressed(self, instance):
        self.search(home_screen=self.home_screen, 
                    textEntered=self.search_input.text, 
                    age=self.age_spinner.text, 
                    salary=self.salary_spinner.text, 
                    mode=self.mode_spinner.text, 
                    job_style=self.job_style_spinner.text)

    def search(self, home_screen, textEntered, age, salary, mode, job_style):
        home_screen.manager.current = 'recruiter_searchresults'
        search_results_screen = home_screen.manager.get_screen('recruiter_searchresults')
        search_results_screen.home_screen = home_screen
        search_results_screen.textEntered = textEntered
        search_results_screen.age = age
        search_results_screen.salary = salary
        search_results_screen.mode = mode
        search_results_screen.job_style = job_style
        # Now you can use the age, salary, mode, and job_style variables as needed

class Recruiter_SearchResults(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.home_screen = None
        self.layout = ''
        self.textEntered = ''
        self.age=''
        self.salary=''
        self.mode=''
        self.jobstyle=''
        
    def on_enter(self):
        self.layout = GridLayout(cols=1, 
                                   spacing=10, 
                                   size_hint_y=None)
        self.button_layout = FloatLayout()
        self.layout.bind(minimum_height=self.layout.setter('height'))
        print("PRINTINTG:",self.textEntered,self.salary,self.mode,self.age,self.jobstyle)
        L=connectivity_file.search_jobseekers_byfilter(self.textEntered,self.salary,self.mode,self.age,self.jobstyle)
        for _name, _perc,path in L:
            self.layout.add_widget(Recruiter_Recommendations_Card(home_screen=self.home_screen, username = _name,rec_perc = round((_perc/6)*100,2),profile_picture=path) )
        back_button = Button(text='<--',bold = True,size_hint=(None, None),
                             size=(250, 50),background_color=(0, 0, 0.5, 1), 
                             pos_hint={'center_x': 0.1, 'center_y': 0.925},
                             on_press = self.back_page)
        self.button_layout.add_widget(back_button)
        self.add_widget(self.layout)
        self.add_widget(self.button_layout)

    def on_leave(self, *args):
        self.remove_widget(self.layout)
        self.remove_widget(self.button_layout)
        self.layout = None
    
    def back_page(self,instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current='recruiter_home_page'

class RecruiterEditPage1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=SQLpassword,
            database="db1"
        )
        self.cursor = self.db.cursor()

        # Initialize TextInput fields for first screen
        self.name_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.dob_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.address_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.rec_desig_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.rec_dept_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.exp_years_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.mob_no_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.email_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.avail_job_design_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.qualifications_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.add_requirements_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.company_name_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))

        # Layout setup using GridLayout for first screen
        layout = GridLayout(cols=1, spacing=5, padding=[15,20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text='EDIT PROFILE', bold=True, font_size=40, size_hint=(0.5, None), size=(400, 50),
                            color=(0.8, 1.0, 0.0))
        layout.add_widget(title_label)

        fields = [
            (" ", Label(text=" ", font_size=20)),
            ("Name:", self.name_input),
            ("Date of Birth:", self.dob_input),
            ("Address:", self.address_input),
            ("Designation:", self.rec_desig_input),
            ("Department:", self.rec_dept_input),
            ("Years of Experience:", self.exp_years_input),
            ("Mobile Number:", self.mob_no_input),
            ("Email:", self.email_input),
            ("Available Job Designation:", self.avail_job_design_input),
            ("Qualifications:", self.qualifications_input),
            ("Additional Requirements:", self.add_requirements_input),
            ("Company Name:", self.company_name_input),
        ]
        form_layout=GridLayout(cols=2, spacing=10)
        for label, widget in fields:
            if label == "RECRUITER DETAILS":
                label_widget = Label(text=label, font_size=26, bold=True, color=(1, 0, 1, 1))
                form_layout.add_widget(label_widget)
            else:
                label_widget = Label(text=label, font_size=23, bold=True)
                form_layout.add_widget(label_widget)
            form_layout.add_widget(widget)

        # Load existing data from the database for first screen
        recruiter_data = self.edit_recruiter_profile(current_username)
        if recruiter_data:
            self.set_hint_text(self.name_input, recruiter_data[0])
            self.set_hint_text(self.dob_input, recruiter_data[1].strftime('%Y-%m-%d') if recruiter_data[1] else '')
            self.set_hint_text(self.address_input, recruiter_data[2])
            self.set_hint_text(self.rec_desig_input, recruiter_data[3])
            self.set_hint_text(self.rec_dept_input, recruiter_data[4])
            self.set_hint_text(self.exp_years_input, str(recruiter_data[5]) if recruiter_data[5] else '')
            self.set_hint_text(self.mob_no_input, str(recruiter_data[6]) if recruiter_data[6] else '')
            self.set_hint_text(self.email_input, recruiter_data[7])
            self.set_hint_text(self.avail_job_design_input, recruiter_data[8])
            self.set_hint_text(self.qualifications_input, recruiter_data[9])
            self.set_hint_text(self.add_requirements_input, recruiter_data[10])
            self.set_hint_text(self.company_name_input, recruiter_data[11])

        button_layout = FloatLayout(size_hint_y=None, height=100)
        next_button = Button(text='Next', color=(0.8, 1.0, 0.0), bold=True, font_size=22,
                     size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.85,'center_y':0.5},
                     on_press=self.save_changes)
        back_button = Button(text='Back', color=(0.8, 1.0, 0.0), bold=True, font_size=22,
                     size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.15,'center_y':0.5},
                     on_press=self.back_page)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        layout.add_widget(form_layout)
        layout.add_widget(button_layout)
        self.add_widget(layout)

    def back_page(self,instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_home_page'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def edit_recruiter_profile(self, username):
        self.cursor.execute("SELECT * FROM recruiter WHERE username=%s", (username,))
        result = self.cursor.fetchone()
        return result if result else None

    def set_hint_text(self, input_field, hint_text):
        input_field.hint_text = hint_text if hint_text else ""  # Ensure hint_text is not None
        input_field.hint_text_color = (0, 0, 0, 1)  # Black color for hint text

    def go_to_next_screen(self, instance):
        self.manager.current = 'recruiter_edit_page2'  # Make sure this matches the name of RecruiterEditPage2

    def save_changes(self, instance):
        name = self.name_input.text if self.name_input.text else self.name_input.hint_text
        dob = self.dob_input.text if self.dob_input.text else self.dob_input.hint_text
        address = self.address_input.text if self.address_input.text else self.address_input.hint_text
        rec_desig = self.rec_desig_input.text if self.rec_desig_input.text else self.rec_desig_input.hint_text
        rec_dept = self.rec_dept_input.text if self.rec_dept_input.text else self.rec_dept_input.hint_text
        exp_years = self.exp_years_input.text if self.exp_years_input.text else self.exp_years_input.hint_text
        mob_no = self.mob_no_input.text if self.mob_no_input.text else self.mob_no_input.hint_text
        email = self.email_input.text if self.email_input.text else self.email_input.hint_text
        avail_job_design = self.avail_job_design_input.text if self.avail_job_design_input.text else self.avail_job_design_input.hint_text
        qualifications = self.qualifications_input.text if self.qualifications_input.text else self.qualifications_input.hint_text
        add_requirements = self.add_requirements_input.text if self.add_requirements_input.text else self.add_requirements_input.hint_text
        company_name = self.company_name_input.text if self.company_name_input.text else self.company_name_input.hint_text

        updated_details = [
            name, dob, address, rec_desig, rec_dept, exp_years, mob_no, email,
            avail_job_design, qualifications, add_requirements, company_name
        ]
        query = """
        UPDATE recruiter
        SET name = %s, dob = %s, address = %s, rec_desig = %s, rec_dept = %s, 
            exp_years = %s, mob_no = %s, email = %s, avail_job_design = %s,
            qualifications = %s, add_requirements = %s, company_name = %s
        WHERE username = %s
        """
        self.cursor.execute(query, (*updated_details, current_username))
        self.db.commit()
        print("Changes saved successfully!")
        """except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:"""
        self.cursor.close()
        self.db.close()
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'recruiter_edit_page2'

class RecruiterEditPage2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=SQLpassword,  # Replace with your actual MySQL password
            database="db1"
        )
        self.cursor = self.db.cursor()

        # Initialize TextInput fields for second screen
        self.basic_pay_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.certifications_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.req_exp_years_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.industrial_sector_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.mow_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.job_style_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.age_constraints_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.shift_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.working_hours_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.overall_description_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))
        self.profile_picture_input = TextInput(multiline=False, background_color=(0.8, 0.85, 1.0, 1.0))

        # Layout setup using GridLayout for second screen
        layout = GridLayout(cols=1, spacing=10, padding=[15, 20])
        with layout.canvas.before:
            Color(0, 34/255, 102/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(text='EDIT PROFILE', bold=True, font_size=40, size_hint=(0.5, None), size=(400, 50),
                            color=(0.8, 1.0, 0.0))
        layout.add_widget(title_label)

        form_layout = GridLayout(cols=2, spacing=10)
        fields = [
            (" ", Label(text=" ", font_size=20)),
            ("Basic Pay:", self.basic_pay_input),
            ("Certifications:", self.certifications_input),
            ("Required Experience (Years):", self.req_exp_years_input),
            ("Industrial Sector:", self.industrial_sector_input),
            ("Mode of Working:", self.mow_input),
            ("Job Style:", self.job_style_input),
            ("Age Constraints:", self.age_constraints_input),
            ("Shift:", self.shift_input),
            ("Working Hours:", self.working_hours_input),
            ("Overall Description:", self.overall_description_input),
            ("Profile Picture Path:", self.profile_picture_input),
        ]

        for label, widget in fields:
            if label == "RECRUITER DETAILS":
                label_widget = Label(text=label, font_size=26, bold=True, color=(1, 0, 1, 1))
                form_layout.add_widget(label_widget)
            else:
                label_widget = Label(text=label, font_size=23, bold=True)
                form_layout.add_widget(label_widget)
            form_layout.add_widget(widget)

        # Load existing data from the database for second screen
      # Replace with actual logic to get current user
        recruiter_data = self.edit_recruiter_profile(current_username)
        if recruiter_data:
            self.set_hint_text(self.basic_pay_input, str(recruiter_data[12]) if recruiter_data[12] else '')
            self.set_hint_text(self.certifications_input, recruiter_data[13])
            self.set_hint_text(self.req_exp_years_input, str(recruiter_data[14]) if recruiter_data[14] else '')
            self.set_hint_text(self.industrial_sector_input, recruiter_data[15])
            self.set_hint_text(self.mow_input, recruiter_data[16])
            self.set_hint_text(self.job_style_input, recruiter_data[17])
            self.set_hint_text(self.age_constraints_input, recruiter_data[18])
            self.set_hint_text(self.shift_input, recruiter_data[19])
            self.set_hint_text(self.working_hours_input, recruiter_data[20])
            self.set_hint_text(self.overall_description_input, recruiter_data[21])
            self.set_hint_text(self.profile_picture_input, recruiter_data[25] if recruiter_data[25] else '')
        button_layout = FloatLayout(size_hint_y=None, height=100)
        save_button = Button(text='Save Changes', color=(0.8, 1.0, 0.0), bold=True, font_size=22,
                             size_hint=(None, None), size=(250, 75), pos_hint={'center_x': 0.85, 'center_y': 0.5},
                             on_press=self.save_changes)
        back_button = Button(text='Back', bold=True, size_hint=(None, None), size=(250, 75),
                             pos_hint={'center_x': 0.15, 'center_y': 0.5}, color=(0.8, 1.0, 0.0),
                             background_color=(0.9, 0.95, 1.0, 1.0), on_press=self.back_page)
        choose_button = Button(text='Choose', size_hint=(None, None), size=(100, 44))
        choose_button.bind(on_release=self.open_file_dialog)
        button_layout.add_widget(back_button)
        button_layout.add_widget(save_button)
        form_layout.add_widget(Label(text=" "))
        form_layout.add_widget(choose_button)
        layout.add_widget(form_layout)
        layout.add_widget(button_layout)
        self.add_widget(layout)
    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction ="right")
        self.manager.current = 'recruiter_edit_page1'
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def edit_recruiter_profile(self, username):
        self.cursor.execute("SELECT * FROM recruiter WHERE username=%s", (username,))
        result = self.cursor.fetchone()
        return result if result else None
    def set_hint_text(self, input_field, hint_text):
        input_field.hint_text = str(hint_text) if hint_text else ""  # Ensure hint_text is not None
        input_field.hint_text_color = (0, 0, 0, 1)  # Black color for hint text
    def open_file_dialog(self, instance):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Profile Picture",
                                               filetypes=(("Image Files", "*.jpg *.png"), ("All Files", "*.*")))
        if file_path:
            self.profile_picture_input.text = file_path
        root.destroy()  # Destroy the root window after selection
    def save_changes(self, instance):
          # Replace with actual logic to get current user
        basic_pay = self.basic_pay_input.text if self.basic_pay_input.text else self.basic_pay_input.hint_text
        certifications = self.certifications_input.text if self.certifications_input.text else self.certifications_input.hint_text
        req_exp_years = self.req_exp_years_input.text if self.req_exp_years_input.text else self.req_exp_years_input.hint_text
        industrial_sector = self.industrial_sector_input.text if self.industrial_sector_input.text else self.industrial_sector_input.hint_text
        mow = self.mow_input.text if self.mow_input.text else self.mow_input.hint_text
        job_style = self.job_style_input.text if self.job_style_input.text else self.job_style_input.hint_text
        age_constraints = self.age_constraints_input.text if self.age_constraints_input.text else self.age_constraints_input.hint_text
        shift = self.shift_input.text if self.shift_input.text else self.shift_input.hint_text
        working_hours = self.working_hours_input.text if self.working_hours_input.text else self.working_hours_input.hint_text
        overall_description = self.overall_description_input.text if self.overall_description_input.text else self.overall_description_input.hint_text
        profile_picture = self.profile_picture_input.text if self.profile_picture_input.text else self.profile_picture_input.hint_text
        updated_details = [
        basic_pay, certifications, req_exp_years, industrial_sector, mow, job_style,
        age_constraints, shift, working_hours, overall_description, profile_picture, current_username
        ]
        query = """
        UPDATE recruiter
        SET basic_pay = %s, certifications = %s, req_exp_years = %s, industrial_sector = %s,
            mow = %s, job_style = %s, age_constraints = %s, shift = %s, working_hours = %s,
            overall_description = %s, profile_picture_path = %s
        WHERE username = %s
        """
        try:
            self.cursor.execute(query, updated_details)
            self.db.commit()
            print("Changes saved successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()
            self.db.close()

class Recruiter_ChatPage(BoxLayout):
    def __init__(self, **kwargs):
        super(Recruiter_ChatPage, self).__init__(**kwargs)
        self.clear_widgets()
        self.layout = BoxLayout(orientation='vertical', padding=[30], spacing=10)
        with self.layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.88, 0.93, 1, 1)  # sky blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.layout.bind(size=self._update_rect, pos=self._update_rect)
        
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.message_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.message_list.bind(minimum_height=self.message_list.setter('height'))
        self.scroll_view.add_widget(self.message_list)
    
        self.input_box = BoxLayout(size_hint=(1, 0.1))
        self.text_input = TextInput(size_hint=(0.8, 1), hint_text="Chat with Admin!")
        self.send_button = Button(text='Send', font_size=20, size_hint=(0.2, 1), color=[0.8, 0.8, 0.8, 1], background_color=[0, 0, 139, 1])
        self.send_button.bind(on_press=self.send_message)
        self.back_button = Button(text='back', font_size=20, size_hint=(0.1, 1), color=[0.8, 0.8, 0.8, 1], background_color=[0, 0, 139, 1])
        self.back_button.bind(on_press=self.go_back)
        self.input_box.add_widget(self.text_input)
        self.input_box.add_widget(self.send_button)
        self.input_box.add_widget(self.back_button)
        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.input_box)
    
        threading.Thread(target=self.connect_to_server, daemon=True).start()
        self.add_widget(self.layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_back(self, instance):
        self.manager.current = 'recruiter_home_page'
    
    def connect_to_server(self):
        try:
            sio.connect('http://127.0.0.1:5000/')  # Use your actual server URL
            sio.on('connect', self.on_connect)
            sio.on('disconnect', self.on_disconnect)
            sio.on('message', self.receive_message)
        except Exception as e:
            print(f"Connection error: {e}")

    def on_connect(self):
        print("Connected to server")
        self.is_connected = True

    def on_disconnect(self):
        print("Disconnected from server")
        self.is_connected = False

    def send_message(self, instance):
        message = self.text_input.text
        self.sent_msg = message
        if message:
            sio.send(message)
            self.text_input.text = ''
        boxlay = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        label = Button(text=f"{current_username} : {message}", 
                      font_size=20, 
                      size_hint_x=0.5, 
                      size_hint_y=None, 
                      height=40, 
                      halign='right', 
                      #valign='right', 
                      color=[1, 1, 1, 1],
                      background_color=[0, 1, 0, 1] )
        label2 = Label(text='', size_hint_x=0.5, size_hint_y=None, height=40)
        boxlay.add_widget(label2)
        boxlay.add_widget(label)
        
        self.message_list.add_widget(boxlay)
        self.scroll_view.scroll_to(label)

    def receive_message(self, msg):
        if self.sent_msg:
            if self.sent_msg == msg:
                self.sent_msg = ''
                return
        self.add_message_to_ui("Admin : "+msg, "received")

    @mainthread
    def add_message_to_ui(self, msg, msg_type):
        if msg_type == "received":
            boxlay = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            label = Button(text=msg, 
                           font_size=20, 
                           size_hint_x=0.5, 
                           size_hint_y=None,
                           height=40, 
                           halign='left', 
                           #valign='left', 
                           color=[1, 1, 1, 1],
                           background_color=[0, 1, 1, 1])
            label2 = Label(text='', size_hint_x=0.5, size_hint_y=None, height=40, halign='left', valign='center')
            boxlay.add_widget(label)
            boxlay.add_widget(label2)
        self.message_list.add_widget(boxlay)
        self.scroll_view.scroll_to(label)

class RecruiterHomePage(Screen):
    def __init__(self,**kwargs):
        super(RecruiterHomePage, self).__init__(**kwargs)
    def on_enter(self, *args):
        with self.canvas.before:
            Color(0.88, 0.93, 1, 1)  # Whitish sky blue color
            self.rect = Rectangle(size=self.size, pos=self.pos)       
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.homepage_layout = BoxLayout(orientation='vertical')
        self.homepage_layout.add_widget(Label(text="WELCOME      "+str(current_username)+" !!!!",
                                      bold=True,
                                      font_size='35',
                                      size_hint=(1, 0.1),
                                      color=(1, 0, 0, 1),
                                      font_name='Roboto-BoldItalic'))
          # Adjust font_size as needed
        
        navbar_layout = BoxLayout(size_hint=(1, 0.1))

        self.recommendationpage = Recruiter_RecommendationsPage(home_screen=self)
        self.searchpage = Recruiter_SearchPage(home_screen=self)
        self.chatpage = Recruiter_ChatPage()
        self.current_page = self.recommendationpage

        navbar_layout.add_widget(
            Button(text='Recommendations', 
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   on_press=lambda instance: self.switch_page(self.recommendationpage),
                   )
            )
        navbar_layout.add_widget(
            Button(text='Search Bar',
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   on_press=lambda instance: self.switch_page(self.searchpage),
                   )
            )
        
        navbar_layout.add_widget(
            Button(text='Chat Page',
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   on_press=lambda instance: self.switch_page(self.chatpage),
                   )
            )
        
        navbar_layout.add_widget(
            Button(text='Edit Profile',
                   size_hint=(0.25, 1),
                   background_color=(0.53, 0.81, 0.92, 1),
                   on_press=lambda instance: self.gotoEditPage(),
                   )
            )
        
        self.button_layout = FloatLayout(size_hint_y=None, height=100)
        back_button = Button(text='Logout',bold = True,size_hint=(None, None),size=(250, 50),background_color=(0, 0, 0.5, 1), pos_hint={'center_x': 0.8, 'center_y': 0.5},on_press = self.back_page)
        self.button_layout.add_widget(back_button)

        
        self.homepage_layout.add_widget(navbar_layout)
        self.homepage_layout.add_widget(self.current_page)
        self.homepage_layout.add_widget(self.button_layout)        
        self.add_widget(self.homepage_layout)

    def on_leave(self, *args):
        if self.homepage_layout:
            self.remove_widget(self.homepage_layout)
            self.homepage_layout = None

    def switch_page(self, to_page):
        self.homepage_layout.remove_widget(self.current_page)
        self.homepage_layout.remove_widget(self.button_layout)
        self.current_page = to_page
        self.homepage_layout.add_widget(self.current_page)
        self.homepage_layout.add_widget(self.button_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gotoEditPage(self):
        self.manager.transition = SlideTransition(direction ="left")
        self.manager.current = 'recruiter_edit_page1'

    def back_page(self,instance):
        self.manager.transition = SlideTransition(direction ="right")
        jobseeker_record.clear()
        recruiter_record.clear()
        self.manager.current='recruiter_login'

class Display_Recruiter_Resume_1(Screen):
    def __init__(self, **kwargs):
        super(Display_Recruiter_Resume_1, self).__init__(**kwargs)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def disp_resume(self, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15, Data16, Data17, Data18, Data19, Data20, Data21, Data22):
        layout = GridLayout(cols=1, spacing=10, padding=[50, 20])
        with layout.canvas.before:
            Color(0.88, 0.93, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        profile_picture = Image(source=str(Data11), size=(100, 100), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(profile_picture)
        
        form_layout = GridLayout(cols=1, spacing=10, padding=[20, 20], size_hint_y=None, height=800)

        def create_label(text, color=(0, 0, 0, 1), bold=False, **kwargs):
            label = Label(text=text, color=color, bold=bold, halign='left', valign='middle', text_size=(self.width - 100, None), **kwargs)
            label.bind(size=label.setter('text_size'))
            return label

        form_layout.add_widget(create_label("Name:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data1)))
        form_layout.add_widget(create_label("Address:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data3)))
        form_layout.add_widget(create_label("Designation, Department, Location:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data4, Data5, Data12)))
        form_layout.add_widget(create_label("Contact:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data8, Data7)))
        form_layout.add_widget(create_label("Available Job Designation:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data9)))
        form_layout.add_widget(create_label("Required Qualifications:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data10)))
        form_layout.add_widget(create_label("Additional Requirements:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data14)))
        form_layout.add_widget(create_label("Job Details:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("Job in {} Sector, {} mode with minimum {} years of experience, {} shift with working hours of {}".format(Data16, Data17, Data15, Data20, Data21)))
        form_layout.add_widget(create_label("Overall Job Description:", color=(1, 0, 0, 1), bold=True))
        form_layout.add_widget(create_label("{}".format(Data22)))

        # Add some spacing
        for _ in range(4):
            form_layout.add_widget(Label(text=""))

        layout.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=700, padding=[20, 10, 20, 10])

        back_button = Button(text='Back', color=(0.8, 1.0, 0.0), bold=True, font_size=23, size_hint=(None, None), size=(200, 75), on_press=self.back_page)
        next_button = Button(text='Apply', color=(0.8, 1.0, 0.0), bold=True, font_size=23, size_hint=(None, None), size=(200, 75), on_press=self.next_page)

        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        self.add_widget(layout)
        self.add_widget(button_layout)

    def next_page(self, instance):
        print("JS RECORD:",jobseeker_record)
        print("rec RECORD:",recruiter_record)
        x=Mail_functions.Apply_email_j2r(jobseeker_record,recruiter_record)
        if x==1:
            print("Application sent!")

    def back_page(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'job_seeker_home_page'

""" MODULE OF MAIN APPLICATION """

class DesignApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(JobSeekerLoginScreen(name='job_seeker_login'))
        sm.add_widget(RecruiterLoginScreen(name='recruiter_login'))
        sm.add_widget(RegisterScreenPart1(name='register_part_1'))
        sm.add_widget(RegisterScreenPart2(name='register_part_2'))
        sm.add_widget(RegisterScreenPart3(name='register_part_3'))
        sm.add_widget(UsernamePasswordJobSeeker(name='Username_jobseeker'))
        sm.add_widget(RecruiterRegisterPart1(name='recruiter_register_1'))
        sm.add_widget(RecruiterRegisterPart2(name='recruiter_register_2'))
        sm.add_widget(RecruiterRegisterPart3(name='recruiter_register_3'))
        sm.add_widget(RecruiterRegisterPart4(name='recruiter_register_4'))
        sm.add_widget(UsernamePasswordRecruiter(name='Username_recruiter'))
        sm.add_widget(ForgotPasswordJobSeeker(name='forgot_password_jobseeker'))
        sm.add_widget(ChangePasswordJobseeker(name='change_password_jobseeker'))
        sm.add_widget(ForgotPasswordRecruiter(name='forgot_password_recruiter'))
        sm.add_widget(ChangePasswordRecruiter(name='change_password_recruiter'))
        sm.add_widget(JobSeekerHomePage(name="job_seeker_home_page"))
        sm.add_widget(RecruiterHomePage(name="recruiter_home_page"))
        sm.add_widget(Display_JobSeeker_Resume_1(name='jobseeker_resume_1'))
        sm.add_widget(Display_Recruiter_Resume_1(name='recruiter_resume_1'))
        sm.add_widget(Recruiter_SearchResults(name='recruiter_searchresults')) #changes
        sm.add_widget(JobSeeker_SearchResults(name='jobseeker_searchresults')) #changes
        sm.add_widget(RecruiterEditPage1(name='recruiter_edit_page1'))
        sm.add_widget(RecruiterEditPage2(name='recruiter_edit_page2'))
        sm.add_widget(JobSeekerEditPage1(name='jobseeker_edit_page1'))
        sm.add_widget(JobSeekerEditPage2(name='jobseeker_edit_page2'))
        return sm

if __name__ == '__main__':
    DesignApp().run() 