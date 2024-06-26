# Internal Modules
from Workers.Monitor import Monitor
from Workers.Subprocess import Subprocess
from Helpers.Helpers import *
# Design Libraries
import customtkinter as ctk
from Components.UI import *
from Components.Gradient import *
from Components.Session import *
#from Components.Images import * # Fix error
# Other Libraries
from threading import Thread,Event
from math import floor,ceil
import time as t
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
    config_feedback: ctk.CTkLabel = None
    config_stat: ctk.CTkLabel = None
    config_timer: ctk.CTkLabel = None
    config_result: ctk.CTkButton = None

    # Event Handler for Thread
    thread: Thread = None
    t_on = False
    t_run: bool = False
    t_complete: bool = False
    t_feedback: bool = False
    event: Event = Event()
    timer_start = 0
    pause_starts = []
    pause_ends = []

    def __init__(self):
        self.window = ctk.CTk() # Main window
        ctk.set_appearance_mode("Dark")
        ctk.set_appearance_mode("blue")
        # Tk window specs
        self.window.title("Downloads Classifier")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.minsize(MINW,MINH)
        # Supposed to set widget transparent, but cuts out a whole section of the window
        #self.window.attributes("-transparentcolor","#FFFFF9")

    # Get total pause time
    def total_pause(self) -> float:
        limit = len(self.pause_ends)
        sum = 0
        for i in range(limit):
            sum += self.pause_ends[i]
            sum -= self.pause_starts[i]
        return sum


    # Get thread state
    def __get_state_label(self) -> str:
        t = ""
        if self.t_on:
            t = "Running..."
        elif self.t_run:
            t = "Paused."
        elif self.t_complete:
            t = "Session Over."
        return t

    # Configurations for Main Window
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
        self.config_start.configure(require_redraw=True,text_color=("#B0B0B0" if self.t_complete else "#EAEAEA"),fg_color=("grey" if self.t_complete else "#3E84D7" if self.t_on else "#46AA56"),text=("Pause" if self.t_on else "Continue" if self.t_run else "Start"))
        self.config_stop.configure(require_redraw=True,text_color=("#B0B0B0" if self.t_complete or not self.t_run else "#EAEAEA"),fg_color=("#46AA56" if self.t_complete else "#D14040" if self.t_run else "grey"))

    def __config_label(self):
        if self.config_label == None:
            return
        self.config_label.configure(text=self.__get_state_label())
    
    def __config_feedback_info(self):
        self.config_feedback.configure(text=("Plase select monitor file" if self.t_feedback else ""))
    
    def __config_stat_label(self):
        self.config_stat.configure(text=f"Moved files: {len(self.monitor.finished)}")
    
    def __config_timer(self):
        display = t.time()-self.total_pause()-self.timer_start
        if not self.t_on:
            display = self.pause_starts[-1]-self.total_pause()-self.timer_start
        self.config_timer.configure(text=f"Runtime: {floor(10*display)/10}s")
    
    def __display_result(self):
        self.config_result.pack(side="left",padx=(15,0))

    # Main Window Button Functionalities
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
        
    # UI Generation for Main Window
    def __gen_frames(self) -> tuple[ctk.CTkFrame,ctk.CTkFrame]:
        #background = GradientBg(self.window,GRAD,LEVELS)
        #background.place(relx=0,rely=0,relwidth=1,relheight=1,anchor=ctk.NW)
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
        button_dir = ctk.CTkButton(master=dir_frame,text="Choose Folder",fg_color="#46AA56",command=self.__set_monitor_file) # Sets monitor downloads folder
        button_dest = ctk.CTkButton(master=flex_frame,text="Set Destination",fg_color="#46AA56",command=self.__set_format_destination)
        dp = dropdown(window=flex_frame,values=ftypes,width=70,height=25,call=self.__select_format)
        # Info frame
        info = ctk.CTkFrame(master=frame,fg_color="transparent")
        info_label1 = ctk.CTkLabel(master=info,text=INFO1,justify="left",fg_color="transparent")
        info_label2 = ctk.CTkLabel(master=info,text=INFO2,justify="left",fg_color="transparent")
        # Start frame
        start = ctk.CTkFrame(master=frame,fg_color="transparent")
        button_start = ctk.CTkButton(
                master=start,
                text="Start",
                width=100,
                fg_color="#46AA56",
                text_color="#EAEAEA",
                hover_color="darkgrey",
                command=self.__run_monitor
            )
        button_stop = ctk.CTkButton(
                master=start,
                text="Stop",
                width=100,
                fg_color="grey",
                text_color="#B0B0B0",
                hover_color="darkgrey",
                command=self.__kill_thread
            )
        self.config_start = button_start
        self.config_stop = button_stop
        # Thread Info Frame
        t_info_frame = ctk.CTkFrame(frame,fg_color="transparent")
        t_info_text = ctk.CTkLabel(t_info_frame,text="",text_color="#E5B300",justify="left")
        self.config_feedback = t_info_text
        # Stats Label Frae
        t_stat_frame = ctk.CTkFrame(frame,fg_color="transparent")
        t_stat_label = ctk.CTkLabel(t_stat_frame,text="",justify="left",font=("Helvetica",18))
        self.config_stat = t_stat_label
        # Timer
        t_timer_frame = ctk.CTkFrame(frame,fg_color="transparent")
        t_timer_label = ctk.CTkLabel(t_timer_frame,text="",justify="left",font=("Helvetica",18))
        self.config_timer = t_timer_label
        # Pack Upper Frame
        upper.pack(side="top",fill="x")
        dir_frame.pack(pady=10,padx=10,fill="x")
        button_dir.pack(side="right")
        button_dest.pack(side="right")
        dp.pack(side="right",padx=(0,15))
        flex_frame.pack(pady=10,padx=10,fill="x")
        # Pack Info
        info.pack(side="top",fill="x",pady=(20,0))
        info_label1.place(relx=0.05,rely=0,anchor=ctk.NW)
        info_label2.place(relx=0.05,rely=0.3,anchor=ctk.NW)
        # Pack Buttons
        start.pack(side="top",fill="x",pady=(20,0),padx=10)
        button_stop.pack(side="right",padx=(8,0))
        button_start.pack(side="right",padx=(0,8))
        # Pack Feedback
        t_info_frame.pack(side="top",fill="x",pady=10)
        t_info_text.pack(side="top",fill="x")
        # Pack Stats
        t_stat_frame.pack(side="top",fill="x",pady=15)
        t_stat_label.pack(side="left",padx=20)
        # Pack Timer
        t_timer_frame.pack(side="top",fill="x",pady=10)
        t_timer_label.pack(side="left",padx=20)
    
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
        results_button = ctk.CTkButton(
                master=thread_frame,
                text="See Results",
                width=100,
                fg_color="#46AA56",
                hover_color="darkgrey",
                command=self.__show_results
            )
        self.config_result = results_button
        # Generate recent jobs finished
        jobs_list = DropList(frame,[],1.0)
        self.config_logs = jobs_list
        jobs_list.pack(pady=(0,10),padx=10,side="top",fill="both",expand=True)
    
    # Session Info Window UI Generation
    def __gen_session_info(self,master):
        scroll_view = ctk.CTkScrollableFrame(master)
        scroll_view.place(relx=0,rely=0,relwidth=1,relheight=1,anchor=ctk.NW)
        stat_keys = list(self.monitor.stats.keys())
        info_count = len(stat_keys)
        rows = ceil(info_count/3)

        for c in range(3):
            scroll_view.grid_columnconfigure(c,weight=1)

        for r in range(rows):
            scroll_view.grid_rowconfigure(r,weight=1)
        
        for i in range(len(stat_keys)):
            # Create Stat Frame
            key = stat_keys[i]
            job_n = self.monitor.stats[key]
            frame = FormatStatFrame(scroll_view,key,job_n)
            # Compute Column and Row for Display
            r = i//3
            c = i % 3
            frame.grid(row=r,column=c)

    # Back-end Operations
    def __kill_thread(self):
        if self.t_complete or not self.t_run:
            return
        self.event.set()
        print("Stopped listening.")

    def __monitor_mainloop(self):
        
        self.monitor.start()
        try:
            while self.monitor.is_alive():
                # Configurate the logs
                self.__config_jobs()
                self.__config_stat_label()
                self.__config_timer()
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
            self.__display_result()
            print("Thread execution over. Configuration complete.")
            
    # Before this code runs, you have to make sure that files have a destination
    # The code wouldn't crash either way, but why run something when it serves no purpose
    def __run_monitor(self):

        if not self.monitor.can_start():
            print("Make sure you have a monitoring directory selected.")
            self.t_feedback = True
            self.__config_feedback_info()
            return
        
        if self.t_complete:
            print("Once a session is over, you have to close the tab that is dedicated to it an re-run the program.")
            return

        if self.t_run:
            print("Program already running. Toggling pause")
            if self.t_on:
                self.pause_starts.append(t.time())
            else:
                self.pause_ends.append(t.time())
            self.t_on = not self.t_on
            self.__config_buttons()
            self.__config_label()
            return

        # Define & Start Thread
        self.thread = Thread(target=self.__monitor_mainloop,daemon=True)
        self.thread.start()
        # Update View State
        self.t_run = True
        self.t_on = True
        self.t_feedback = False
        self.timer_start = t.time()
        # Configure Buttons
        self.__config_buttons()
        self.__config_label()
    
    def __show_results(self):
        self.window.destroy()
        session_info = ctk.CTk()
        session_info.title("Downloads Classifier (Session Results)")
        session_info.geometry(f"{WIDTH}x{HEIGHT}")
        session_info.minsize(MINW,MINH)
        self.__gen_session_info(session_info)
        session_info.mainloop()

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
# burning glass picture floating when the search is happening
# display monitor stats once the session is over

# DONT CODE WHEN YOU'RE TIRED...
# Add the branch where duplicate jobs are all done. 
# Re-write yesterday's data type.
# Change algorithms accordingly.
# Remove job removing, instead append all jobs in queue to finished and flush the queue (the logic bug you missed yesterday)

#POSTPONED:
# Circular buttons for start/stop designed on figma
# Gradient background color