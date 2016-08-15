import update_addons
import multiprocessing
from tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.button = Button(frame,
                             text='Update!',
                             command=self.run_update)
        self.button.pack(side=LEFT)

    def run_update(self):
        update_addons.run_update()

if __name__ == '__main__':
    multiprocessing.freeze_support()

    root = Tk()
    app = App(root)
    root.mainloop()