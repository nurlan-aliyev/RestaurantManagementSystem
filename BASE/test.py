
# import tkinter as tk

# class window2:
#     def __init__(self, master1):
#         self.panel2 = tk.Frame(master1)
#         self.panel2.grid()
#         self.button2 = tk.Button(self.panel2, text = "Quit", command = self.panel2.quit)
#         self.button2.grid()
#         vcmd = (master1.register(self.validate),
#                 '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
#         self.text1 = tk.Entry(self.panel2, validate = 'key', validatecommand = vcmd)
#         self.text1.grid()
#         self.text1.focus()

#     def validate(self, action, index, value_if_allowed,
#                        prior_value, text, validation_type, trigger_type, widget_name):
#         if value_if_allowed:
#             try:
#                 float(value_if_allowed)
#                 return True
#             except ValueError:
#                 return False
#         else:
#             return False

# root1 = tk.Tk()
# window2(root1)
# root1.mainloop()


# # python 3.x
# import tkinter as tk



# class CustomWidget(tk.Frame):
#     def __init__(self, parent, label, default=""):
#         tk.Frame.__init__(self, parent)

#         self.label = tk.Label(self, text=label, anchor="w")
#         self.entry = tk.Entry(self)
#         self.entry.insert(0, default)

#         self.label.pack(side="top", fill="x")
#         self.entry.pack(side="bottom", fill="x", padx=4)

#     def get(self):
#         return self.entry.get()

# class Example(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         self.label = tk.Label(self)
#         self.e1 = CustomWidget(self, "First Name:", "Inigo")
#         self.e2 = CustomWidget(self, "Last Name:", "Montoya")
#         self.submitButton = tk.Button(self, text="Submit", command=self.e1.destroy)

#         self.e1.grid(row=0, column=0, sticky="ew")
#         self.e2.grid(row=1, column=0, sticky="ew")
#         self.label.grid(row=2, column=0, sticky="ew")
#         self.submitButton.grid(row=4, column=0)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(2, weight=1)

#     def submit(self):
#         first = self.e1.get()
#         last = self.e2.get()
#         self.label.configure(text="Hello, %s %s" % (first, last))


# if __name__ == "__main__":
#     root = tk.Tk()
#     Example(root).place(x=0, y=0, relwidth=1, relheight=1)
#     root.mainloop()


# import tkinter as tk

# class Example(tk.Frame):
#     def __init__(self, parent):

#         tk.Frame.__init__(self, parent)
#         self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
#         self.frame = tk.Frame(self.canvas, background="#ffffff")
#         self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.vsb.set)

#         self.vsb.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((4,4), window=self.frame, anchor="nw",
#                                   tags="self.frame")

#         self.frame.bind("<Configure>", self.onFrameConfigure)

#         self.populate()

#     def populate(self):
#         '''Put in some fake data'''
#         for row in range(100):
#             tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
#                      relief="solid").grid(row=row, column=0)
#             t="this is the second column for row %s" %row
#             tk.Label(self.frame, text=t).grid(row=row, column=1)

#     def onFrameConfigure(self, event):
#         '''Reset the scroll region to encompass the inner frame'''
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# if __name__ == "__main__":
#     root=tk.Tk()
#     example = Example(root)
#     example.pack(side="top", fill="both", expand=True)
#     root.mainloop()

 self.canv = tk.Canvas(self, width=600, height=400,
        scrollregion=(0, 0, 1200, 800))
    self.canv.grid(row=0, column=0)

    self.scrollY = tk.Scrollbar(self, orient=tk.VERTICAL,
        command=self.canv.yview)
    self.scrollY.grid(row=0, column=1, sticky=tk.N+tk.S)

    self.scrollX = tk.Scrollbar(self, orient=tk.HORIZONTAL,
        command=self.canv.xview)
    self.scrollX.grid(row=1, column=0, sticky=tk.E+tk.W)

    self.canv['xscrollcommand'] = self.scrollX.set
    self.canv['yscrollcommand'] = self.scrollY.set