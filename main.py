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
            string_var.set(readInventory(client))
        time.sleep(1)


def runLogin(string_var, lock):  # Copies password from file and logs in to Runelite.
    readPassword()
    with lock:
        string_var.set('Logging in')
        login(client)
        string_var.set('Idle')

# --Threading locks
status_lock = threading.Lock()
inventory_lock = threading.Lock()

# --GUI and main thread set-up.
client = runelite()  # Object from Runelite.py class. Used for client location data.
gui = tk.Tk()
gui.title("NMZPro")
gui.geometry("300x400")
print(f'Thread initialized in main: {threading.get_ident()}')
# gui.bind("<<StatusChange>>", printBonjour('no'))

# --Widgets
static_status_label = tk.Label(text='Status: ').grid(row=2, column=1)
static_inventory_label = tk.Label(text='Current tab: ').grid(row=3, column=1)

status_string = tk.StringVar()
status_label = tk.Label(textvariable=status_string).grid(row=2, column=2)
inventory_string = tk.StringVar()
inventory_label = tk.Label(textvariable=inventory_string).grid(row=3, column=2)

press_button = tk.Button(text='Login', command=lambda: createThread(runLogin, status_string, status_lock))
press_button.grid(row=1, column=1)

# Boot threads
createThread(inventoryListener, inventory_string, inventory_lock)

gui.mainloop()  # Accessible code above this point.
