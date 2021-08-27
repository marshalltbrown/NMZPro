import threading
import time
import tkinter as tk
from tkinter import *
from Actions import *
from Runelite import runelite


def createThread(function, string_dict, lock_dict):  # Generates thread on the referenced function.
    print(f'Generating new thread for {function}.')
    threading.Thread(target=function, args=(string_dict, lock_dict,), daemon=True).start()


def inventoryListener(string_dict, lock_dict):
    while True:
        with lock_dict['inventory']:
            client.updateClient()  # WARNING - IS UPDATING CLIENT EVERY SECOND
            readInventory(client, string_dict, lock_dict, inventory_table)
        time.sleep(5)


def healthListener(string_dict, lock_dict):
    while True:
        with lock_dict['health']:
            string_dict['health'].set(readHealth(client))
        time.sleep(.5)


def runLogin(string_dict, lock_dict):  # Copies password from file and logs in to Runelite.
    readPassword()
    with lock_dict['status']:
        string_dict['status'].set('Logging in')
        login(client)
        string_dict['status'].set('Idle')


def runAlch(string_var, lock):
    with lock:
        string_var['status'].set('Setting up auto-alch.')
        autoAlch(client, string_var, lock)


def runNMZ(string_dict, lock_dict):
    NMZ(client, string_dict, lock_dict)
    string_dict['status'].set('Idle.')




# --GUI and main thread set-up.
client = runelite()  # Object from Runelite.py class. Used for client location data.
gui = tk.Tk()
gui.title("NMZPro")
gui.geometry("300x400")
print(f'Thread initialized in main: {threading.get_ident()}')
# gui.bind("<<StatusChange>>", printBonjour('no'))


# --Threading locks
locks = {'status': threading.Lock(), 'health': threading.Lock(), 'inventory': threading.Lock()}
string_vars = {'status': tk.StringVar(), 'health': tk.StringVar(), 'inventory': tk.StringVar()}

# --Widgets
static_health_label = tk.Label(text='Health: ').grid(row=2, column=1)
static_status_label = tk.Label(text='Status: ').grid(row=3, column=1)
static_inventory_label = tk.Label(text='Current tab: ').grid(row=4, column=1)

health_label = tk.Label(textvariable=string_vars['health']).grid(row=2, column=2)
status_label = tk.Label(textvariable=string_vars['status']).grid(row=3, column=2)
inventory_label = tk.Label(textvariable=string_vars['inventory']).grid(row=4, column=2, pady=20)

inventory_table = [{}, {}, {}, {}]
for x in range(4):
    for y in range(7):
        inventory_table[x][y] = tk.StringVar()
        inventory_table[x][y].set('?')
        l = Label(textvariable=inventory_table[x][y], relief=RIDGE)
        if x == 0:
            l.grid(row=y+5, column=x, sticky=NSEW, padx=(45, 0))
        else:
            l.grid(row=y+5, column=x, sticky=NSEW)


# print(f"My data: {str(inventory_table[0])}")
# print(f"My data: {str(inventory_table[1])}")
# print(f"My data: {str(inventory_table[2])}")
# print(f"My data: {str(inventory_table[3])}")


#login_button = tk.Button(text='Login', command=lambda: createThread(runLogin, string_vars, locks))
#login_button.grid(row=1, column=1)

login_button = tk.Button(text='Login', command=lambda: win32test())
login_button.grid(row=1, column=1)

alch_button = tk.Button(text='Alch', command=lambda: createThread(runAlch, string_vars, locks))
alch_button.grid(row=1, column=2)

nmz_button = tk.Button(text='NMZ', command=lambda: createThread(runNMZ, string_vars, locks))
nmz_button.grid(row=1, column=3)

# Boot threads
#createThread(inventoryListener, string_vars, locks)
#createThread(healthListener, string_vars, locks)

gui.mainloop()  # Accessible code above this point.
