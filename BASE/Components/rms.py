"""
Restaurant Management System v0.1.2 NA,
    App is made to facilitate restaurant management processes.

Developed by Aliyev Nurlan in Dec 2022
    Last upgrades: Jan 2023
"""

from mainwindow import MainWindow
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
