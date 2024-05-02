# Internal Modules
from Workers.Monitor import Monitor
from Workers.Subprocess import Subprocess
from Helpers.Helpers import *
# Design Libraries
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from Components.UI import *
from Components.Gradient import GradientBg
#from Components.Images import * # Fix error
# Other Libraries
from threading import Thread,Event
import os

class App:

    monitor = Monitor() # This class starts monitoring the downloads
    process = Subprocess() # This class opens a file dialog for directory selection
    selected_format = "pdf"

    # UI for Update
    config_logs: DropList = None
    config_table: CustomTable = None
    config_directory: ctk.CTkLabel = None
    config_start: ctk.CTkButton = None
    config_stop: ctk.CTkButton = None
    config_label: ctk.CTkLabel = None

    # Event Handler for Thread
    thread: Thread = None
    t_on = False
    t_run: bool = False
    t_complete: bool = False
    event: Event = Event()

    def __init__(self):
        self.window = ctk.CTk() # Main window
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        # Tk window specs
        self.window.title("Downloads Classifier")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.minsize(MINW,MINH)

    def __get_state_label(self) -> str:
        t = ""
        if self.t_on:
            t = "Running..."
        elif self.t_run:
            t = "Paused."
        elif self.t_complete:
            t = "Session Over."
        return t

    # Internal Calls
    def __config_jobs(self):
        if self.config_logs == None:
            return
        self.config_logs.config(self.monitor.list_finished_jobs())

    def __config_table(self):
        if self.config_table == None:
            return
        self.config_table.config(self.monitor.dest_handler.data)
    
    def __config_directory(self):
        if self.config_directory == None:
            return
        self.config_directory.configure(text=self.monitor.directory)
    
    def __config_buttons(self):
        if self.config_start == None or self.config_stop == None:
            return
        self.config_start.configure(require_redraw=True,fg_color=("grey" if self.t_complete else "yellow" if self.t_on else "blue"),text=("Pause" if self.t_on else "Continue" if self.t_run else "Start"))
        self.config_stop.configure(require_redraw=True,fg_color=("green" if self.t_complete else "red" if self.t_run else "grey"))

    def __config_label(self):
        if self.config_label == None:
            return
        self.config_label.configure(text=self.__get_state_label())

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
        #background = GradientBg(self.window,GRAD,LEVELS)
        #background.pack(side="top",fill="both",expand=True)
        button_frame = ctk.CTkFrame(master=self.window,width=250,fg_color="transparent")
        button_frame.pack(side="left",fill="y")
        contents_frame = ctk.CTkFrame(master=self.window,fg_color="transparent")
        contents_frame.pack(side="left",fill="both",expand=True)
        return button_frame,contents_frame
    
    def __gen_buttons(self,frame):
        # Upper frame
        upper = ctk.CTkFrame(master=frame,fg_color="transparent")
        flex_frame = ctk.CTkFrame(master=upper,fg_color="transparent")
        dir_frame = ctk.CTkFrame(master=upper,fg_color="transparent")
        button_dir = ctk.CTkButton(master=dir_frame,text="Choose Folder",command=self.__set_monitor_file) # Sets monitor downloads folder
        button_dest = ctk.CTkButton(master=flex_frame,text="Set Destination",command=self.__set_format_destination)
        dp = dropdown(window=flex_frame,values=ftypes,width=70,height=25,call=self.__select_format)
        # Start frame
        start = ctk.CTkFrame(master=frame,fg_color="transparent")
        button_start = ctk.CTkButton(
                master=start,
                text="Start",
                width=100,
                fg_color="blue",
                command=self.__run_monitor
            )
        button_stop = ctk.CTkButton(
                master=start,
                text="Stop",
                width=100,
                fg_color="grey",
                command=self.__kill_thread
            )
        self.config_start = button_start
        self.config_stop = button_stop
        # Pack Upper Frame
        upper.pack(side="top",fill="x")
        dir_frame.pack(pady=10,padx=10,fill="x")
        button_dir.pack(side="right")
        button_dest.pack(side="right")
        dp.pack(side="right",padx=(0,15))
        flex_frame.pack(pady=10,padx=10,fill="x")
        # Pack Buttons
        start.pack(side="top",fill="x",pady=(240,0),padx=10)
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
        # Text that shows if running
        thread_frame = ctk.CTkFrame(frame,fg_color="transparent")
        thread_frame.pack(side="top",fill="x",pady=(10,5))
        thread_label = ctk.CTkLabel(thread_frame,text="",font=("Helvetica",18))
        thread_label.pack(side="left",padx=(10,0))
        self.config_label = thread_label
        # Generate recent jobs finished
        jobs_list = DropList(frame,[],1.0)
        self.config_logs = jobs_list
        jobs_list.pack(pady=(0,10),padx=10,side="top",fill="both",expand=True)
    
    # Back-end Operations
    def __kill_thread(self):
        self.event.set()
        print("Stopped listening.")

    def __monitor_mainloop(self):
        
        self.monitor.start()
        try:
            while self.monitor.is_alive():
                # Configurate the logs
                self.__config_jobs()
                # If stop command is given from outside the thread,
                # kill the monitor thread
                if self.event.is_set(): 
                    self.event.clear()
                    self.t_complete = True
                    self.t_run = False
                    self.t_on = False
                    break

                if not self.t_on:
                    print("Waiting...",end="\r")
                    continue
                print("Running...",end="\r")

                remove_keys = []
                for key in self.monitor.queue.keys(): # Iterate through all keys
                    dest = self.monitor.queue[key] # Get destination
                    self.process.move_file(key,dest) # Perform job
                    remove_keys.append(key) # Append to deleting keys
                
                self.monitor.delete_keys(remove_keys) # Delete keys after all jobs are done
        finally:
            self.monitor.stop()
            self.monitor.join(0)
            self.__config_buttons()
            self.__config_label()
            print("Thread execution over. Configuration complete.")
            
    # Before this code runs, you have to make sure that files have a destination
    # The code wouldn't crash either way, but why run something when it serves no purpose
    def __run_monitor(self):

        if not self.monitor.can_start():
            print("Make sure you have a monitoring directory selected.")
            return
        
        if self.t_complete:
            print("Once a session is over, you have to close the tab that is dedicated to it an re-run the program.")
            return

        if self.t_run:
            print("Program already running. Toggling pause")
            self.t_on = not self.t_on
            self.__config_buttons()
            self.__config_label()
            return

        # Define & Start Thread
        self.thread = Thread(target=self.__monitor_mainloop,daemon=True)
        self.thread.start()
        self.t_run = True
        # Listen for thread to finish (end of code of exception)
        # Change View Model and Configurate Buttons
        self.t_on = True
        self.__config_buttons()
        self.__config_label()

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

# Better Design Ideas:
# Circular buttons for start/stop designed on figma --TODAY
# Gradient background color --TODAY
# burning glass picture floating when the search is happening
# info display message at the bottom of start/stop for different states of the app
# display monitor stats once the session is over

# DONT CODE WHEN YOU'RE TIRED...
# Add the branch where duplicate jobs are all done. 
# Re-write yesterday's data type.
# Change algorithms accordingly.
# Remove job removing, instead append all jobs in queue to finished and flush the queue (the logic bug you missed yesterday)
