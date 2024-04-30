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
        super().__init__(window,orientation="vertical")
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
            new.pack(side="top",fill="x")
        
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
        super().__init__(master,orientation="vertical")
        self.rows: list[TableRow] = []
        self.width = width
        self.values = values
        # Generate Tables from Lists
        row_len = len(values)
        for i in range(row_len):
            text = values[i]
            new = TableRow(self,[text],[width])
            self.rows.append(new)
            new.pack(side="top",fill="x",pady=0)
        
    # Configure rows
    def config(self,new_values:list[str]):
        if not self.__should_config(new_values):
            return
        self.values = new_values
        self.__unpack()
        self.rows = []
        row_len = len(new_values)
        for i in range(row_len):
            text = new_values[i]
            new = TableRow(self,[text],[self.width])
            self.rows.append(new)
            new.pack(side="top",fill="x",pady=0)

    def __should_config(self,new_vals:list[str]) -> bool:
        return len(new_vals) != len(self.values)
        
    # Unpack all rows
    def __unpack(self):
        for row in self.rows:
            row.destroy()
        
class TableRow(ctk.CTkFrame):
    
    def __init__(self,table:ctk.CTkScrollableFrame,values:list[str],rel_widths:tuple[float]):
        super().__init__(table,height=40)
        limit = min(len(rel_widths),len(values)) # Limit iteration to shorter list
        offset = 0
        for i in range(limit):
            # Border (not working intended): ,border_width=2,border_color="white"
            cell = ctk.CTkFrame(master=self)
            text = ctk.CTkLabel(master=cell,text=values[i],anchor="center")
            cell.place(rely=0.5,relx=offset,relwidth=rel_widths[i],anchor=ctk.W)
            #cell.pack(side="left",fill="x")
            #cell.grid(row=i,sticky=ctk.W)
            text.place(x=10,rely=0.5,anchor=ctk.W)
            offset += rel_widths[i]
        
# Dropdown Menu

def dropdown(window:ctk.CTkFrame,values:list[str],width:int,height:int,call:callable) -> ctk.CTkComboBox:
    obj = ctk.CTkComboBox(master=window,values=values,width=width,height=height,command=call)
    return obj