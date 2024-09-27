import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import string
import subprocess
import threading
import webbrowser

def create_test_frame(parent):
    test_frame = tk.Frame(parent)
    test_frame.pack(fill=tk.BOTH, expand=True)

    def list_folders():
        test_folder = "test"
        return [f for f in os.listdir(test_folder) if os.path.isdir(os.path.join(test_folder, f))]

    def get_first_image(folder):
        try:
            for file in os.listdir(folder):
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                    return os.path.join(folder, file)
        except Exception as e:
            print(f"Error loading image: {e}")
        return None

    def generate_random_folder_name(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def select_video():
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            video_path.set(file_path)

    def submit():
        if not video_path.get():
            messagebox.showinfo("No Video Selected", "Please select a video file.")
            return

        selected_folders = [folder for folder, var in folder_vars.items() if var.get()]
        if selected_folders:
            show_processing_frame()
            threading.Thread(target=run_script).start()
        else:
            messagebox.showinfo("No Selection", "No folders selected.")

    def run_script():
        random_folder = generate_random_folder_name()
        main_folder = 'display'
        random_folder_path = os.path.join(main_folder, random_folder)

        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        if not os.path.exists(random_folder_path):
            os.makedirs(random_folder_path)

        output_video_path = os.path.join(random_folder_path, 'output_video.mp4')

        try:
            result = subprocess.run(['python', 'tested.py', video_path.get(), output_video_path], capture_output=True, text=True)

            if result.returncode == 0:
                parent.after(0, processing_complete, output_video_path)
            else:
                parent.after(0, show_error, result.stderr)
        except Exception as e:
            print(f"Error running script: {e}")
            parent.after(0, show_error, str(e))

    def show_processing_frame():
        global processing_frame
        processing_frame = tk.Frame(test_frame)
        processing_frame.pack()
        processing_label = tk.Label(processing_frame, text="Processing...")
        processing_label.pack()
        parent.after(100, update_processing_message, processing_label, 1)

    def update_processing_message(label, count):
        if count > 3:
            count = 1
        label.config(text=f"Processing{'.' * count}")
        parent.after(500, update_processing_message, label, count + 1)

    def processing_complete(output_video_path):
        processing_frame.destroy()
        messagebox.showinfo("Process Completed", f"The script has completed running. Processed video is saved at {output_video_path}.")
        os.startfile(output_video_path)  # This will open the video file with the default video player

    def show_error(message):
        processing_frame.destroy()
        messagebox.showerror("Error", f"An error occurred: {message}")

    def open_processed_videos():
        main_folder = 'display'
        if not os.path.exists(main_folder):
            messagebox.showinfo("No Processed Videos", "No processed videos found.")
            return

        processed_videos = []
        for root, dirs, files in os.walk(main_folder):
            for file in files:
                if file.lower().endswith(('mp4', 'avi', 'mov', 'mkv')):
                    processed_videos.append(os.path.join(root, file))

        if not processed_videos:
            messagebox.showinfo("No Processed Videos", "No processed videos found.")
        else:
            video_list_window = tk.Toplevel(parent)
            video_list_window.title("Processed Videos")

            for video_path in processed_videos:
                video_label = tk.Label(video_list_window, text=video_path, fg="blue", cursor="hand2")
                video_label.pack()
                video_label.bind("<Button-1>", lambda e, p=video_path: webbrowser.open(p))

    # Get the list of folders from the "test" directory
    folders = list_folders()

    # Create a dictionary to hold the folder variables
    folder_vars = {}

    # Create a frame for the folder icons
    frame = tk.Frame(test_frame)
    frame.pack()

    if not folders:
        no_folders_label = tk.Label(frame, text="No folders found.")
        no_folders_label.pack()
    else:
        for folder in folders:
            folder_path = os.path.join("test", folder)
            var = tk.BooleanVar()

            first_image_path = get_first_image(folder_path)
            if first_image_path:
                img = Image.open(first_image_path)
                img = img.resize((50, 50), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
            else:
                default_icon = Image.new('RGB', (50, 50), color='gray')
                photo = ImageTk.PhotoImage(default_icon)

            panel = tk.Label(frame, image=photo)
            panel.image = photo  # Keep a reference to avoid garbage collection
            panel.pack(side="left", padx=10, pady=10)

            chk = tk.Checkbutton(frame, text=folder, variable=var)
            chk.pack(side="left")

            folder_vars[folder] = var

    # Create a variable to hold the selected video path
    video_path = tk.StringVar()

    # Create a button to select a video file
    select_video_button = tk.Button(test_frame, text="Select Video", command=select_video)
    select_video_button.pack(pady=10)

    # Display the selected video path
    video_label = tk.Label(test_frame, textvariable=video_path)
    video_label.pack(pady=10)

    # Create a submit button
    submit_button = tk.Button(test_frame, text="Test", command=submit)
    submit_button.pack(pady=10)

    # Create a button to open processed videos
    open_videos_button = tk.Button(test_frame, text="Open Processed Videos", command=open_processed_videos)
    open_videos_button.pack(pady=10)

    return test_frame

# If running this as a standalone script, create the main window and run the create_test_frame function
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Custom Data")
    create_test_frame(root)
    root.mainloop()
