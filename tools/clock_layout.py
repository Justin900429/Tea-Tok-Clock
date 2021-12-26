import tkinter as tk
from tkinter.ttk import Label

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


class Clock(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set up tkinter frame
        self.title("Clock")
        self.configure(background="white")

        # Create clock and its label
        self.clk_label = Label(self, text="Time: ", font=("arial", 30), background="white")
        self.clk_label.grid(column=0, row=0, sticky=tk.W)
        self.clk = Label(self, font=("arial", 30), background="white")
        self.clk.grid(column=1, row=0, sticky=tk.W)

        # Create temperature and its label
        self.temp_label = Label(self, text="Temperature: ", font=("arial", 30), background="white")
        self.temp_label.config(background="white")
        self.temp_label.grid(column=0, row=1, sticky=tk.W)
        self.temp = Label(self, font=("arial", 30), background="white")
        self.temp.config(background="white")
        self.temp.grid(column=1, row=1, sticky=tk.W)

        # Set up figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.axis = self.figure.add_subplot(111)
        self.axis.set_ylim(0, 100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=2, sticky=tk.W)
