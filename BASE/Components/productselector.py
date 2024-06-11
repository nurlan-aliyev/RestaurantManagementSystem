import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from database import Database


class ProductSelector(tk.Frame):
    def __init__(self, parent, root_frame, row, func):
        self.func = func
        tk.Frame.__init__(self, parent)

        self.init_database()

        self.menuBtn = ttk.Menubutton(root_frame, text="Select a meal")

        self.menu = tk.Menu(self.menuBtn, tearoff=0)
        self.m_var1 = tk.StringVar()
        self.m_var1.set("Select a meal")
        self.retrieve_products()
        self.menuBtn['menu'] = self.menu

        self.menuBtn.grid(column=0, row=row, padx=(15, 85), sticky=tk.W)

        self.pr_qty_var = tk.StringVar(root_frame)
        self.pr_qty_var.set("1")
        self.spin_box = ttk.Spinbox(
            root_frame,
            from_=1,
            to=100,
            textvariable=self.pr_qty_var,
            wrap=True,
            width=5,
            state=tk.DISABLED,
        )
        self.spin_box.grid(column=1, row=row)

        self.order_st_lb = ttk.Label(root_frame,  text="Choosing")
        self.order_st_lb.grid(column=2, row=row, padx=(110, 10))

        self.del_icon_png = Image.open(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'delete.png'))
        self.del_icon_res = self.del_icon_png.resize(
            (18, 18), Image.Resampling.LANCZOS)
        self.del_icon = ImageTk.PhotoImage(self.del_icon_res)
        self.destroy_btn = ttk.Button(
            root_frame, image=self.del_icon, width=10, command=self.destroy_all)
        self.destroy_btn.image = self.del_icon
        self.destroy_btn.grid(column=3, row=row, padx=(10, 0))

    def init_database(self):
        self.fac_db = Database("restaurant.db")

    def retrieve_products(self):
        load_query = """SELECT * FROM menu_config"""
        result = self.fac_db.read_val(load_query)
        for row in result:
            pr_lbl = row[1]
            self.menu.add_radiobutton(
                label=pr_lbl, variable=self.m_var1, command=self.sel)

    def pad_num(self):
        var_len = len(self.m_var1.get())
        return 165 - ((var_len - 1) * 7.5)

    def sel(self):
        selx = self.m_var1.get()
        self.menuBtn.config(text=selx)
        self.pad_n = self.pad_num()
        self.order_updt()

    def retrieve_data(self):
        return (self.m_var1.get(), self.pr_qty_var.get())

    def order_updt(self):
        self.order_st_lb.config(text="Ordered")
        self.spin_box.config(state=tk.ACTIVE)
        self.spin_box.config(textvariable=self.pr_qty_var)
        self.menuBtn.grid_configure(padx=(15, self.pad_n))

    def destroy_all(self):
        super().destroy()
        self.menuBtn.destroy()
        self.menu.destroy()
        self.spin_box.destroy()
        self.order_st_lb.destroy()
        self.destroy_btn.destroy()
        self.func()
