import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image 
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS gen_config (id INTEGER PRIMARY KEY, conf_name text);")
        self.conn.commit()

        self.insert_genconfig()
      

    def create_table(self, create_table_query):
        try:
            cursor = self.cur
            cursor.execute(create_table_query)
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_genconfig(self):
        try:
            self.cur.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                            (1, "fac_config"))
            self.cur.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                    (2, "menu_config"))    
            self.cur.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                            (3, "orders"))     
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_spec_config(self, insert_query, values):
        try:
            con = self.cur
            con.execute(insert_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def update(self, update_query, values):
        try:
            con = self.cur
            con.execute(update_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def read_val(self, read_query):
        try:
            con = self.cur
            con.execute(read_query)
            rows = con.fetchall()
            return rows
        except Error as e:
            print(e)
            
    def delete_val(self, delete_query, item_id):
        try:
            con = self.cur
            con.execute(delete_query, item_id)
            self.conn.commit()
        except Error as e:
            print(e)
            

    def __del__(self):
        self.conn.close()

class ConfigWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.init_database()

        self.win_width = 530
        self.win_height = 650
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.i = 5

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Restaurant Management System')
        self.resizable(False, False)
        #main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        #up frame
        self.up_frame = ttk.Frame(self.main_frame)
        self.up_frame.grid(column=0, row=0, sticky=tk.NSEW)

        #down frame
        self.down_frame = ttk.Frame(self.main_frame)
        self.down_frame.grid(column=0, row=1, sticky=tk.NSEW)


        #Facility Label frame
        self.fac_config_lf = ttk.LabelFrame(self.up_frame, text="Facility Configuration")
        self.fac_config_lf.grid(column=0, row=0, pady=5, rowspan=4, columnspan=3, sticky=tk.EW)


        #Labels
        self.fc_name_lb = ttk.Label(self.fac_config_lf, text="Facility Name:")
        self.fc_name_lb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)
        
        # fc_icon_lb = ttk.Label(fac_config_lf, text="Facility Icon")
        # fc_icon_lb.grid(column=0, row=2, sticky=tk.W, padx=15, pady=15)

        self.fc_table_num_lb = ttk.Label(self.fac_config_lf, text="Number of Tables:")
        self.fc_table_num_lb.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        self.fc_seat_num_lb = ttk.Label(self.fac_config_lf, text="Number of Seats:")
        self.fc_seat_num_lb.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

        #Entries
        self.fc_name_ent = ttk.Entry(self.fac_config_lf)
        self.fc_name_ent.grid(column=1, row=1, sticky=tk.E, padx=15)

        # fc_icon_ent = ttk.Entry(fac_config_lf)
        # fc_icon_ent.grid(column=1, row=2, sticky=tk.E, padx=15)

        vcmd_t = (self.register(self.callback_table))
        vcmd_s = (self.register(self.callback_seats))
        
        self.fc_table_num_ent = ttk.Entry(self.fac_config_lf, validate='all', validatecommand=(vcmd_t, "%P"))
        self.fc_table_num_ent.grid(column=1, row=2, sticky=tk.E, padx=15)
        
        self.fc_seat_num_ent = ttk.Entry(self.fac_config_lf, validate='all', validatecommand=(vcmd_s, "%P"))
        self.fc_seat_num_ent.grid(column=1, row=3, sticky=tk.E, padx=15)

        #buttons
        self.fc_save_btn = ttk.Button(self.fac_config_lf, text="Save", command=self.save_fac_config)
        self.fc_save_btn.grid(column=2, row=1, pady=5, padx=15)

        self.fc_load_btn = ttk.Button(self.fac_config_lf, text="Load", command=self.load_fac_config, state=tk.DISABLED)
        self.fc_load_btn.grid(column=2, row=2, pady=5, padx=15)

        self.fc_clear_btn = ttk.Button(self.fac_config_lf, text="Clear", command=self.fac_conf_clear, state=tk.DISABLED)
        self.fc_clear_btn.grid(column=2, row=3, pady=5, padx=15)

        #Menu Label Frame
        self.menu_conf_lf = ttk.LabelFrame(self.down_frame, text="Menu Configuration")
        # self.menu_conf_lf.config(width=450)
        self.menu_conf_lf.grid(column=0, row=0)
        
        #TreeView 

        self.tr_v_vscr = ttk.Scrollbar(self.menu_conf_lf, orient="vertical")


        self.tr_view_columns = ('id', 'name', 'price')
        self.tr_view = ttk.Treeview(self.menu_conf_lf, columns=self.tr_view_columns, show='headings', height=8, selectmode='browse', yscrollcommand=self.tr_v_vscr.set)
        self.tr_view.column('id', width=50, anchor=tk.CENTER)
        self.tr_view.column('name', width=200, anchor=tk.CENTER)
        self.tr_view.column('price', width=200, anchor=tk.CENTER)

        self.tr_view.heading('id', text="ID")
        self.tr_view.heading('name', text="Name")
        self.tr_view.heading('price', text="Price(ft)")

        # for e in self.menu_itms:
        #     self.tr_view.insert('', tk.END, iid=f"{e[0]}",values=e)
        

        self.tr_view.grid(column=0,row=0, rowspan=6, columnspan=3, pady=10)

        self.tr_v_vscr.config(command=self.tr_view.yview)
        self.tr_v_vscr.grid(column=3, row=0, rowspan=6,  sticky=tk.NS)
        
        self.tr_view.bind('<ButtonRelease-1>', self.product_selected)
        self.tr_view.bind('<Delete>', self.remove_selected)

        # add product labelframe
        self.add_prd_lbf = ttk.LabelFrame(self.menu_conf_lf, text="Add product")
        self.add_prd_lbf.grid(column=0, row=7, pady=10, padx=5,  columnspan=3, sticky=tk.EW)

        self.remove_prd_lbf = ttk.LabelFrame(self.menu_conf_lf, text="Remove product")
        self.remove_prd_lbf.grid(column=0, row=8, pady=10, padx=5,  columnspan=3, sticky=tk.EW)

        # Label and entrys

        self.food_name_lbl = ttk.Label(self.add_prd_lbf, text="Name of the product:")
        self.food_name_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

        self.food_price_lbl = ttk.Label(self.add_prd_lbf, text="Price of the product:")
        self.food_price_lbl.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.food_name_entry = ttk.Entry(self.add_prd_lbf)
        self.food_name_entry.grid(column=1, row=0, pady=10, padx=10)

        self.food_price_entry = ttk.Entry(self.add_prd_lbf)
        self.food_price_entry.grid(column=1, row=1, pady=10, padx=10)


        self.pr_id_lbl = ttk.Label(self.remove_prd_lbf, text="Product Selected:")
        self.pr_id_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.sel_pr_id_lbl = ttk.Label(self.remove_prd_lbf, text="")
        self.sel_pr_id_lbl.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        #btn tr
        self.tr_view_add = ttk.Button(self.add_prd_lbf, text="Add", command=self.add_record)
        self.tr_view_add.grid(column=2, row=0, rowspan=2, padx=10)

        self.tr_view_remove = ttk.Button(self.remove_prd_lbf, text="Remove", command=self.remove_selected, state=tk.DISABLED)
        self.tr_view_remove.grid(column=2, row=0,padx=10, sticky=tk.E)
        
        self.check_if_empty_database()
        self.check_if_empty_fc_entry()
        self.retreive_menu_items()
        
    def retreive_menu_items(self):
        load_query = """SELECT * FROM menu_config"""
        result = self.fac_db.read_val(load_query)
        if len(result) > 0:    
            for el in result:
                self.tr_view.insert('', tk.END, iid=f"{el[0]}", values=el)
                
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
            
            if f_name == '' and t_num == '' and s_num == '':
                self.fc_load_btn.config(state=tk.DISABLED)
            else:
                self.fc_load_btn.config(state=tk.ACTIVE)
            
    def check_if_empty_fc_entry(self):
        f_name = self.fc_name_ent.get()
        t_num = self.fc_table_num_ent.get()
        s_num = self.fc_seat_num_ent.get()
        
        if  f_name and  t_num and  s_num:
            self.fc_clear_btn.config(state=tk.ACTIVE)
        else:
            self.fc_clear_btn.config(state=tk.DISABLED)
        
    def product_selected(self, event):
        selected_item = self.tr_view.selection()[0]
        sel_item_val = self.tr_view.item(selected_item)['values']
        sel_pr_txt = f"{sel_item_val[0]}) {sel_item_val[1]} {sel_item_val[2]}"
        self.sel_pr_id_lbl.config(text="")
        self.sel_pr_id_lbl.config(text=sel_pr_txt)
        self.tr_view_remove.config(state=tk.ACTIVE)

    def fac_conf_clear(self):
        self.fc_name_ent.delete(0, tk.END) 
        self.fc_seat_num_ent.delete(0, tk.END)
        self.fc_table_num_ent.delete(0, tk.END)
        
        self.fc_clear_btn.config(state=tk.DISABLED)

    def callback_table(self, P):
        if (str.isdigit(P) and int(P) <= 50) or P == "":
            return True
        else:
            messagebox.showerror("Input Error", "Maximum number of tables must not exceed 50!")
            return False

    def callback_seats(self, P):
        max_table_num = int(self.fc_table_num_ent.get()) * 8
        if (str.isdigit(P) and int(P) <= max_table_num) or P == "":
            return True
        else:
            messagebox.showerror("Input Error", f"Maximum number of seats cannot exceed {max_table_num}")
            return False

    def check_food_price(self, price):
        if ( self.is_float(price) and float(price) <= 10000000) or price == "":
            return True
        elif (self.is_float(price) and float(price) > 10000000):
            usr_resp = messagebox.askyesno("Overprice Check", "The price you have entered exceeds maximum allowed (10 million Forints), do you wish to continue?")
            if usr_resp:
                return True
            else:
                self.food_price_entry.delete(0, tk.END)
                return False
        else:
            messagebox.showerror("Wrong input", "Please enter the price correctly using only numbers!")
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
                seat_num = ?
                WHERE id = ?
                """
                self.fac_db.update(update_query, (fac_name, table_num, seat_num, 1))
            else:
                spec_insert_query = """INSERT INTO fac_config VALUES (?, ?, ?, ?)""" 
                self.fac_db.insert_spec_config(spec_insert_query, (1, fac_name, table_num, seat_num))
            self.check_if_empty_database()
            self.check_if_empty_fc_entry()
        else:
            messagebox.showerror("Empty input fields", "Please enter facility name, table number and seat number accordingly!")
            
    def load_fac_config(self):
        self.fac_conf_clear()
        load_query = """SELECT * FROM fac_config"""
        result = self.fac_db.read_val(load_query)

        self.fc_name_ent.insert(0, result[0][1])
        self.fc_table_num_ent.insert(0, result[0][2])
        self.fc_seat_num_ent.insert(0, result[0][3])
        self.check_if_empty_fc_entry()

    def remove_selected(self, event="<Delete>"):
        selected_item = self.tr_view.selection()
        try:
            sel_it_ind = selected_item[0]
            delete_query = """DELETE FROM menu_config WHERE id = ?"""
        except IndexError as e:
            print(e)
        
        self.fac_db.delete_val(delete_query, sel_it_ind)

        for sel_item in selected_item:
            self.tr_view.delete(sel_item)
        self.sel_pr_id_lbl.config(text="")

    def add_record(self):
        food_name = self.food_name_entry.get()
        food_price = self.food_price_entry.get()
        spec_insert_query = """INSERT INTO menu_config VALUES (?, ?, ?)""" 
        pr_id = self.get_product_id()
        pr_ind = pr_id if pr_id == 1 else int(pr_id) + 1
        if food_name and food_price:
            validate_price = self.check_food_price(food_price)
            if validate_price:
                self.tr_view.insert("", tk.END, iid=f"{pr_ind}", values=(pr_ind, food_name, food_price))
                
                self.fac_db.insert_spec_config(spec_insert_query, (pr_ind, food_name, food_price))
        else:
            er_msg = "Please fill \"Name of the product \" and \"Price of the product\" fields!"
            messagebox.showerror("Empty input fields", er_msg)

        self.food_name_entry.delete(0, tk.END)
        self.food_price_entry.delete(0, tk.END)
        
    def is_float(self,element):
        if element is None: 
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False
        
class KitchenWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.win_width = 650
        self.win_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Restaurant Management System')
        # self.resizable(0, 0)
        #main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=15, pady=10)

        #Label
        self.kt_lb = ttk.LabelFrame(self.main_frame, text="Kitchen receipt")
        self.kt_lb.grid(column=0, row=0, sticky=tk.NSEW, ipadx=10, ipady=10, columnspan=3)

        #notebook
        self.nt = ttk.Notebook(self.kt_lb)
        self.nt.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)

        self.close_btn = ttk.Button(self.main_frame,text='Close',command=self.destroy)
        self.close_btn.grid(column=0, row=7, padx=(0, 0), pady=10)

        self.retrieve_pr()

    def retrieve_pr(self):
        self.op = OrderedProducts(self.main_frame, self.nt, self.kt_lb, "1")

class CustomerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.win_width = 600
        self.win_height = 570
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Restaurant Management System')
        self.resizable(0, 0)

        #main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10, ipady=5, ipadx=5)

        #Labels
        self.cst_lbl  = ttk.LabelFrame(self.main_frame, text="Customer Receipt")
        self.cst_lbl.grid(column=0, row=0, columnspan=4, sticky=tk.NSEW, padx=10) 

        self.pr_sel_lbl = ttk.Frame(self.cst_lbl)
        self.pr_sel_lbl.grid(column=0, row=5, columnspan=4, rowspan=10, sticky=tk.NSEW)

        self.pr_sel_canvas = tk.Canvas(self.pr_sel_lbl, borderwidth=0, width=520, height=400)
        self.pr_sel_canvas.grid(column=0, row=0, sticky=tk.NSEW)

        self.pr_sel_canvas_frm = ttk.Frame(self.pr_sel_canvas)
        self.cst_lbl_scroller = ttk.Scrollbar(self.pr_sel_lbl, command=self.pr_sel_canvas.yview) 
        self.cst_lbl_scroller.grid(column=4, row=0, sticky=tk.NS)
        self.pr_sel_canvas.configure(yscrollcommand=self.cst_lbl_scroller.set)
        
        self.pr_sel_canvas.create_window((5, 5), anchor=tk.NW, window=self.pr_sel_canvas_frm)

        self.pr_sel_canvas_frm.bind("<Configure>", self.onFrameConfig)


        self.fc_name = ttk.Label(self.cst_lbl, text="Restaurant name/icon")
        self.fc_name.grid(column=1, row=0)

        self.tb_name = ttk.Label(self.cst_lbl, text="Table number:")
        self.tb_name.grid(column=1, row=1)

        self.pr_name = ttk.Label(self.cst_lbl, text="Product Name")
        self.pr_name.grid(column=0, row=3)

        self.pr_qty = ttk.Label(self.cst_lbl, text="Quantity")
        self.pr_qty.grid(column=1, row=3)

        self.pr_st = ttk.Label(self.cst_lbl, text="Order Status")
        self.pr_st.grid(column=2, row=3)

        self.row_count = tk.IntVar()
        self.row_count.set(1)

        self.btn_add_product = ttk.Button(self.main_frame, text="Add product", command=self.add_product)
        self.btn_add_product.grid(column=0, row=2, padx=(50,0), pady=10)

        self.close_btn = ttk.Button(self.main_frame,text='Close',command=self.destroy)
        self.close_btn.grid(column=1, row=2, padx=(50,0), pady=10)

        self.send_to_ch = ttk.Button(self.main_frame,text='Send to kitchen', state=tk.DISABLED)
        self.send_to_ch.grid(column=2, row=2, padx=(50,0), pady=10)

        self.tb_name_entry = ttk.Entry(self.cst_lbl, width=4)
        self.tb_name_entry.grid(row=1, column=1, padx=(140,0))



    def add_product(self):
        self.max = self.pr_sel_canvas_frm.grid_size()
        self.row_count.set((self.row_count.get() + 1) if self.row_count.get() >= self.max[1] else self.max[1] + 1)
        self.pr_sl = ProductSelector(self, self.pr_sel_canvas_frm,self.row_count.get(), func=self.des_pr)
        self.send_to_ch.config(state=tk.ACTIVE)
    
    def des_pr(self):
        if len(self.pr_sel_canvas_frm.winfo_children()) == 0:
            self.send_to_ch.config(state=tk.DISABLED)
            self.row_count.set(1)
        self.set_val = self.row_count.get() - 1 if self.row_count.get() > 1 else 1
        self.row_count.set(self.set_val)
    
    def onFrameConfig(self, event):
        self.pr_sel_canvas.configure(scrollregion=self.pr_sel_canvas.bbox("all"))

class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.win_width = 360
        self.win_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)
        self.title('About the application')

        about_lbl = ttk.Label(self, wraplength=300, justify='left', padding=(5,20, 0, 0), font=("Helvetica Bold", 12),text="This application is developed by Aliyev Nurlan as a final project for Programming course of Msc. in Construction Information Technology Engineering. Main functionality of this app involves managing a restaurant system, facilitating the order process between customer an the kitchen chief. Date of development December 2022.")
        about_lbl.pack()

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

class ProductSelector(tk.Frame):
    def __init__(self, parent, root_frame, row, func):
        self.func = func
        tk.Frame.__init__(self, parent)

        self.menuBtn = ttk.Menubutton(root_frame, text="Select a meal")

        self.menu = tk.Menu(self.menuBtn, tearoff=0)
        self.m_var1 = tk.StringVar()
        self.m_var1.set("Select a meal")
        self.menu.add_radiobutton(label="Goulyash", variable=self.m_var1, command=self.sel)
        self.menu.add_radiobutton(label="Borscht", variable=self.m_var1, command=self.sel)
        self.menu.add_radiobutton(label="Varenyky", variable=self.m_var1, command=self.sel)
        self.menu.add_radiobutton(label="SIRNIKI", variable=self.m_var1, command=self.sel)
        self.menuBtn['menu'] = self.menu

        self.menuBtn.grid(column=0, row=row, sticky=tk.W, padx=(15, 0))

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
        self.spin_box.grid(column=1, row=row, sticky=tk.E, padx=(80,0))

        self.order_st_lb = ttk.Label(root_frame,  text="Choosing")
        self.order_st_lb.grid(column=2, row=row, sticky=tk.E, padx=(100, 25))

        self.del_icon_png = Image.open('C:\\Users\\N\\Desktop\\PYTHON_BME\\pythonProject\\HW\\assets\\delete.png')
        self.del_icon_res = self.del_icon_png.resize((18, 18), Image.Resampling.LANCZOS)
        self.del_icon = ImageTk.PhotoImage(self.del_icon_res)
        self.destroy_btn = ttk.Button(root_frame, image=self.del_icon, width=10, command=self.destroy_all)
        self.destroy_btn.image = self.del_icon
        self.destroy_btn.grid(column=3, row=row, sticky=tk.E, padx=0)
    
    def pad_num(self):
        pad_num = 38 -  len(self.m_var1.get())
        return pad_num

    def sel(self):
        selx = self.m_var1.get()
        self.menuBtn.config(text=selx)
        self.pad_n = self.pad_num()
        self.order_updt()

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

class OrderedProducts(tk.Frame):
    def __init__(self, parent, root_frame, label_frame, table_num):
        tk.Frame.__init__(self, parent)
        self.root_frame = root_frame
        self.label_frame = label_frame
        self.table_num = f"Table {table_num}"

        # Frames
        self.tb = ttk.Frame(self.root_frame)
        self.tb.grid(column=0, row=0, padx=10, pady=10)

        #TreeView 
        self.tr_view_columns = ('name', 'quantity', 'orderstatus')
        self.tr_view = ttk.Treeview(self.tb, columns=self.tr_view_columns, show='headings', height=10, selectmode='browse')
        self.tr_view.column('name', width=200)
        self.tr_view.column('quantity', width=100)
        self.tr_view.column('orderstatus', width=200)

        self.tr_view.heading('name', text="Product Name")
        self.tr_view.heading('quantity', text="Quantity")
        self.tr_view.heading('orderstatus', text="Order Status")

        self.menu_itms = [
            ['Goulyash', '1','Cooking'],
            ['Goulyash', '2','Cooking'],
            ['Goulyash', '3','Cooking'],
            ['Goulyash', '4','Cooking'],
            ['Goulyash', '5','Cooking'],
            ['Goulyash', '6','Cooking'],
            ['Goulyash', '7','Cooking'],
            ['Goulyash', '8','Cooking'],
            ['Goulyash', '9','Cooking'],
            ['Goulyash', '10','Cooking'],
            ['Goulyash', '11','Cooking'],
            ['Goulyash', '12','Cooking'],
            ['Goulyash', '13','Cooking'],
            ['Goulyash', '14','Cooking'],
            ['Goulyash', '15','Cooking'],
            
            ]
        for e in self.menu_itms:
            self.tr_view.insert('', tk.END, values=e)

        self.tr_view.grid(column=0,row=0, rowspan=6, columnspan=3, pady=10, padx=10, ipadx=5, ipady=5)

        self.tr_v_vscr = ttk.Scrollbar(self.tb, orient="vertical", command=self.tr_view.yview)
        self.tr_v_vscr.grid(column=3, row=0, rowspan=6,  sticky=tk.NS)

        self.tr_view.config(yscrollcommand=self.tr_v_vscr.set)

        self.root_frame.add(self.tb, text=self.table_num)

        self.tr_view.bind("<ButtonRelease-1>", self.selected_item)

        self.cooked_btn = ttk.Button(self.label_frame, text="Cooked", command=self.change_state)
        self.cooked_btn.grid(column=0, row=2, padx=(0, 100), pady=10)
        self.cooked_btn.config(state='disabled')

        self.flf_btn = ttk.Button(self.label_frame, text="Fulfill order")
        self.flf_btn.grid(column=0, row=2, padx=(100, 0), pady=10)
        self.flf_btn.config(state='disabled')
    
    def selected_item(self, event):
        self.cooked_btn.config(state=tk.ACTIVE)

    def change_state(self):
        sel_item = self.tr_view.focus()
        retrieved_value = self.tr_view.item(sel_item, 'values')
        self.tr_view.item(sel_item, text="", values=(retrieved_value[0], retrieved_value[1], "Cooked"))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
