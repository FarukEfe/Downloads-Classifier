import customtkinter as ctk

class GradientBg(ctk.CTkFrame):
    def __init__(self, parent, gradients:list[str],levels:list[float]):
        ctk.CTkFrame.__init__(self, parent)
        f2 = GradientCanvas(self, gradients, levels)
        f2.pack(side="top", fill="both", expand=True)

class GradientCanvas(ctk.CTkCanvas):
    def __init__(self, parent, colors_hex:list[str], levels_hex:list[float]):
        ctk.CTkCanvas.__init__(self, parent)
        self.colors = colors_hex
        self.levels = sorted(levels_hex)
        self.bind("<Configure>",self.__draw)
    
    # This method is taken from: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    def hex_to_rgb(self,hex) -> tuple[int,int,int]:
        val = hex.lstrip('#')
        lv = len(val)
        return tuple(int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
    def get_lowerbound_index(self,level) -> int:
        for i in range(len(self.levels)-1):
            if self.levels[i] < level and level <= self.levels[i+1]:
                return i
        return -1
    
    def get_diff(self,level) -> float:
        for i in range(len(self.levels)-1):
            if self.levels[i] < level and level <= self.levels[i+1]:
                return (level-self.levels[i])/(self.levels[i+1]-self.levels[i])
        return 1
    
    def get_lower_slice(self,limit,n) -> int:
        selection = 0
        for level in self.levels:
            val = limit*level
            if val >= n:
                return int(n-selection)
            
            selection = val
        return int(n-selection)

    
    # This method is developed by myself to fit infinite gradients and their levels as a float between 0 and 1
    def __draw(self,event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width

        rgbs: list[tuple] = []
        for hex in self.colors:
            rgb = self.hex_to_rgb(hex)
            rgbs.append(rgb)

        ratios_r = []
        ratios_g = []
        ratios_b = []

        for rgb_i in range(len(rgbs)-1):
            dist = self.levels[rgb_i+1]-self.levels[rgb_i]
            r1,g1,b1 = rgbs[rgb_i]
            r2,g2,b2 = rgbs[rgb_i+1]
            diff_r = (r2-r1) / (limit * dist)
            diff_g = (g2-g1) / (limit * dist)
            diff_b = (b2-b1) / (limit * dist)
            ratios_r.append(diff_r)
            ratios_g.append(diff_g)
            ratios_b.append(diff_b)
            
        for i in range(limit):
            current_level = i/limit
            print(current_level)
            lower_index = self.get_lowerbound_index(current_level)
            print(lower_index)
            color = rgbs[lower_index]
            print(color)
            diff = self.get_diff(current_level)
            shift = diff*self.get_lower_slice(limit,i)
            nr = int(color[0] + (ratios_r[lower_index]*shift))
            ng = int(color[1] + (ratios_g[lower_index]*shift))
            nb = int(color[2] + (ratios_b[lower_index]*shift))
            print(ratios_r[lower_index],nb,ng,nb)
            print("\n")
            color = '#%02x%02x%02x' % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    GradientBg(root,["#F8AA20","D081EB","DE815A","#C6B049"],[0.0,0.33,0.66,1.0]).pack(fill="both", expand=True)
    root.mainloop()