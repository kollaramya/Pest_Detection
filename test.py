import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import torch
import cv2
import matplotlib.pyplot as plt
import pathlib
import requests

# Replace PosixPath with WindowsPath to handle Windows file paths
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

def browse_image():
    file_path = filedialog.askopenfilename()
    path_label.config(text="Selected Image: " + file_path)

    results = model1(file_path)
    pest_name = extract_pest_name(results)
    show_pest_dialog(pest_name)
    send_to_esp(pest_name)
    results.show()

def extract_pest_name(results):
    pest_name = None
    if results.xyxy[0] is not None:
        classes = results.names[int(results.xyxy[0][0][-1])]
        pest_name = classes
    return pest_name

def show_pest_dialog(pest_name):
    if pest_name:
        messagebox.showinfo("Detected Pest", f"The detected pest is: {pest_name}")
    else:
        messagebox.showinfo("Detected Pest", "No pest detected.")

def send_to_esp(pest_name):
    if pest_name:
        url = 'http://192.168.1.7/display'
        data = {'pest_name': pest_name}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("Pest information sent to ESP8266 successfully.")
            else:
                print("Failed to send pest information to ESP8266.")
        except Exception as e:
            print("Error:", e)
    else:
        print("No pest detected to send to ESP8266.")

root = tk.Tk()
root.title("Image Selection")

browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack(pady=10)

path_label = tk.Label(root, text="Selected Image: ", wraplength=300)
path_label.pack()

model1 = torch.hub.load('ultralytics/yolov5', 'custom', r"C:\Users\DELL\yolov5\best.pt")

root.mainloop()
