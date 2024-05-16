import tkinter as tk
from tkinter import ttk
from sqlite3 import Error

from database import Database


class OrderedProducts(tk.Frame):
    def __init__(self, parent, root_frame, label_frame, table_num, func):
        tk.Frame.__init__(self, parent)
        self.root_frame = root_frame
        self.label_frame = label_frame
        self.table_num = f"Table {table_num}"
        self.t_num = table_num
        self.f = func

        self.init_database()

        # Frames
        self.tb = ttk.Frame(self.root_frame)
        self.tb.grid(column=0, row=0, padx=10, pady=10)

        # TreeView
        self.tr_view_columns = ('name', 'quantity', 'orderstatus')
        self.tr_view = ttk.Treeview(
            self.tb,
            columns=self.tr_view_columns,
            show='headings',
            height=10,
            selectmode='browse'
        )
        self.tr_view.column('name', width=200, anchor=tk.CENTER)
        self.tr_view.column('quantity', width=100, anchor=tk.CENTER)
        self.tr_view.column('orderstatus', width=200, anchor=tk.CENTER)

        self.tr_view.heading('name', text="Product Name")
        self.tr_view.heading('quantity', text="Quantity")
        self.tr_view.heading('orderstatus', text="Order Status")

        self.tr_view.grid(column=0, row=0, rowspan=6,
                          columnspan=3, pady=10, padx=10, ipadx=5, ipady=5)

        self.tr_v_vscr = ttk.Scrollbar(
            self.tb, orient="vertical", command=self.tr_view.yview)
        self.tr_v_vscr.grid(column=3, row=0, rowspan=6,  sticky=tk.NS)

        self.tr_view.config(yscrollcommand=self.tr_v_vscr.set)

        self.root_frame.add(self.tb, text=self.table_num)

        self.tr_view.bind("<ButtonRelease-1>", self.selected_item)

        self.cooked_btn = ttk.Button(
            self.tb, text=f"Cooked", command=self.change_state)
        self.cooked_btn.grid(column=1, row=7, padx=(0, 200), pady=10)
        self.cooked_btn.config(state='disabled')

        self.flf_btn = ttk.Button(
            self.tb, text="Fulfil order", command=self.fulfil_order, state=tk.DISABLED)
        self.flf_btn.grid(column=1, row=7, padx=(200, 0), pady=10)

        self.populate_menu()

        self.root_frame.select(self.tb)

    def init_database(self):
        self.fac_db = Database("restaurant.db")

        cooked_orders = """
        CREATE TABLE IF NOT EXISTS cooked_orders(
            id integer PRIMARY KEY,
            table_num integer NOT NULL, 
            product_name text NOT NULL,
            order_quantity integer NOT NULL,
            order_price integer NOT NULL
        );
        """

        self.fac_db.create_table(cooked_orders)

    def populate_menu(self):
        retrieve_query = """SELECT id, table_num, product_name,  SUM(order_quantity) as order_quantity, order_status  FROM orders WHERE table_num = ? GROUP BY product_name ;
            """
        res = self.fac_db.read_val(retrieve_query, (self.t_num,))
        for r in res:
            product_name = r[2]
            product_quantity = f"x{r[3]}"
            order_status = r[4]
            self.tr_view.insert('', tk.END, values=(
                product_name, product_quantity, order_status))

    def check_for_cooked(self):
        or_stat = []
        for item in self.tr_view.get_children():
            it_val = self.tr_view.item(item, 'values')
            or_status = it_val[2]
            or_stat.append(or_status)

        btn_state = tk.DISABLED if "Ordered" in or_stat else tk.ACTIVE
        self.flf_btn.config(state=btn_state)

    def update_order_status(self):
        try:
            update_query = """
                UPDATE orders 
                SET order_status = ? 
                WHERE (table_num = ? AND product_name = ?)
                """

            sel_item = self.tr_view.focus()
            retrieved_value = self.tr_view.item(sel_item, 'values')
            or_status = retrieved_value[2]
            or_name = retrieved_value[0]

            self.fac_db.update(update_query, (or_status, self.t_num, or_name))

            # for item in self.tr_view.get_children():
            #     it_val = self.tr_view.item(item, 'values')
            #     or_status = it_val[2]
            #     self.fac_db.update(update_query, (or_status, self.t_num))
        except Error as e:
            print(e)

    def get_product_price(self, pr_name):
        load_query = """SELECT product_price FROM menu_config WHERE product_name = ?"""
        res = self.fac_db.read_val(load_query, (pr_name,))
        return res[0][0]

    def store_cooked_orders(self):
        try:
            load_query = """SELECT * FROM cooked_orders ORDER BY id DESC LIMIT 1; """
            spec_insert_query = """INSERT INTO cooked_orders VALUES (?, ?, ?,  ?, ?)"""
            for item in self.tr_view.get_children():
                result = self.fac_db.read_val(load_query)
                if result:
                    order_id = result[0][0] + 1
                else:
                    order_id = 1
                it_val = self.tr_view.item(item, 'values')
                or_name = it_val[0]
                or_quantity = int(it_val[1][1:])
                or_price = float(self.get_product_price(or_name))
                or_total = or_quantity * or_price
                self.fac_db.insert_spec_config(
                    spec_insert_query, (order_id, self.t_num, or_name, or_quantity, or_total))
        except Error as e:
            print(e)

    def update_order_db(self):
        try:
            delete_query = """DELETE FROM orders WHERE order_status = ?"""
            self.fac_db.delete_val(delete_query, ["Cooked"])
        except Error as e:
            print(e)

    def fulfil_order(self):
        self.store_cooked_orders()
        self.update_order_db()
        self.destroy()
        self.root_frame.forget(self.tb)
        if not self.root_frame.tabs():
            self.f()

    def selected_item(self, event):
        self.cooked_btn.config(state=tk.ACTIVE)
        self.check_for_cooked()

    def change_state(self):
        sel_item = self.tr_view.focus()
        retrieved_value = self.tr_view.item(sel_item, 'values')
        self.tr_view.item(sel_item, text="", values=(
            retrieved_value[0], retrieved_value[1], "Cooked"))
        self.update_order_status()
        self.check_for_cooked()
