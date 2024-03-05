# User Interface gathers the directories as user input to deterine where to classify each file type
# Holds class called Settings that holds a dictionary of file types and their destination
# As well as if the program should or should not ignore suspicious files
from Monitor import Monitor
from Subprocess import Subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from Helpers import *
from threading import Thread,Event

# This custom button class will be used for better design, abstraction and specialized use of buttons on the window
class CustomButton(ctk.CTkButton):
    def __init__(self,window:ctk.CTkFrame,txt:str,call:callable):
        super().__init__(window,text=txt,command=call)
        self.place(relx=0.5,rely=0.5,width=120,relheight=30,anchor='center')

class App:

    monitor = Monitor() # This class starts monitoring the downloads
    process = Subprocess() # This class opens a file dialog for directory selection


    def __init__(self):
        self.window = tk.Tk() # Main window
        self.event = Event() # Handle monitor thread
        # Tk window specs
        self.window.title("Downloads Classifier")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
    
    # View Layout
    def __gen_frame(self) -> ctk.CTkFrame:
        button_frame = ctk.CTkFrame(master=self.window)
        button_frame.place(relx=0.1,rely=0.5,relwidth=0.2,relheight=1.0,anchor='center')
        button_frame.pack()
        return button_frame
    
    def __gen_buttons(self,frame):
        # Generate buttons, input fields & assign tasks
        button_dir = ttk.Button(master=frame,text="Choose Downloads Folder",command=lambda x: x+1)
        button_dest = ttk.Button(master=frame,text="Choose Destination For Your Files",command= lambda x: x+1)
        button_start = ttk.Button(master=frame,text="Start",command=self.__run_monitor)
        button_stop = ttk.Button(master=frame,text="Stop",command=self.__kill_thread)
        button_dir.pack(pady=10)
        button_dest.pack(pady=10)
        button_start.pack(pady=10)
        button_stop.pack(pady=10)
    
    # Back-end Operations
    def __kill_thread(self):
        self.event.set()

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
            
    # Before this code runs, you have to make sure that files have a destination
    # The code wouldn't crash either way, but why run something when it serves no purpose
    def __run_monitor(self):
        t = Thread(target=self.__monitor_mainloop,args=(self.event,))
        t.start()
        


    def runApp(self):
        # Here put any previous setup to do before running the app mainloop
        frame = self.__gen_frame()
        self.__gen_buttons(frame)
        # This is the app mainloop
        self.window.mainloop()

if __name__ == '__main__':
    app = App()
    app.runApp()