import customtkinter as ctk

class CustomButton(ctk.CTkButton):
    def __init__(self,window:ctk.CTkFrame,txt:str,call:callable):
        super().__init__(window,text=txt,command=call)
        self.place(relx=0.5,rely=0.5,width=120,relheight=30,anchor='center')

def dropdown(window:ctk.CTkFrame,values:list[str],width:int,height:int,call:callable) -> ctk.CTkComboBox:
    obj = ctk.CTkComboBox(master=window,values=values,width=width,height=height,command=call)
    return obj