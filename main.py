import threading
import time
import tkinter
from tkinter import *
import tkinter.scrolledtext as st
from tkinter.ttk import Separator

from Actions import *
from Runelite import runelite
from reader import reader


def startListener():  # Generates thread on the referenced function.
    print(f'Generating new thread for reader.')
    threading.Thread(target=reader, args=(client, string_vars, inventory_table,), daemon=True).start()


def runLogin():  # Copies password from file and logs in to Runelite.
    with lock:
        string_vars['status'].set('Logging in')
        threading.Thread(target=login, args=(client, string_vars,), daemon=True).start()
        string_vars['status'].set('Idle')


def runAlch():
    string_vars['status'].set('Setting up auto-alch.')
    threading.Thread(target=autoAlch, args=(client, string_vars, lock,), daemon=True).start()


def runNMZ():
    string_vars['status'].set('Loading...')
    startListener()
    threading.Thread(target=NMZ, args=(client, string_vars, lock, inventory_table,), daemon=True).start()

# --GUI and main thread set-up.
client = runelite()  # Object from Runelite.py class. Used for client location data.
gui = Tk()
gui.title("NMZPro")
gui.geometry("590x475")
print(f'Thread initialized in main: {threading.get_ident()}')


# --Threading lock
lock = threading.Lock()

# --Thread safe strings that are used to update labels.
string_vars = {'status': StringVar(),
               'health': StringVar(),
               'absorption': StringVar(),
               'buff': StringVar(),
               'inventory': StringVar()
               }

# --Widgets
Label(text='NMZPro', font=('Arial', 25)).grid(row=0, column=0, sticky='nw', columnspan=2, padx=10, pady=10)

text_frame = Frame(gui, width=160, height=100)
text_frame.grid(row=1, column=0, sticky='nw', padx=(10, 0), pady=(25, 0))

static_health_label = Label(text_frame, text='Health: ').grid(row=0, column=0, sticky='e')
static_status_label = Label(text_frame, text='Status: ').grid(row=1, column=0, sticky='e')
static_absorption_label = Label(text_frame, text='Absorbs: ').grid(row=2, column=0, sticky='e')
static_buff_label = Label(text_frame, text='Buffs: ').grid(row=3, column=0, sticky='e')


var_frame = Frame(gui, height=100)
var_frame.grid(row=1, column=1, sticky='nw', pady=(25, 0))
health_label = Label(var_frame, textvariable=string_vars['health'], width=35, anchor='w').grid(row=0, column=0, sticky='w')
status_label = Label(var_frame, textvariable=string_vars['status'], width=35, anchor='w').grid(row=1, column=0, sticky='w')
absorption_label = Label(var_frame, textvariable=string_vars['absorption'], width=35, anchor='w').grid(row=2, column=0, sticky='w')
buff_label = Label(var_frame, textvariable=string_vars['buff'], width=35, anchor='w').grid(row=3, column=0, sticky='w')

Separator(gui, orient='vertical').grid(row=0, column=2, rowspan=2, sticky='ns')

inv_info_frame = Frame(gui, width=150, bg='pink')
inv_info_frame.grid(row=0, column=3)
static_inventory_label = Label(inv_info_frame, text='Current tab: ').grid(row=0, column=0)
inventory_label = Label(inv_info_frame, textvariable=string_vars['inventory']).grid(row=0, column=1)

inventory_table = [{}, {}, {}, {}, {}, {}, {}]
inv_frame = Frame(gui, width=150, padx=50)
inv_frame.grid(row=1, column=3, sticky='ns')
for row in range(7):
    for column in range(4):
        inventory_table[row][column] = StringVar()
        inventory_table[row][column].set('?')
        l = Label(inv_frame, textvariable=inventory_table[row][column], relief=RIDGE, width=5, height=2)
        if column == 0:
            l.grid(row=row, column=column)
        else:
            l.grid(row=row, column=column)

# Button Widgets
Separator(text_frame).grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)
Separator(var_frame).grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)

login_button = Button(text_frame, text='Login', width=7, command=lambda: runLogin())
login_button.grid(row=5, column=0, pady=(10, 0))

alch_button = Button(text_frame, text='Alch', width=7, command=lambda: runAlch())
alch_button.grid(row=6, column=0, pady=13)

nmz_button = Button(text_frame, text='NMZ', width=7, command=lambda: runNMZ())
nmz_button.grid(row=7, column=0)

string_vars['box'] = st.ScrolledText(gui,
                         wrap=WORD,
                         width=2,
                         height=7,
                         bg='black',
                         fg='white',
                         font=("Arial", 12))

string_vars['box'].grid(row=2, column=0, columnspan=4, padx=(10, 0), pady=(20, 0), sticky='nsew')
string_vars['box'].insert('end', "Program intiated.")
string_vars['box'].configure(state='normal')


gui.mainloop()  # Accessible code above this point.
