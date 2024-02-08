# User Interface gathers the directories as user input to deterine where to classify each file type
# Holds class called Settings that holds a dictionary of file types and their destination
# As well as if the program should or should not ignore suspicious files
from Monitor import Monitor
import tkinter as tk
from tkinter import ttk

window = tk.Tk()

window.title("Downloads Classifier")
window.geometry("800x600")

# Generate buttons, input fields & assign tasks
button_dir = ttk.Button(master=window,text="Choose Downloads Folder",command=lambda x: x+1)
button_dest = ttk.Button(master=window,text="Choose Destination For Your Files",command= lambda x: x+1)
button_start = ttk.Button(master=window,text="Start",command=lambda x:x+1)
button_dir.pack()
button_dest.pack()
button_start.pack()

window.mainloop()
