# User Interface gathers the directories as user input to deterine where to classify each file type
# Holds class called Settings that holds a dictionary of file types and their destination
# As well as if the program should or should not ignore suspicious files
from Monitor import Monitor
import tkinter as tk
from tkinter import ttk
from Helpers import *

# This custom button class will be used for better design, abstraction and specialized use of buttons on the window
class Button(ttk.Button):
    def __init__(self,window:ttk.Frame,txt:str,call:callable):
        super().__init__(window,text=txt,command=call)

class App:



    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Downloads Classifier")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.button_frame = ttk.Frame(self.window)
        self.buttons: list[ttk.Button] = []
    
    def __gen_buttons(self):
        # Generate buttons, input fields & assign tasks
        button_dir = ttk.Button(master=self.button_frame,text="Choose Downloads Folder",command=lambda x: x+1)
        button_dest = ttk.Button(master=self.button_frame,text="Choose Destination For Your Files",command= lambda x: x+1)
        button_start = ttk.Button(master=self.button_frame,text="Start",command=lambda x:x+1)
        button_dir.pack()
        button_dest.pack()
        button_start.pack()
        self.buttons = [button_dir,button_dest,button_start]

    def runApp(self):
        self.window.mainloop()

if __name__ == '__main__':
    app = App()
    app.runApp()