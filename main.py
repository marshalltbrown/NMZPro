import tkinter.scrolledtext as st
from tkinter import *
from tkinter.ttk import Separator
from Actions import *
from Runelite import runelite
from Controllers import admin
from reader import reader


def savePass():
    password = pass_entry.get()
    with open('password.txt', 'w') as f:
        f.write(password)
        string_vars['box'].insert('end', "New password saved.\n")
    pass_entry.delete(0, 'end')
    pass_entry.insert(0, readPassword())


def readPassword():  # Reads password from the password.txt then copies it to the clipboard.
    with open('password.txt', 'r') as f:
        data = f.readline()
    password = 'No password saved'
    data_length = len(data)
    if data_length != 0:
        password = ''
        for i in range(data_length):
            password += '*'
    return password


def startListener():  # Generates thread on the referenced function.
    print(f'Generating new thread for reader.')
    boss = admin('Null', string_vars, lock, inventory_table)
    threading.Thread(target=reader, args=(client, boss,), daemon=True).start()


def runLogin():  # Copies password from file and logs in to Runelite.
    with lock:
        string_vars['status'].set('Logging in')
        boss = admin('Null', string_vars, lock, inventory_table)
        threading.Thread(target=login, args=(client, boss,), daemon=True).start()
        string_vars['status'].set('Idle')


def runAlch():
    string_vars['status'].set('Setting up auto-alch.')
    boss = admin('S', string_vars, lock, inventory_table)
    threading.Thread(target=reader, args=(client, boss), daemon=True).start()


def runNMZ():
    string_vars['status'].set('Loading...')
    style = options_var.get()
    if style == 'Strength':
        s_style = 'S'
    elif style == 'Mage':
        s_style = 'M'
    elif style == 'Overload':
        s_style = 'O'
    else:
        s_style = 'R'

    string_vars['box'].insert('end', f"Starting NMZ script.\nStyle: {style}\n")
    boss = admin(s_style, string_vars, lock, inventory_table)
    threading.Thread(target=reader, args=(client, boss,), daemon=True).start()
    threading.Thread(target=NMZ, args=(client, boss,), daemon=True).start()

# --GUI and main thread set-up.
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
# -Top left logo label
Label(text='NMZPro', font=('Arial', 25)).grid(row=0, column=0, sticky='nw', columnspan=2, padx=10, pady=10)

# -Text Widgets
text_frame = Frame(gui, width=16, height=10)
text_frame.grid(row=1, column=0, sticky='nw', padx=(10, 0))
# Left side of text panel
static_health_label = Label(text_frame, text='Health: ').grid(row=0, column=0, sticky='e')
static_status_label = Label(text_frame, text='Status: ').grid(row=1, column=0, sticky='e')
static_absorption_label = Label(text_frame, text='Absorbs: ').grid(row=2, column=0, sticky='e')
static_buff_label = Label(text_frame, text='Buffs: ').grid(row=3, column=0, sticky='e')
# Right side of text panel
health_label = Label(text_frame, textvariable=string_vars['health'], width=35, anchor='w').grid(row=0, column=1, sticky='w')
status_label = Label(text_frame, textvariable=string_vars['status'], width=35, anchor='w').grid(row=1, column=1, sticky='w')
absorb_label = Label(text_frame, textvariable=string_vars['absorption'], width=35, anchor='w').grid(row=2, column=1, sticky='w')
buff_label = Label(text_frame, textvariable=string_vars['buff'], width=35, anchor='w').grid(row=3, column=1, sticky='w')

# -Horizontal Separator
Separator(gui).grid(row=2, column=0, sticky='ew', pady=20)

# -Button Widgets
button_frame = Frame(gui, height=100)
button_frame.grid(row=3, column=0, columnspan=2, sticky='nw', pady=(10, 0))
# Left side of button panel
login_button = Button(button_frame, text='Login', width=7, command=lambda: runLogin()).grid(row=0, column=0, padx=10, pady=(10, 0))
alch_button = Button(button_frame, text='Alch', width=7, command=lambda: runAlch()).grid(row=1, column=0, padx=10, pady=13)
nmz_button = Button(button_frame, text='NMZ', width=7, command=lambda: runNMZ()).grid(row=2, column=0, padx=10)
# Right side of button panel
pass_entry = Entry(button_frame, width=20)
pass_entry.insert(0, readPassword())
pass_entry.grid(row=0, column=1, pady=(10, 0), sticky='e')
save_button = Button(button_frame, text='Save', width=7, command=lambda: savePass()).grid(row=0, column=2, padx=10, pady=(10, 0), sticky='e')
options_var = StringVar()
options_var.set('Ranging')
option_menu = OptionMenu(button_frame, options_var, 'Ranging', 'Strength', 'Mage', 'Overload')
option_menu.grid(row=2, column=2, sticky='w')

# -Vertical separator
Separator(gui, orient='vertical').grid(row=0, column=2, rowspan=4, sticky='ns')

inv_info_frame = Frame(gui, width=150)
inv_info_frame.grid(row=0, column=3)
static_inventory_label = Label(inv_info_frame, text='Current tab: ').grid(row=0, column=0)
inventory_label = Label(inv_info_frame, textvariable=string_vars['inventory']).grid(row=0, column=1)

inv_frame = Frame(gui, width=150, padx=50)
inv_frame.grid(row=1, rowspan=3, column=3, sticky='ns')

inventory_table = [[StringVar() for _1 in range(4)] for _ in range(7)]
for row in range(7):
    for column in range(4):
        inventory_table[row][column] = StringVar()
        inventory_table[row][column].set('?')
        l = Label(inv_frame, textvariable=inventory_table[row][column], relief=RIDGE, width=5, height=2)
        l.grid(row=row, column=column)


string_vars['box'] = st.ScrolledText(gui, wrap=WORD, width=2, height=7, bg='black', fg='white', font=("Arial", 12))
string_vars['box'].grid(row=4, column=0, columnspan=4, padx=(10, 0), pady=(20, 0), sticky='nsew')
string_vars['box'].insert('end', "Program initiated.\n")
string_vars['box'].configure(state='normal')

#try:
client = runelite()  # Object from Runelite.py class. Used for client data.
#except Exception as e:
    #string_vars['box'].insert('end', "Runelite not found. Make sure Runelite is on screen before continuing.\n")

gui.mainloop()  # Accessible code above this point.
