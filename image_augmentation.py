import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import random
import string
import ImgAgu

def create_image_augmentation_frame(parent):
    augmentation_frame = tk.Frame(parent)
    augmentation_frame.pack(fill=tk.BOTH, expand=True)

    selected_folders = []

    def list_folders(directory):
        return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    def get_first_image(folder):
        try:
            for file in os.listdir(folder):
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                    return os.path.join(folder, file)
        except Exception as e:
            print(f"Error loading image: {e}")
        return None

    def open_folder_dialog():
        folder = filedialog.askdirectory()
        if folder and folder not in selected_folders:
            selected_folders.append(folder)

            print(f"Selected folder path: {folder}")  # Print the folder path
            File_object = open(r"C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\imageAug\\results.txt", "w")
            File_object.write(folder)
            display_selected_folders()

    def display_selected_folders():
        for widget in selected_folders_frame.winfo_children():
            widget.destroy()
        for folder in selected_folders:
            first_image_path = get_first_image(folder)
            if first_image_path:
                img = Image.open(first_image_path)
                img = img.resize((50, 50), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
            else:
                default_icon = Image.new('RGB', (50, 50), color='gray')
                photo = ImageTk.PhotoImage(default_icon)

            panel = tk.Label(selected_folders_frame, image=photo)
            panel.image = photo
            panel.pack(side="left", padx=10, pady=10)

    def submit():
        if selected_folders:
            show_processing_frame()
            # Run the external script in a separate thread
            threading.Thread(target=run_script, args=(selected_folders,)).start()
        else:
            messagebox.showinfo("No Selection", "No folders selected.")

    def run_script(selected_folders):


        try:
            # Run back.py and wait for it to complete
            result = subprocess.run(['python', 'C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\ImgAgu.py'], capture_output=True, text=True)


            ImgAgu.main()



            parent.after(0, processing_complete)
        except Exception as e:
            print(f"Error running script: {e}")
            parent.after(0, show_error, str(e))

    def show_processing_frame():
        global processing_frame
        processing_frame = tk.Frame(augmentation_frame)
        processing_frame.pack()
        processing_label = tk.Label(processing_frame, text="Processing...")
        processing_label.pack()
        parent.after(100, update_processing_message, processing_label, 1)

    def update_processing_message(label, count):
        if count > 3:
            count = 1
        label.config(text=f"Processing{'.' * count}")
        parent.after(500, update_processing_message, label, count + 1)

    def processing_complete():
        processing_frame.destroy()
        messagebox.showinfo("Process Completed", "The script has completed running. Results are saved in the 'augmentationtest' folder.")

    def show_error(message):
        processing_frame.destroy()
        messagebox.showerror("Error", f"An error occurred: {message}")

    # UI elements
    folder_button = tk.Button(augmentation_frame, text="Open Folder", command=open_folder_dialog)
    folder_button.pack(pady=10)

    selected_folders_frame = tk.Frame(augmentation_frame)
    selected_folders_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    submit_button = tk.Button(augmentation_frame, text="Submit", command=submit)
    submit_button.pack(pady=10)

    return augmentation_frame

# If running this as a standalone script, create the main window and run the create_image_augmentation_frame function
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Augmentation Interface")
    create_image_augmentation_frame(root)
    root.mainloop()
