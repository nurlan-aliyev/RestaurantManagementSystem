import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image 
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

from configwindow import ConfigWindow
from kitchenwindow import KitchenWindow  
from customerwindow import CustomerWindow
from aboutwindow import AboutWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.win_width = 600
        self.win_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)
        self.title('Restaurant Management System')

        m_frame = ttk.Frame(self, width=600, height=400)
        m_frame.grid(row=0, column=0,  sticky=tk.NSEW)

        self.iconphoto(True, tk.PhotoImage(file='C:/Users/N/Desktop/PYTHON_BME/pythonProject/HW/assets/icon_m.png'))

        menubar = tk.Menu(m_frame)
        filebar = tk.Menu(menubar, tearoff=0)
        filebar.add_cascade(label="Kitchen Receipt", command=self.kitchen_win)
        filebar.add_cascade(label="Customer Receipt", command=self.customer_win)
        filebar.add_cascade(label="Configure", command=self.config_window)
        filebar.add_separator()
        filebar.add_cascade(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filebar)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.about_win)
        menubar.add_cascade(label="About", menu=helpmenu)

        self.config(menu=menubar)

        img = Image.open("C:\\Users\\N\\Desktop\\PYTHON_BME\\pythonProject\\HW\\assets\\main_win_ph.png")
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(m_frame, image = img, text="Restaurant Management System", compound='top', font=("Helvetica Bold", 20))
        panel.image = img
        panel.grid(row=0, column=0, sticky=tk.NSEW, padx=60, pady=35)

        vers = tk.Label(m_frame, text="v0.1, N.A", font=("Helvetica", 8))
        vers.grid(row=1, column=0, sticky=tk.SW, padx=10)


    def config_window(self):
        config_window = ConfigWindow(self)
        config_window.grab_set()
    def kitchen_win(self):
        kitchen_win = KitchenWindow(self)
        kitchen_win.grab_set()
    def customer_win(self):
        customer_win = CustomerWindow(self)
        customer_win.grab_set()
    def about_win(self):
        about_win = AboutWindow(self)
        about_win.grab_set()

