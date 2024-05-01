from tkinter import *
from PIL import ImageTk,Image

start_img = ImageTk.PhotoImage(Image.open("./Img/start.svg").resize((23,23),Image.FIXED))
pause_img = ImageTk.PhotoImage(Image.open("./Img/pause.svg").resize((23,23),Image.FIXED))
stop_inactive_img = ImageTk.PhotoImage(Image.open("./Img/stop_inactive.svg").resize((23,23),Image.FIXED))
stop_active_img = ImageTk.PhotoImage(Image.open("./Img/stop_active.svg").resize((23,23),Image.FIXED))