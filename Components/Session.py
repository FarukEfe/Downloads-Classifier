import customtkinter as ctk

class FormatStatFrame(ctk.CTkFrame):

    def __init__(self,master,format:str,jobs:int):
        super().__init__(master)
        f_label = ctk.CTkLabel(self,text=f"Format: {format}",justify="left")
        j_label = ctk.CTkLabel(self,text=f"Files Moved: {jobs}",justify="left")
        f_label.pack(side="top",fill="x")
        j_label.pack(side="top",fill="x")
