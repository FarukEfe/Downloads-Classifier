# User Interface gathers the directories as user input to deterine where to classify each file type
# Holds class called Settings that holds a dictionary of file types and their destination
# As well as if the program should or should not ignore suspicious files
# Internal Modules
from Monitor import Monitor
from Workers.Subprocess import Subprocess
from Helpers import *
# Design Libraries
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from Components.UI import *
# Other Libraries
from threading import Thread,Event
import os

class App:

    monitor = Monitor() # This class starts monitoring the downloads
    process = Subprocess() # This class opens a file dialog for directory selection
    selected_format = "pdf"
    on = False
    
    # User Feedback
    destination_feeback = False

    def __init__(self):
        self.window = tk.Tk() # Main window
        self.event = Event() # Handle monitor thread
        # Tk window specs
        self.window.title("Downloads Classifier")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")

    # Internal Calls
    def __select_format(self,choice):
        self.selected_format = choice
    
    def __set_format_destination(self):
        target = self.process.ask_user_folder()
        if os.path.exists(target) and os.path.isdir(target):
            self.monitor.dest_handler.set_destination(self.selected_format,target)
            self.destination_feeback = False
            return
        self.destination_feeback = True
    
    def __set_monitor_file(self):
        folder = self.process.ask_user_folder()
        self.monitor.set_directory(folder)
    
    # View Layout
    def __gen_frames(self) -> tuple[ctk.CTkFrame,ctk.CTkFrame]:
        button_frame = ctk.CTkFrame(master=self.window)
        button_frame.place(relx=0.1,rely=0.5,relwidth=0.2,relheight=1.0,anchor='center')
        contents_frame = ctk.CTkFrame(master=self.window)
        contents_frame.place(relx = 0.6,rely=0.5,relwidth=0.8,relheight=1.0,anchor='center')
        return button_frame,contents_frame
    
    def __gen_buttons(self,frame):
        # Generate buttons, input fields & assign tasks
        button_dir = ttk.Button(master=frame,text="Choose Downloads Folder",command=self.__set_monitor_file) # Sets monitor downloads folder
        # Dropdown that associates with destination button
        dp = dropdown(window=frame,values=ftypes,width=120,height=30,call=self.__select_format)
        button_dest = ttk.Button(master=frame,text="Choose Destination For Format",command=self.__set_format_destination)
        button_start = ttk.Button(master=frame,text="Start",command=self.__run_monitor)
        button_stop = ttk.Button(master=frame,text="Stop",command=self.__kill_thread)
        button_dir.pack(pady=10)
        button_dest.pack(pady=10)
        button_start.pack(pady=10)
        button_stop.pack(pady=10)
        dp.pack()
    
    def __gen_contents(self,frame):
        # Genetate contents that display
        # Should display monitoring file
        # Should display a table of set directories for file types
        # Should display if watchdog is running
        pass
    
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
        button_frame,contents_frame = self.__gen_frames()
        self.__gen_buttons(button_frame)
        self.__gen_contents(contents_frame)
        # This is the app mainloop
        self.window.mainloop()

if __name__ == '__main__':
    app = App()
    app.runApp()