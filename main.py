import time
import threading
import tkinter as tk

print(f'Thread initialized in main: {threading.get_ident()}')


def update_button(status):
    status.set('Button pressed.')


def create_spammer_reverse(status, lock):
    counter = 6
    with lock:
        while counter >= 0:
            status.set(f'Reversing for {counter} seconds.')
            time.sleep(1)
            counter -= 1


def create_spammer(status, lock):
    print(f'Thread initialized in worker: {threading.get_ident()}')
    counter = 0
    with lock:
        while counter <= 5:
            status.set(f'Increasing for {counter} seconds.')
            time.sleep(1)
            counter += 1


gui = tk.Tk()
gui.title("NMZPro")
gui.geometry("300x400")
#gui.bind("<<StatusChange>>", printBonjour('no'))

lock = threading.Lock()

status_label = tk.Label(text='Status: ').grid(row=2, column=1)
variable_string = tk.StringVar()
variable_string.set('Loading...')
variable_label = tk.Label(textvariable=variable_string).grid(row=2, column=2)
press_button = tk.Button(text='Press', command=lambda: update_button(variable_string))
press_button.grid(row=1, column=1)

thd = threading.Thread(target=create_spammer, args=(variable_string, lock,), daemon=True).start()
thd = threading.Thread(target=create_spammer_reverse, args=(variable_string, lock,), daemon=True).start()

gui.mainloop()  # Accessible code above this point.
