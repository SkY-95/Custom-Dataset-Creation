# scrap.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import requests
import io
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

scraped_folders = []

def run_scraper(parent):
    def get_images_by_class(wd, class_name, max_images, download_folder, progress_var, progress_label, open_folder_button):
        try:
            url = f"https://www.google.com/search?q={class_name}&tbm=isch"
            wd.get(url)

            image_urls = set()
            while len(image_urls) < max_images:
                wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                thumbnails = WebDriverWait(wd, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//img[@class="YQ4gaf"]'))
                )
                for img in thumbnails[len(image_urls):max_images]:
                    try:
                        img.click()
                        time.sleep(1)
                    except:
                        continue
                    images = WebDriverWait(wd, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//img[@class="YQ4gaf"]'))
                    )
                    for image in images:
                        if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                            image_urls.add(image.get_attribute('src'))
                            progress_label.config(text=f"Found {len(image_urls)} images.")
                            if len(image_urls) >= max_images:
                                break
            for i, url in enumerate(image_urls):
                download_image(download_folder, url, f"image_{i}.jpg", progress_var, max_images, progress_label)
            progress_label.config(text=f"Downloaded {len(image_urls)} images.")
            messagebox.showinfo("Success", f"Images have been saved in {download_folder}")
            scraped_folders.append(download_folder)
            open_folder_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_image(download_folder, url, file_name, progress_var, max_images, progress_label):
        try:
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            file_path = os.path.join(download_folder, file_name)
            with open(file_path, "wb") as f:
                image.save(f, "JPEG")
            progress_var.set(int((len(os.listdir(download_folder)) / max_images) * 100))
            progress_label.config(text=f"Downloaded {file_name}")
        except Exception as e:
            print(f"Failed to download {file_name} - {e}")

    def open_folder():
        global scraped_folders

        def show_images_in_folder(selected_folder):
            image_window = tk.Toplevel()
            image_window.title(f"Images in {selected_folder}")

            image_frame = tk.Frame(image_window)
            image_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

            images = [os.path.join(selected_folder, img) for img in os.listdir(selected_folder) if img.endswith(('jpg', 'jpeg', 'png'))]
            for i, img_path in enumerate(images):
                img = Image.open(img_path)
                img.thumbnail((150, 150))
                img = ImageTk.PhotoImage(img)
                panel = tk.Label(image_frame, image=img)
                panel.image = img
                panel.grid(row=i // 5, column=i % 5, padx=5, pady=5)

        folder_window = tk.Toplevel()
        folder_window.title("Scraped Folders")

        folders_frame = tk.Frame(folder_window)
        folders_frame.pack(padx=20, pady=20)

        def create_folder_box(folder_path, folder_name):
            box_frame = tk.Frame(folders_frame, width=150, height=150, borderwidth=1, relief="solid")
            box_frame.pack_propagate(False)
            box_frame.grid(row=folders_frame.grid_size()[1] // 5, column=folders_frame.grid_size()[1] % 5, padx=10, pady=10)

            try:
                images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(('jpg', 'jpeg', 'png'))]
                if images:
                    first_image_path = images[0]
                    img = Image.open(first_image_path)
                    img.thumbnail((150, 150))
                    img = ImageTk.PhotoImage(img)
                    image_label = tk.Label(box_frame, image=img)
                    image_label.image = img
                    image_label.pack(pady=5)
                folder_label = tk.Label(box_frame, text=folder_name, wraplength=150, anchor='center')
                folder_label.pack(pady=5)
                box_frame.bind("<Button-1>", lambda e, path=folder_path: show_images_in_folder(path))
            except Exception as e:
                print(f"Failed to create box for {folder_name} - {e}")

        for folder in scraped_folders:
            folder_name = os.path.basename(folder)
            create_folder_box(folder, folder_name)

    def start_scraping(image_class_entry, progress_var, progress_label, download_folder_label, wd, open_folder_button):
        image_class = image_class_entry.get()
        if not image_class:
            messagebox.showerror("Input Error", "Please enter a class name.")
            return
        folder_name = simpledialog.askstring("Folder Name", "Enter the folder name to save images:")
        if not folder_name:
            return
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), r'C:\Users\maqwi\Desktop\major_project[1]\major_project\scrap')
        download_folder = os.path.join(desktop_path, folder_name)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        download_folder_label.config(text=f"Download Folder: {download_folder}")
        max_images = 100
        threading.Thread(target=get_images_by_class, args=(wd, image_class, max_images, download_folder, progress_var, progress_label, open_folder_button)).start()

    CHROMEDRIVER_PATH = r"C:\Users\maqwi\Desktop\major_project[1]\major_project\chromedriver.exe"
    service = Service(CHROMEDRIVER_PATH)
    wd = webdriver.Chrome(service=service)

    scraper_frame = tk.Frame(parent)
    scraper_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(scraper_frame, text="Enter Image Class Name:").grid(row=0, column=0, padx=10, pady=10)
    image_class_entry = ttk.Entry(scraper_frame)
    image_class_entry.grid(row=0, column=1, padx=10, pady=10)

    scrape_button = ttk.Button(scraper_frame, text="Start Scraping", command=lambda: start_scraping(image_class_entry, progress_var, progress_label, download_folder_label, wd, open_folder_button))
    scrape_button.grid(row=1, column=0, columnspan=2, pady=10)

    progress_label = tk.Label(scraper_frame, text="Progress:")
    progress_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(scraper_frame, variable=progress_var, maximum=100)
    progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    download_folder_label = tk.Label(scraper_frame, text="Download Folder: ")
    download_folder_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    open_folder_button = ttk.Button(scraper_frame, text="Open Scraped Folders", state=tk.DISABLED, command=open_folder)
    open_folder_button.grid(row=5, column=0, columnspan=2, pady=10)

    return scraper_frame
