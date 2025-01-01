import os
import tkinter as tk
from tkinter import filedialog

def delete_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            #? Check if the folder is empty
            if not os.listdir(dir_path):  
                os.rmdir(dir_path)
                print(f"Deleted empty folder: {dir_path}")

def main():
    root = tk.Tk()
    root.withdraw()
    main_folder = filedialog.askdirectory(title="Select the Folder to Clean")
    if not main_folder:
        print("No folder selected. Exiting.")
        return
    delete_empty_folders(main_folder)
    print("Empty folder cleanup completed.")

if __name__ == "__main__":
    main()