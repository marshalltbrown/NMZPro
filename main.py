import time
import threading
import tkinter as tk

print(f'Thread initialized in main: {threading.get_ident()}')


def printBonjour(status):
    status.set('Pressed')

def create_spammer(status):
    print(f'Thread initialized in worker: {threading.get_ident()}')
    counter = 0
    while counter <= 60:
        status.set(f'Idle for {counter} seconds.')
        time.sleep(1)
        counter += 1


gui = tk.Tk()
gui.title("NMZPro")
gui.geometry("500x400")
#gui.bind("<<StatusChange>>", printBonjour('no'))


status_label = tk.Label(text='Status: ').grid(row=2, column=1)
variable_string = tk.StringVar()
variable_string.set('Loading...')
variable_label = tk.Label(textvariable=variable_string).grid(row=2, column=2)
press_button = tk.Button(text='Press', command=lambda: printBonjour(variable_string))
press_button.grid(row=1, column=1)

thd = threading.Thread(target=create_spammer, args=(variable_string,), daemon=True).start()

gui.mainloop()  # Accessible code above this point.
