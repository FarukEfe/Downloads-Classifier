import customtkinter as ctk

# The below code is influenced by the following resource:
# https://stackoverflow.com/questions/26178869/is-it-possible-to-apply-gradient-colours-to-bg-of-tkinter-python-widgets

class GradientBg(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        f2 = GradientCanvas(self, ["#EF68A1","#D081EB"], [0.1,0.9])
        f2.pack(side="bottom", fill="both", expand=True)

class GradientCanvas(ctk.CTkCanvas):
    def __init__(self, parent, colors_hex:list[str], levels_hex:list[float], **kwargs):
        ctk.CTkCanvas.__init__(self, parent, **kwargs)
        self.colors = colors_hex
        self.levels = levels_hex
        self.bind("<Configure>", self._draw)

    def _draw(self, event=None):
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

if __name__ == "__main__":
    root = ctk.CTk()
    GradientBg(root).pack(fill="both", expand=True)
    root.mainloop()