import time
import threading
import gui as mygui
import tkinter as tk

print(f'Thread initialized in main: {threading.get_ident()}')



def create_gui():
    print(f'Thread initialized in gui: {threading.get_ident()}')
    gui = tk.Tk()
    gui.title("NMZPro")
    gui.geometry("500x400")
    app = mygui.Application(gui)
    gui.mainloop()


thd = threading.Thread(target=create_gui)
thd.daemon = True
thd.start()

while True:
    for i in range(20):
        print(i)
        time.sleep(1)
