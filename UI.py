# User Interface gathers the directories as user input to deterine where to classify each file type
# Holds class called Settings that holds a dictionary of file types and their destination
# As well as if the program should or should not ignore suspicious files
from Monitor import Monitor
from Subprocess import Subprocess
import tkinter as tk
from tkinter import ttk
from Helpers import *
from threading import Thread,Event

# This custom button class will be used for better design, abstraction and specialized use of buttons on the window
class Button(ttk.Button):
    def __init__(self,window:ttk.Frame,txt:str,call:callable):
        super().__init__(window,text=txt,command=call)
    
    def display(self):
        # Make button layers and pack them
        pass

class App:

    monitor = Monitor() # This class starts monitoring the downloads
    process = Subprocess() # This class opens a file dialog for directory selection
    event = Event()

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Downloads Classifier")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.button_frame = ttk.Frame(self.window)
        self.buttons: list[ttk.Button] = []
    
    # View Layout
    def __gen_buttons(self):
        # Generate buttons, input fields & assign tasks
        button_dir = ttk.Button(master=self.button_frame,text="Choose Downloads Folder",command=lambda x: x+1)
        button_dest = ttk.Button(master=self.button_frame,text="Choose Destination For Your Files",command= lambda x: x+1)
        button_start = ttk.Button(master=self.button_frame,text="Start",command=lambda x:x+1)
        button_stop = ttk.Button(master=self.button_frame,text="Stop",command=self.__kill_thread)
        button_dir.pack()
        button_dest.pack()
        button_start.pack()
        button_stop.pack()
        self.buttons = [button_dir,button_dest,button_start,button_stop]
    
    # Back-end Operations
    def __kill_thread(self):
        self.event.set()
    # Before this code runs, you have to make sure that files have a destination
    # The code wouldn't crash either way, but why run something when it serves no purpose
    def __monitor_mainloop(self,event:Event):
        self.monitor.start()
        try:
            while self.monitor.is_alive():
                # If stop command is given from outside the thread,
                # kill the monitor thread
                if event.is_set():
                    event.clear()
                    break
                remove_keys = []
                for key in self.monitor.queue.keys(): # Iterate through all keys
                    dest = self.monitor.queue[key] # Get destination
                    self.process.move_file(key,dest) # Perform job
                    remove_keys.append(key) # Append to deleting keys
                
                self.monitor.delete_keys(remove_keys) # Delete keys after all jobs are done
        finally:
            self.monitor.stop()
            self.monitor.join(0)
    
    def runMonitor(self):
        t = Thread(target=self.__monitor_mainloop,args=(self.event,))
        t.start()
        


    def runApp(self):
        # Here put any previous setup to do before running the app mainloop
        self.__gen_buttons()
        # This is the app mainloop
        self.window.mainloop()

if __name__ == '__main__':
    app = App()
    app.runApp()