import customtkinter as ctk

class GradientBg(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        f2 = GradientCanvas(self, ["#FFFFFF","#000000"], [0,1])
        f2.pack(side="bottom", fill="both", expand=True)

class GradientCanvas(ctk.CTkCanvas):
    def __init__(self, parent, colors_hex:list[str], levels_hex:list[float]):
        ctk.CTkCanvas.__init__(self, parent)
        self.colors = colors_hex
        self.levels = levels_hex
        self.bind("<Configure>",self.__draw_mult)
    
    # Code taken from: https://stackoverflow.com/questions/26178869/is-it-possible-to-apply-gradient-colours-to-bg-of-tkinter-python-widgets
    def __draw(self,event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self.colors[0])
        (r2,g2,b2) = self.winfo_rgb(self.colors[1])
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")
    
    # Code taken from https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    def hex_to_rgb(self,hex) -> tuple[int,int,int]:
        val = hex.lstrip('#')
        lv = len(val)
        return tuple(int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
    def get_lowerbound_index(self,level) -> int:
        for i in range(len(self.levels)-1):
            if self.levels[i] < level and level < self.levels[i+1]:
                return i
        return -1
    
    # This method is developed by myself to fit infinite gradients and their levels as a float between 0 and 1
    def __draw_mult(self,event=None):
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
            nr,ng,nb = 0,0,0 # Get appropriate diff, colors, progress
            if current_level in self.levels:
                color_index = list.index(self.levels,current_level)
                color = rgbs[color_index]
                nr,ng,nb = color
            else:
                lower_index = self.get_lowerbound_index(current_level)
                print(lower_index)
                color = rgbs[lower_index]
                print(color)
                diff = current_level - self.levels[lower_index]
                print(diff)
                nr = int(color[0] + (ratios_r[lower_index] * diff))
                ng = int(color[1] + (ratios_g[lower_index] * diff))
                nb = int(color[2] + (ratios_b[lower_index] * diff))
                print(ratios_r[lower_index],nb,ng,nb)
            print("\n")

            color = '#%02x%02x%02x' % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")


if __name__ == "__main__":
    root = ctk.CTk()
    GradientBg(root).pack(fill="both", expand=True)
    root.mainloop()