from customtkinter import CTkImage
from PIL import Image
start_img = CTkImage(Image.open("./Img/start.svg").resize((23,23),Image.FIXED))
pause_img = CTkImage(Image.open("./Img/pause.svg").resize((23,23),Image.FIXED))
stop_inactive_img = CTkImage(Image.open("./Img/stop_inactive.svg").resize((23,23),Image.FIXED))
stop_active_img = CTkImage(Image.open("./Img/stop_active.svg").resize((23,23),Image.FIXED))