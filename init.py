# Internal Modules
from Monitor import Monitor
from Workers.Subprocess import Subprocess
from Helpers.Helpers import *
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

    # View Controllers
    on = False
    destination_feeback = False

    # UI for Update
    config_table: CustomTable = None
    config_directory: ctk.CTkLabel = None
    config_start: ctk.CTkButton = None
    config_stop: ctk.CTkButton = None

    def __init__(self):
        self.window = ctk.CTk() # Main window
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.event = Event() # Handle monitor thread
        # Tk window specs
        self.window.title("Downloads Classifier")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")

    # Internal Calls
    def __config_table(self):
        if self.config_table == None:
            return
        self.config_table.config(self.monitor.dest_handler.data)
    
    def __config_directory(self):
        if self.config_directory == None:
            return
        self.config_directory.configure(text=self.monitor.directory)
    
    def __config_buttons(self):
        self.config_start.configure(require_redraw=True,fg_color=("grey" if self.on else "blue"))
        self.config_stop.configure(require_redraw=True,fg_color=("red" if self.on else "grey"))

    def __select_format(self,choice):
        self.selected_format = choice
    
    def __set_format_destination(self):
        target = self.process.ask_user_folder()
        if os.path.exists(target) and os.path.isdir(target):
            self.monitor.dest_handler.set_destination(self.selected_format,target)
            self.destination_feeback = False
            self.__config_table()
            return
        self.destination_feeback = True
    
    def __set_monitor_file(self):
        folder = self.process.ask_user_folder()
        self.monitor.set_directory(folder)
        self.__config_directory()
    
    # View Layout
    def __gen_frames(self) -> tuple[ctk.CTkFrame,ctk.CTkFrame]:
        button_frame = ctk.CTkFrame(master=self.window)
        button_frame.place(relx=0.2,rely=0.5,relwidth=0.4,relheight=1.0,anchor='center')
        contents_frame = ctk.CTkFrame(master=self.window)
        contents_frame.place(relx = 0.7,rely=0.5,relwidth=0.6,relheight=1.0,anchor='center')
        return button_frame,contents_frame
    
    def __gen_buttons(self,frame):
        # Upper frame
        upper = ctk.CTkFrame(master=frame,fg_color="transparent")
        flex_frame = ctk.CTkFrame(master=upper,fg_color="transparent")
        dir_frame = ctk.CTkFrame(master=upper,fg_color="transparent")
        button_dir = ctk.CTkButton(master=dir_frame,text="Choose Folder",command=self.__set_monitor_file) # Sets monitor downloads folder
        button_dest = ctk.CTkButton(master=flex_frame,text="Set Destination",command=self.__set_format_destination)
        dp = dropdown(window=flex_frame,values=ftypes,width=100,height=25,call=self.__select_format)
        # Start frame
        start = ctk.CTkFrame(master=frame,fg_color="transparent")
        button_start = ctk.CTkButton(
                master=start,
                text="Start",
                width=120,
                fg_color=("blue"),
                command=self.__run_monitor
            )
        button_stop = ctk.CTkButton(
                master=start,
                text="Stop",
                width=120,
                fg_color="grey",
                command=self.__kill_thread
            )
        self.config_start = button_start
        self.config_stop = button_stop
        # Pack Upper Frame
        upper.pack(side="top")
        dir_frame.pack(pady=10,fill="x")
        button_dir.pack(side="right")
        button_dest.pack(side="right")
        dp.pack(side="right",padx=15)
        flex_frame.pack(pady=10)
        # Pack Buttons
        start.pack(side="top",fill="x",pady=(210,0),padx=25)
        button_stop.pack(side="right",padx=(8,0))
        button_start.pack(side="right",padx=(0,8))
    
    def __gen_contents(self,frame):
        # Generate monitor directory text
        monitor_frame = ctk.CTkFrame(frame)
        monitor_text = ctk.CTkLabel(monitor_frame,text=self.monitor.directory,anchor="center")
        monitor_frame.pack(pady=10,padx=10,side="top",fill="x")
        monitor_text.pack()
        self.config_directory = monitor_text
        # Generate format and directories table
        values = self.monitor.dest_handler.data
        table = CustomTable(frame,(0.1,0.9),values)
        self.config_table = table
        table.pack(pady=10,padx=10,side="top",fill="x")
        # Generate recent jobs finished
        jobs_list = DropList(frame,["lolol","ahhahahhahhhha"],1.0)
        jobs_list.pack(pady=10,padx=10,side="top",fill="both")
    
    # Back-end Operations
    def __kill_thread(self):
        if not self.on:
            return
        self.event.set()
        print("Stopped listening")

    def __monitor_mainloop(self):
        
        self.monitor.start()
        try:
            while self.monitor.is_alive():
                print("Running...")
                # If stop command is given from outside the thread,
                # kill the monitor thread
                if self.event.is_set():
                    self.event.clear()
                    self.on = False
                    self.__config_buttons()
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
        if self.on:
            return
        t = Thread(target=self.__monitor_mainloop)
        t.start()
        self.on = True
        self.__config_buttons()
        print("Started listening...")

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

# Make a text that shows the program is running
# Complete Logging of Finished Jobs
# Threads can only be started once, destroy old one and make new thread when re-starting
# Resize window adjustments