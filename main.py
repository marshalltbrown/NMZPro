import threading
import tkinter as tk
from Actions import *
from Runelite import runelite


def createThread(function):  # Generates thread on the referenced function.
    print(f'Generating new thread for {function}.')
    threading.Thread(target=function, args=(variable_string, status_lock,), daemon=True).start()


def runLogin(status_string, lock):  # Copies password from file and logs in to Runelite.
    readPassword()
    with lock:
        status_string.set('Logging in')
        login(client)
        status_string.set('Idle')

# --Threading locks
status_lock = threading.Lock()

# --GUI and main thread set-up.
client = runelite()  # Object from Runelite.py class. Used for client location data.
gui = tk.Tk()
gui.title("NMZPro")
gui.geometry("300x400")
print(f'Thread initialized in main: {threading.get_ident()}')
# gui.bind("<<StatusChange>>", printBonjour('no'))

# --Widgets
status_label = tk.Label(text='Status: ').grid(row=2, column=1)

variable_string = tk.StringVar()
variable_string.set('Loading...')
variable_label = tk.Label(textvariable=variable_string).grid(row=2, column=2)

press_button = tk.Button(text='Login', command=lambda: createThread(runLogin))
press_button.grid(row=1, column=1)


gui.mainloop()  # Accessible code above this point.
