import threading
import time
import tkinter as tk
from Actions import *
from Runelite import runelite


def createThread(function, string_var, lock_var):  # Generates thread on the referenced function.
    print(f'Generating new thread for {function}.')
    threading.Thread(target=function, args=(string_var, lock_var,), daemon=True).start()


def inventoryListener(string_var, lock):
    while True:
        with lock:
            client.updateClient()  # WARNING - IS UPDATING CLIENT EVERY SECOND
            string_var.set(readInventory(client, gamestate))
        time.sleep(1)


def healthListener(string_var, lock):
    while True:
        with lock:
            string_var.set(readHealth(client, gamestate))


def runLogin(string_var, lock):  # Copies password from file and logs in to Runelite.
    readPassword()
    with lock:
        string_var.set('Logging in')
        login(client)
        string_var.set('Idle')


def runAlch(string_var, lock):
    with lock:
        string_var.set('Setting up auto-alch.')
        autoAlch(client, string_var, lock)


def runNMZ(string_var, lock):
    NMZ(client, gamestate, string_var)
    string_var.set('Idle.')


# --Variables
gamestate = {}
gamestate['tab'] = 'Unknown'
gamestate['health'] = 'Unknown'

# --Threading locks
status_lock = threading.Lock()
inventory_lock = threading.Lock()
health_lock = threading.Lock()

# --GUI and main thread set-up.
client = runelite()  # Object from Runelite.py class. Used for client location data.
gui = tk.Tk()
gui.title("NMZPro")
gui.geometry("300x400")
print(f'Thread initialized in main: {threading.get_ident()}')
# gui.bind("<<StatusChange>>", printBonjour('no'))

# --Widgets
static_inventory_label = tk.Label(text='Current tab: ').grid(row=2, column=1)
static_health_label = tk.Label(text='Health: ').grid(row=3, column=1)
static_status_label = tk.Label(text='Status: ').grid(row=4, column=1)

inventory_string = tk.StringVar()
inventory_label = tk.Label(textvariable=inventory_string).grid(row=2, column=2)
health_string = tk.StringVar()
health_label = tk.Label(textvariable=health_string).grid(row=3, column=2)
status_string = tk.StringVar()
status_label = tk.Label(textvariable=status_string).grid(row=4, column=2)

login_button = tk.Button(text='Login', command=lambda: createThread(runLogin, status_string, status_lock))
login_button.grid(row=1, column=1)

alch_button = tk.Button(text='Auto Alch', command=lambda: createThread(runAlch, status_string, status_lock))
alch_button.grid(row=1, column=2)

nmz_button = tk.Button(text='NMZ', command=lambda: createThread(runNMZ, status_string, status_lock))
nmz_button.grid(row=1, column=3)

# Boot threads
createThread(inventoryListener, inventory_string, inventory_lock)
createThread(healthListener, health_string, health_lock)

gui.mainloop()  # Accessible code above this point.
