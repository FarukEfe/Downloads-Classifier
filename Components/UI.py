import customtkinter as ctk
'''
Create scrollable tabview to display done jobs
Create scrollable tabview to display set destination directories
Create text that displays monitor file
Create Classified Files Counter
'''

# Custom Button

class CustomButton(ctk.CTkButton):
    def __init__(self,window:ctk.CTkFrame,txt:str,call:callable):
        super().__init__(window,text=txt,command=call)
        self.place(relx=0.5,rely=0.5,width=120,relheight=30,anchor='center')

# Design Custom Table
    
class CustomTableTwo(ctk.CTkScrollableFrame):

    def __init__(self,window:ctk.CTkFrame,rel_widths:tuple[float],dest:dict[str:str]):
        super().__init__(window)
        # Generate Tables from Lists
        key_list = dest.keys()
        row_len = len(key_list)
        for i in range(row_len):
            key = key_list[i]
            value = dest[key]
            new = TableRow(self,[key,value],rel_widths)
            new.pack(side="top")
            

        
class TableRow(ctk.CTkFrame):
    
    def __init__(self,table:CustomTableTwo,values:list[str],rel_widths:tuple[float]):
        super().__init__(table)
        limit = min(len(rel_widths),len(values)) # Limit iteration to shorter list
        for i in range(limit):
            cell = ctk.CTkFrame(master=self,relwidth=rel_widths[i])
            text = ctk.CTkLabel(master=cell,text=values[i],anchor="center")
            cell.pack(side="left")
            text.pack(side="top")
        
# Dropdown Menu

def dropdown(window:ctk.CTkFrame,values:list[str],width:int,height:int,call:callable) -> ctk.CTkComboBox:
    obj = ctk.CTkComboBox(master=window,values=values,width=width,height=height,command=call)
    return obj