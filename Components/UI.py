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

    def __init__(self,window:ctk.CTkFrame,rel_widths:tuple[float],dest:dict[str:str]):
        super().__init__(window)
        self.rows: list[TableRow] = []
        self.widths = rel_widths
        # Generate Tables from Lists
        key_list = list(dest.keys())
        row_len = len(key_list)
        for i in range(row_len):
            key = key_list[i]
            value = dest[key]
            new = TableRow(self,[key,value],self.widths)
            self.rows.append(new)
            new.pack(side="top")
        
    def config(self,dest:dict[str:str]):
        self.__unpack()
        self.rows = []
        # Generate Tables from Lists
        key_list = list(dest.keys())
        row_len = len(key_list)
        for i in range(row_len):
            key = key_list[i]
            value = dest[key]
            new = TableRow(self,[key,value],self.widths)
            self.rows.append(new)
            new.pack(side="top",fill="x")
    
    def __unpack(self):
        for row in self.rows:
            row.destroy()

class DropList(ctk.CTkScrollableFrame):
    
    def __init__(self,master:ctk.CTkFrame,values:list[str],width:float):
        super().__init__(master)
        self.rows: list[TableRow] = []
        self.width = width
        # Generate Tables from Lists
        row_len = len(values)
        for i in range(row_len):
            text = values[i]
            new = TableRow(self,[text],[width])
            self.rows.append(new)
            new.pack(side="top",fill="x")
        
    # Configure rows
    def config(self,new_values:list[str]):
        self.__unpack()
        self.rows = []
        row_len = len(new_values)
        for i in range(row_len):
            text = new_values[i]
            new = TableRow(self,[text],[self.width])
            self.rows.append(new)
            new.pack(side="top",fill="x")

    # Unpack all rows
    def __unpack(self):
        for row in self.rows:
            row.destroy()
        
class TableRow(ctk.CTkFrame):
    
    def __init__(self,table:CustomTable,values:list[str],rel_widths:tuple[float]):
        super().__init__(table)
        limit = min(len(rel_widths),len(values)) # Limit iteration to shorter list
        offset = 0
        for i in range(limit):
            cell = ctk.CTkFrame(master=self,height=56)
            text = ctk.CTkLabel(master=cell,text=values[i],anchor="center")
            cell.place(relx=offset+rel_widths[i]/2,relwidth=rel_widths[i],anchor="center")
            text.place(x=10,rely=0.5)
            offset += rel_widths[i]
        
# Dropdown Menu

def dropdown(window:ctk.CTkFrame,values:list[str],width:int,height:int,call:callable) -> ctk.CTkComboBox:
    obj = ctk.CTkComboBox(master=window,values=values,width=width,height=height,command=call)
    return obj