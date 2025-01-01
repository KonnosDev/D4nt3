import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog

def organize_folders_by_character(main_folder, start_char):
    items = os.listdir(main_folder)
    target_folders = [item for item in items if os.path.isdir(os.path.join(main_folder, item)) and item.startswith(start_char)]
    
    for folder in target_folders:
        folder_path = os.path.join(main_folder, folder)
        
        matching_subfolder_path = os.path.join(folder_path, folder)
        if os.path.isdir(matching_subfolder_path):
            new_path = os.path.join(main_folder, folder)
            
            while os.path.exists(new_path):
                new_path = os.path.join(main_folder, f"{folder}_")
            
            shutil.move(matching_subfolder_path, new_path)
            print(f"Moved folder {folder} to {new_path}.")

def main():

    root = tk.Tk()
    root.withdraw()  
    
    main_folder = filedialog.askdirectory(title="Select the Main Folder")

    if not main_folder:
        print("No folder selected. Exiting.")
        return

    start_char = simpledialog.askstring("Input", "Enter the starting character for folder selection:")

    if not start_char or len(start_char) != 1:
        print("Invalid character input. Exiting.")
        return

    organize_folders_by_character(main_folder, start_char)
    print("Folder organization completed.")

if __name__ == "__main__":
    main()
