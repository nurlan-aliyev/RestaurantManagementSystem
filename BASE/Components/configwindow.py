import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import Database


class ConfigWindow(tk.Toplevel):
    def __init__(self, parent, func):
        super().__init__(parent)
        self.func = func
        self.init_database()

        self.win_width = 500
        self.win_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.i = 5

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(
            f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Restaurant Management System')
        self.resizable(False, False)
        # main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        # up frame
        self.up_frame = ttk.Frame(self.main_frame)
        self.up_frame.grid(column=0, row=0, sticky=tk.NSEW)

        # down frame
        self.down_frame = ttk.Frame(self.main_frame)
        self.down_frame.grid(column=0, row=1, sticky=tk.NSEW)

        # Facility Label frame
        self.fac_config_lf = ttk.LabelFrame(
            self.up_frame, text="Facility Configuration")
        self.fac_config_lf.grid(
            column=0,
            row=0,
            pady=5,
            rowspan=4,
            columnspan=3,
            sticky=tk.EW
        )

        # Labels
        self.fc_name_lb = ttk.Label(self.fac_config_lf, text="Facility Name:")
        self.fc_name_lb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        # fc_icon_lb = ttk.Label(fac_config_lf, text="Facility Icon")
        # fc_icon_lb.grid(column=0, row=2, sticky=tk.W, padx=15, pady=15)

        self.fc_table_num_lb = ttk.Label(
            self.fac_config_lf,
            text="Number of Tables:"
        )
        self.fc_table_num_lb.grid(
            column=0,
            row=2,
            sticky=tk.W,
            padx=10,
            pady=10
        )

        self.fc_seat_num_lb = ttk.Label(
            self.fac_config_lf,
            text="Number of Seats:"
        )
        self.fc_seat_num_lb.grid(
            column=0,
            row=3,
            sticky=tk.W,
            padx=10,
            pady=10
        )

        # Entries
        self.fc_name_ent = ttk.Entry(self.fac_config_lf)
        self.fc_name_ent.grid(column=1, row=1, sticky=tk.E, padx=15)

        # fc_icon_ent = ttk.Entry(fac_config_lf)
        # fc_icon_ent.grid(column=1, row=2, sticky=tk.E, padx=15)

        vcmd_t = (self.register(self.callback_table))
        vcmd_s = (self.register(self.callback_seats))

        self.fc_table_num_ent = ttk.Entry(
            self.fac_config_lf,
            validate='all',
            validatecommand=(vcmd_t, "%P")
        )
        self.fc_table_num_ent.grid(column=1, row=2, sticky=tk.E, padx=15)

        self.fc_seat_num_ent = ttk.Entry(
            self.fac_config_lf,
            validate='all',
            validatecommand=(vcmd_s, "%P")
        )
        self.fc_seat_num_ent.grid(column=1, row=3, sticky=tk.E, padx=15)

        # buttons
        self.fc_save_btn = ttk.Button(
            self.fac_config_lf, text="Save", command=self.save_fac_config)
        self.fc_save_btn.grid(column=2, row=1, pady=5, padx=15)

        self.fc_load_btn = ttk.Button(
            self.fac_config_lf,
            text="Load",
            command=self.load_fac_config,
            state=tk.DISABLED
        )
        self.fc_load_btn.grid(column=2, row=2, pady=5, padx=15)

        self.fc_clear_btn = ttk.Button(
            self.fac_config_lf,
            text="Clear",
            command=self.fac_conf_clear,
            state=tk.DISABLED
        )
        self.fc_clear_btn.grid(column=2, row=3, pady=5, padx=15)

        # Menu Label Frame
        self.menu_conf_lf = ttk.LabelFrame(
            self.down_frame, text="Menu Configuration")
        # self.menu_conf_lf.config(width=450)
        self.menu_conf_lf.grid(column=0, row=0)

        # TreeView

        self.tr_v_vscr = ttk.Scrollbar(self.menu_conf_lf, orient="vertical")

        self.tr_view_columns = ('id', 'name', 'price')
        self.tr_view = ttk.Treeview(
            self.menu_conf_lf,
            columns=self.tr_view_columns,
            show='headings',
            height=8,
            selectmode='browse',
            yscrollcommand=self.tr_v_vscr.set
        )
        self.tr_view.column('id', width=50, anchor=tk.CENTER)
        self.tr_view.column('name', width=200, anchor=tk.CENTER)
        self.tr_view.column('price', width=200, anchor=tk.CENTER)

        self.tr_view.heading('id', text="ID")
        self.tr_view.heading('name', text="Name")
        self.tr_view.heading('price', text="Price(ft)")

        self.tr_view.grid(column=0, row=0, rowspan=6, columnspan=3, pady=10)

        self.tr_v_vscr.config(command=self.tr_view.yview)
        self.tr_v_vscr.grid(column=3, row=0, rowspan=6,  sticky=tk.NS)

        self.tr_view.bind('<ButtonRelease-1>', self.product_selected)
        self.tr_view.bind('<Delete>', self.remove_selected)

        # add product labelframe
        self.add_prd_lbf = ttk.LabelFrame(
            self.menu_conf_lf, text="Add product")
        self.add_prd_lbf.grid(column=0, row=7, pady=10,
                              padx=5,  columnspan=3, sticky=tk.EW)

        self.remove_prd_lbf = ttk.LabelFrame(
            self.menu_conf_lf, text="Remove product")
        self.remove_prd_lbf.grid(
            column=0, row=8, pady=10, padx=5,  columnspan=3, sticky=tk.EW)

        # Label and entrys

        self.food_name_lbl = ttk.Label(
            self.add_prd_lbf, text="Name of the product:")
        self.food_name_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

        self.food_price_lbl = ttk.Label(
            self.add_prd_lbf, text="Price of the product:")
        self.food_price_lbl.grid(
            column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.food_name_entry = ttk.Entry(self.add_prd_lbf)
        self.food_name_entry.grid(column=1, row=0, pady=10, padx=10)

        self.food_price_entry = ttk.Entry(self.add_prd_lbf)
        self.food_price_entry.grid(column=1, row=1, pady=10, padx=10)

        self.pr_id_lbl = ttk.Label(
            self.remove_prd_lbf, text="Product Selected:")
        self.pr_id_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

        self.sel_pr_id_lbl = ttk.Label(self.remove_prd_lbf, text="")
        self.sel_pr_id_lbl.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        # btn tr
        self.tr_view_add = ttk.Button(
            self.add_prd_lbf, text="Add", command=self.add_record)
        self.tr_view_add.grid(column=2, row=0, rowspan=2, padx=10)

        self.tr_view_add.bind('<Return>', self.add_record)

        self.tr_view_remove = ttk.Button(
            self.remove_prd_lbf,
            text="Remove",
            command=self.remove_selected,
            state=tk.DISABLED
        )
        self.tr_view_remove.grid(column=2, row=0, padx=10, sticky=tk.E)

        self.check_if_empty_database()
        self.check_if_empty_fc_entry()
        self.retreive_menu_items()

    def retreive_menu_items(self):
        load_query = """SELECT * FROM menu_config"""
        result = self.fac_db.read_val(load_query)
        if len(result) > 0:
            for el in result:
                self.tr_view.insert('', tk.END, iid=f"{el[0]}", values=el)
        else:
            self.tr_view_remove.config(state=tk.DISABLED)

    def get_product_id(self):
        res = self.tr_view.get_children()
        if res:
            return res[-1]
        else:
            return 1

    def init_database(self):
        self.fac_db = Database("restaurant.db")
        fac_conf_query = """
        CREATE TABLE IF NOT EXISTS fac_config(
            id integer PRIMARY KEY,
            fac_name text NOT NULL,
            table_num integer NOT NULL,
            seat_num integer NOT NULL
        );
        """

        menu_conf_query = """
        CREATE TABLE IF NOT EXISTS menu_config(
            id integer PRIMARY KEY,
            product_name text NOT NULL,
            product_price real NOT NULL
        );
        """

        self.fac_db.create_table(fac_conf_query)
        self.fac_db.create_table(menu_conf_query)

    def check_if_empty_database(self):
        load_query = """SELECT * FROM fac_config"""
        result = self.fac_db.read_val(load_query)
        if len(result) > 0:
            f_name = result[0][1]
            t_num = result[0][2]
            s_num = result[0][3]

            if f_name and t_num and s_num:
                self.fc_load_btn.config(state=tk.ACTIVE)
            else:
                self.fc_load_btn.config(state=tk.DISABLED)
                self.tr_view_remove.config(state=tk.DISABLED)

    def check_if_empty_fc_entry(self):
        f_name = self.fc_name_ent.get()
        t_num = self.fc_table_num_ent.get()
        s_num = self.fc_seat_num_ent.get()

        if f_name and t_num and s_num:
            self.fc_clear_btn.config(state=tk.ACTIVE)
        else:
            self.fc_clear_btn.config(state=tk.DISABLED)

    def product_selected(self, event):
        try:
            selected_item = self.tr_view.selection()[0]
            sel_item_val = self.tr_view.item(selected_item)['values']
            sel_pr_txt = f"{sel_item_val[0]}) {sel_item_val[1]} {sel_item_val[2]}"
            self.sel_pr_id_lbl.config(text="")
            self.sel_pr_id_lbl.config(text=sel_pr_txt)
            self.tr_view_remove.config(state=tk.ACTIVE)
        except IndexError as e:
            print(e)

    def fac_conf_clear(self):
        self.fc_name_ent.delete(0, tk.END)
        self.fc_seat_num_ent.delete(0, tk.END)
        self.fc_table_num_ent.delete(0, tk.END)

        self.fc_clear_btn.config(state=tk.DISABLED)

    def callback_table(self, P):
        if (str.isdigit(P) and int(P) <= 50) or P == "":
            return True
        else:
            messagebox.showerror(
                "Input Error", "Maximum number of tables must not exceed 50!")
            return False

    def callback_seats(self, P):
        max_table_num = int(self.fc_table_num_ent.get()) * 8
        if (str.isdigit(P) and int(P) <= max_table_num) or P == "":
            return True
        else:
            messagebox.showerror(
                "Input Error", f"Maximum number of seats cannot exceed {max_table_num}")
            return False

    def validate_product(self, price, name):
        if (self.is_float(price) and float(price) <= 10000000) and (len(name) <= 20):
            return True
        elif (self.is_float(price) and float(price) > 10000000) and (len(name) <= 20):
            usr_resp = messagebox.askyesno(
                "Overprice Check", "The price you have entered exceeds maximum allowed (10 million Forints), do you wish to continue?")
            if usr_resp:
                return True
            else:
                self.food_price_entry.delete(0, tk.END)
                return False
        elif (self.is_float(price) and float(price) > 10000000) and (len(name) > 20):
            usr_resp = messagebox.showerror(
                "Wrong inputs", "The price you have entered exceeds maximum allowed (10 million Forints) and product name should be less than 20 characters long")
            self.food_price_entry.delete(0, tk.END)
            self.food_name_entry.delete(0, tk.END)
            return False
        else:
            messagebox.showerror(
                "Wrong input", "Please enter the product name(max. 20 characters long) and price(max 10 mln forints) correctly!")
            return False

    def save_fac_config(self):
        load_query = """SELECT * FROM fac_config"""
        result = self.fac_db.read_val(load_query)

        fac_name = self.fc_name_ent.get()
        table_num = self.fc_table_num_ent.get()
        seat_num = self.fc_seat_num_ent.get()

        if fac_name and table_num and seat_num:
            if len(result) >= 1:
                update_query = """UPDATE fac_config
                SET fac_name = ?,
                table_num = ?,
                seat_num = ?,
                WHERE id = ?
                """
                self.fac_db.update(
                    update_query, (fac_name, table_num, seat_num, 1))
            else:
                spec_insert_query = """INSERT INTO fac_config VALUES (?, ?, ?, ?)"""
                self.fac_db.insert_spec_config(
                    spec_insert_query, (1, fac_name, table_num, seat_num))
            self.check_if_empty_database()
            self.check_if_empty_fc_entry()
        else:
            messagebox.showerror(
                "Empty input fields", "Please enter facility name, table number and seat number accordingly!")

    def load_fac_config(self):
        self.fac_conf_clear()
        load_query = """SELECT * FROM fac_config"""
        result = self.fac_db.read_val(load_query)

        self.fc_name_ent.insert(0, result[0][1])
        self.fc_table_num_ent.insert(0, result[0][2])
        self.fc_seat_num_ent.insert(0, result[0][3])
        self.check_if_empty_fc_entry()

    def remove_selected(self, event=""):
        try:
            selected_item = self.tr_view.selection()
            sel_it_ind = selected_item[0]
            delete_query = """DELETE FROM menu_config WHERE id = ?"""
            self.fac_db.delete_val(delete_query, [sel_it_ind])
            for sel_item in selected_item:
                self.tr_view.delete(sel_item)
            self.sel_pr_id_lbl.config(text="")
            self.tr_view_remove.config(state=tk.DISABLED)
        except IndexError as e:
            print(e)

    def add_record(self, event='<Return>'):
        food_name = self.food_name_entry.get()
        food_price = self.food_price_entry.get()
        spec_insert_query = """INSERT INTO menu_config VALUES (?, ?, ?)"""
        pr_id = self.get_product_id()
        pr_ind = pr_id if pr_id == 1 else int(pr_id) + 1
        if food_name and food_price:
            validate_product = self.validate_product(food_price, food_name)
            if validate_product:
                self.tr_view.insert("", tk.END, iid=f"{pr_ind}", values=(
                    pr_ind, food_name, food_price))

                self.fac_db.insert_spec_config(
                    spec_insert_query, (pr_ind, food_name, food_price))
        else:
            er_msg = "Please fill \"Name of the product \" and \"Price of the product\" fields!"
            messagebox.showerror("Empty input fields", er_msg)

        self.food_name_entry.delete(0, tk.END)
        self.food_price_entry.delete(0, tk.END)

    def is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def destroy(self):
        self.func()
        super().destroy()

    def __del__(self):
        self.func()
