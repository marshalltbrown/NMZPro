import threading
import time
import tkinter as tk
from tkinter import *
from Actions import *
from Runelite import runelite
from reader import reader


def startListener():  # Generates thread on the referenced function.
    print(f'Generating new thread for reader.')
    threading.Thread(target=reader, args=(client, string_vars, inventory_table,), daemon=True).start()


def runLogin():  # Copies password from file and logs in to Runelite.
    with lock:
        string_vars['status'].set('Logging in')
        login(client)
        string_vars['status'].set('Idle')


def runAlch():
    string_vars['status'].set('Setting up auto-alch.')
    autoAlch(client, string_vars, lock)


def runNMZ():
    string_vars['status'].set('Loading...')
    startListener()
    threading.Thread(target=NMZ, args=(client, string_vars, lock, inventory_table,), daemon=True).start()


# --GUI and main thread set-up.
client = runelite()  # Object from Runelite.py class. Used for client location data.
gui = tk.Tk()
gui.title("NMZPro")
gui.geometry("400x400")
print(f'Thread initialized in main: {threading.get_ident()}')
# gui.bind("<<StatusChange>>", printBonjour('no'))


# --Threading lock
lock = threading.Lock()

# --Thread safe strings that are used to update labels.
string_vars = {'status': tk.StringVar(),
               'health': tk.StringVar(),
               'absorption': tk.StringVar(),
               'buff': tk.StringVar(),
               'inventory': tk.StringVar()
               }

# --Widgets
static_health_label = tk.Label(text='Health: ').grid(row=2, column=1)
static_status_label = tk.Label(text='Status: ').grid(row=3, column=1)
static_absorption_label = tk.Label(text='Absorptions: ').grid(row=4, column=1)
static_buff_label = tk.Label(text='Buffs: ').grid(row=5, column=1)
static_inventory_label = tk.Label(text='Current tab: ').grid(row=6, column=1)

health_label = tk.Label(textvariable=string_vars['health']).grid(row=2, column=2)
status_label = tk.Label(textvariable=string_vars['status']).grid(row=3, column=2)
absorption_label = tk.Label(textvariable=string_vars['absorption']).grid(row=4, column=2)
buff_label = tk.Label(textvariable=string_vars['buff']).grid(row=5, column=2)
inventory_label = tk.Label(textvariable=string_vars['inventory']).grid(row=6, column=2, pady=20)

inventory_table = [{}, {}, {}, {}, {}, {}, {}]

for row in range(7):
    for column in range(4):
        inventory_table[row][column] = tk.StringVar()
        inventory_table[row][column].set('?')
        l = Label(textvariable=inventory_table[row][column], relief=RIDGE)
        if column == 0:
            l.grid(row=row + 7, column=column, sticky=NSEW, padx=(45, 0))
        else:
            l.grid(row=row + 7, column=column, sticky=NSEW)


login_button = tk.Button(text='Login', command=runLogin)
login_button.grid(row=1, column=1)

alch_button = tk.Button(text='Alch', command=runAlch)
alch_button.grid(row=1, column=2)

nmz_button = tk.Button(text='NMZ', command=runNMZ)
nmz_button.grid(row=1, column=3)

read_button = tk.Button(text='Read', command=startListener)
read_button.grid(row=1, column=4)

gui.mainloop()  # Accessible code above this point.
