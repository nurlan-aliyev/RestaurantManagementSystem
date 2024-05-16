import tkinter as tk
from tkinter import ttk

from orderedproducts import OrderedProducts
from database import Database


class KitchenWindow(tk.Toplevel):
    def __init__(self, parent, func):
        super().__init__(parent)
        self.func = func
        self.init_database()

        self.win_width = 625
        self.win_height = 390
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(
            f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Restaurant Management System')
        self.resizable(0, 0)

        self.orders = []

        # main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=15, pady=10)

        # Label
        self.kt_lb = ttk.LabelFrame(self.main_frame, text="Kitchen receipt")
        self.kt_lb.grid(column=0, row=0, sticky=tk.NSEW, columnspan=3)

        # notebook
        self.nt = ttk.Notebook(self.kt_lb)
        self.nt.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)
        self.add_widgets()

    def destroy(self):
        super().destroy()
        self.func()

    def init_database(self):
        self.fac_db = Database("restaurant.db")

    def add_widgets(self):
        retrieve_query = """SELECT table_num FROM orders GROUP BY table_num"""
        res = self.fac_db.read_val(retrieve_query)
        for r in reversed(res):
            self.retrieve_pr(r[0])

    def retrieve_pr(self, table_num):
        self.op = OrderedProducts(
            self.main_frame, self.nt, self.kt_lb, str(table_num), self.destroy)
