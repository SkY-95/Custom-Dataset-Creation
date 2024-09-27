import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import random
import string

def create_image_filter_frame(parent):
    filter_frame = tk.Frame(parent)
    filter_frame.pack(fill=tk.BOTH, expand=True)

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
        if not os.path.exists('filtertest'):
            os.makedirs('filtertest')

        random_folder_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        random_folder_path = os.path.join('filtertest', random_folder_name)
        os.makedirs(random_folder_path)

        try:
            # Run back.py and wait for it to complete
            result = subprocess.run(['python', 'back.py'], capture_output=True, text=True)

            # Store the result in the random folder
            with open(os.path.join(random_folder_path, 'results.txt'), 'w') as f:
                f.write(result.stdout)
                f.write(result.stderr)

            # Save the folder name to a file
            with open('filtertest/folder_names.txt', 'a') as f:
                f.write(random_folder_name + '\n')

            parent.after(0, processing_complete)
        except Exception as e:
            print(f"Error running script: {e}")
            parent.after(0, show_error, str(e))

    def show_processing_frame():
        global processing_frame
        processing_frame = tk.Frame(filter_frame)
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
        messagebox.showinfo("Process Completed", "The script has completed running. Results are saved in the 'filtertest' folder.")

    def show_error(message):
        processing_frame.destroy()
        messagebox.showerror("Error", f"An error occurred: {message}")

    # UI elements
    folder_button = tk.Button(filter_frame, text="Open Folder", command=open_folder_dialog)
    folder_button.pack(pady=10)

    selected_folders_frame = tk.Frame(filter_frame)
    selected_folders_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    submit_button = tk.Button(filter_frame, text="Submit", command=submit)
    submit_button.pack(pady=10)

    return filter_frame

# If running this as a standalone script, create the main window and run the create_image_filter_frame function
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Filter Interface")
    create_image_filter_frame(root)
    root.mainloop()

