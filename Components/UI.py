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
    
class CustomTable(ctk.CTkScrollableFrame):

    def __init__(self,window:ctk.CTkFrame,col_titles:list[str],rel_widths:list[float],*args:list[str]):
        super().__init__(window)
        col_values = list(args)
        row_values = col_values # Transpose values to make rows
        # Generate Tables from Lists
        title_display = TableRow(self,col_titles,rel_widths,titles=True)
        title_display.pack(side="top")
        for val in row_values:
            new = TableRow(self,val,rel_widths)
            new.pack(side="top")
    
    def pack(self,side:str):
        super().pack(side=side)
            

        
class TableRow(ctk.CTKFrame):
    
    def __init__(self,table:CustomTable,values:list[str],rel_widths:list[float],titles:bool=False):
        super().__init__(table)
        limit = min(len(rel_widths),len(values)) # Limit iteration to shorter list
        for i in range(limit):
            cell = ctk.CTkFrame(master=self,relwidth=rel_widths[i])
            text = ctk.CTkLabel(master=cell,text=values[i],anchor="center")
            cell.pack(side="left")
            text.pack(side="top")
    
    def pack(self,side:str):
        super().pack(side=side)
        
# Dropdown Menu

def dropdown(window:ctk.CTkFrame,values:list[str],width:int,height:int,call:callable) -> ctk.CTkComboBox:
    obj = ctk.CTkComboBox(master=window,values=values,width=width,height=height,command=call)
    return obj