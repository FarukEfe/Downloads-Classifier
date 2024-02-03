from tkinter import filedialog
import os, subprocess

class Subprocess:

    def __init__(self):
        pass

    # Returns User Directory
    def ask_user_folder(self):
        return filedialog.askdirectory()

    def find_path(self, dir_name:str, base:str) -> str:
        dir_list = []
        for root, dirs, _ in os.walk(base):
            for dir in dirs:
                if dir == dir_name:  
                    # First encounter is returned
                    dir_list.append(os.path.abspath(os.path.join(root, dir)))
    
        return dir_list
    
    def move_file(self, file_dir: str, destination: str):
        print(file_dir,destination)
        subprocess.run(f"move \"{file_dir}\" \"{destination}\"",shell=True)