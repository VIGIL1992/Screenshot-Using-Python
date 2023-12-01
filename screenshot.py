import tkinter as tk
import requests
import platform
import pyautogui
from datetime import datetime

# Function to take a screenshot
def take_screenshot():
    return pyautogui.screenshot()

# Function to upload the screenshot
def upload_screenshot():
    screenshot = take_screenshot()
    screenshot.save("screenshot.png")

    remarks = get_active_window_name()
    phone = "7878787878"  

    url = "https://trogon.info/interview/python/index.php"
    payload = {
        "remarks": remarks,
        "phone": phone
    }
    files = {
        "image": open("screenshot.png", "rb")
    }

    response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        api_response = response.json()
        if api_response.get("status") == "success":
            file_path = api_response["data"]["file_path"]
            remarks = api_response["data"]["remarks"]
            phone = api_response["data"]["phone"]
            timestamp = api_response["data"]["timestamp"]

            success_label.config(text=f"File uploaded successfully!\nRemarks: {remarks}\nPhone: {phone}\nTimestamp: {timestamp}")
        else:
            success_label.config(text="Failed to upload file.")
    else:
        success_label.config(text="Error uploading file. Please try again.")

# Function to get active window name/application name based on platform
def get_active_window_name():
    try:
        current_system = platform.system()
        if current_system == 'Windows':
            import win32gui
            active_app_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        elif current_system == 'Darwin':  # macOS
            # Implement macOS specific code to get active window name
            active_app_name = "Mac App Name"
        elif current_system == 'Linux':
            # Implement Linux specific code to get active window name
            active_app_name = "Linux App Name"
        else:
            active_app_name = "Unknown"
        
        return active_app_name
    except Exception as e:
        print(f"Error getting active window: {e}")
        return "Unknown"

# Create GUI
root = tk.Tk()
root.title("Screenshot Uploader")

# Button to take and upload screenshot
upload_button = tk.Button(root, text="Take and Upload Screenshot", command=upload_screenshot)
upload_button.pack(pady=20)

# Label to display success/failure message and API response details
success_label = tk.Label(root, text="")
success_label.pack()

root.mainloop()
