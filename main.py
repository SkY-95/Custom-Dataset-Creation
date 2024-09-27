import tkinter as tk
from tkinter import Menu, messagebox
from PIL import Image, ImageTk
import itertools
import subprocess
import scrap  # Import the refactored scrap module
import custom  # Import the refactored custom module
import train  # Import the refactored train module
import test  # Import the refactored test module
import image_filter  # Import the image_filter module
import image_augmentation  # Import the image_augmentation module

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Home Page Interface")
        self.geometry("800x600")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create menu bar
        self.create_menu_bar()

        # Set background image
        self.set_background()

        # Create image slideshow
        self.image_slideshow()

        # Create heading and paragraph
        self.create_heading()
        self.create_paragraph()

        # Bind the configure event to update the background
        self.bind("<Configure>", self.on_resize)

    def create_menu_bar(self):
        menubar = Menu(self)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Home", command=self.show_main_page)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        tool_menu = Menu(menubar, tearoff=0)
        
        custom_menu = Menu(tool_menu, tearoff=0)
        custom_menu.add_command(label="Scrap", command=self.show_scrap_page)
        custom_menu.add_command(label="Custom Data", command=self.show_custom_data_page)
        custom_menu.add_command(label="Train", command=self.show_train_page)
        custom_menu.add_command(label="Test", command=self.show_test_page)
        tool_menu.add_cascade(label="Custom", menu=custom_menu)
        
        imagesegmentation_menu = Menu(tool_menu, tearoff=0)
        imagesegmentation_menu.add_command(label="Image Filter", command=self.show_image_filter_page)
        imagesegmentation_menu.add_command(label="Image Augmentation", command=self.show_image_augmentation_page)
        tool_menu.add_cascade(label="image process", menu=imagesegmentation_menu)

        menubar.add_cascade(label="Tool", menu=tool_menu)

        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def set_background(self):
        self.bg_image = Image.open("6.jpeg")
        self.bg_label = tk.Label(self.main_frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.update_background()

    def on_resize(self, event):
        self.update_background()

    def update_background(self):
        try:
            width = self.winfo_width()
            height = self.winfo_height()
            resized_image = self.bg_image.resize((width, height), Image.LANCZOS)
            self.bg = ImageTk.PhotoImage(resized_image)
            self.bg_label.config(image=self.bg)
            self.bg_label.image = self.bg
        except:
            pass

    def image_slideshow(self):
        self.images = [
            "img10.jpg"
        ]
        self.image_objects = [
            ImageTk.PhotoImage(Image.open(img).resize((400, 400), Image.LANCZOS))
            for img in self.images
        ]
        self.image_cycle = itertools.cycle(self.image_objects)
        self.slideshow_label = tk.Label(self.main_frame)
        self.slideshow_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.update_slideshow()

    def update_slideshow(self):
        next_image = next(self.image_cycle)
        if self.slideshow_label.winfo_exists():  # Check if the label still exists
            self.slideshow_label.config(image=next_image)
            self.after(2000, self.update_slideshow)

    def create_heading(self):
        heading_label = tk.Label(
            self.main_frame,
            text="Welcome to Our Service",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="black"  # Ensuring the background color matches the bg image
        )
        heading_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    def create_paragraph(self):
        paragraph_text = "Object localization is one of the image recognition tasks along with image classification and object detection. Though object detection and object localization are sometimes used interchangeably, they are not the same."
        paragraph_label = tk.Label(
            self.main_frame,
            text=paragraph_text,
            wraplength=600,
            justify="center",
            font=("Helvetica", 12),
            fg="white",
            bg="black",
        )
        paragraph_label.place(relx=0.5, rely=0.94, anchor=tk.CENTER)

    def show_main_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.set_background()
        self.image_slideshow()
        self.create_heading()
        self.create_paragraph()

    def show_scrap_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        scrap.run_scraper(self.main_frame)

    def show_custom_data_page(self):
        self.clear_frame()
        custom_frame = custom.create_custom_frame(self.main_frame)
        custom_frame.pack(fill=tk.BOTH, expand=True)

    def show_test_page(self):
        self.clear_frame()
        test_frame = test.create_test_frame(self.main_frame)
        test_frame.pack(fill=tk.BOTH, expand=True)

    def show_train_page(self):
        self.clear_frame()
        train_frame = train.create_train_frame(self.main_frame)
        train_frame.pack(fill=tk.BOTH, expand=True)

    def show_image_filter_page(self):
        self.clear_frame()
        filter_frame = image_filter.create_image_filter_frame(self.main_frame)
        filter_frame.pack(fill=tk.BOTH, expand=True)

    def show_image_augmentation_page(self):
        self.clear_frame()
        augmentation_frame = image_augmentation.create_image_augmentation_frame(self.main_frame)
        augmentation_frame.pack(fill=tk.BOTH, expand=True)

    def open_display(self):
        try:
            subprocess.Popen(["python", "display.py"], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute script: {e}")

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
