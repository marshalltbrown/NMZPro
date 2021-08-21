import threading
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def printHello(self):
        print("Hello")

    def create_widgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit) # exits background (gui) thread
        self.quitButton.grid(row=1, column=0)
        self.printButton = tk.Button(self, text='Print', command=lambda: self.printHello())
        self.printButton.grid(row=1, column=1)
