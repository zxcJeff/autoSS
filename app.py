import tkinter as tk
import subprocess
import threading
import requests
import os
import zipfile

GITHUB_OWNER = "asdJPasc"
GITHUB_REPO = "AutoSS"
CURRENT_VERSION = "1.1.3"

window = tk.Tk()
window.title("I51 | Autoss v{}".format(CURRENT_VERSION))
window.geometry("270x250")
window.iconbitmap(r"icoFile\icon.ico")
window.resizable(False, False)
window.config(bg="#2e2e2e")

process = None

def run_script():
    global process
    headless_mode = "True" if headless_var.get() else "False"
    browser_on.config(state="disabled")
    browser_off.config(state="disabled")
    status_label.config(text="Script is running...", fg="green")
    process_thread = threading.Thread(target=start_process, args=(headless_mode,))
    process_thread.start()
    button_run.config(state="disabled")
    button_check_updates.config(state="disabled")
    button_stop.config(state="normal")

def start_process(headless_mode):
    global process
    try:
        process = subprocess.Popen(["python", "auto.py", headless_mode])
        process.wait()
        status_label.config(text="Script has stopped", fg="red")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")
    finally:
        button_run.config(state="normal")
        button_check_updates.config(state="normal")
        button_stop.config(state="disabled")
        browser_on.config(state="normal")
        browser_off.config(state="normal")

def stop_script():
    global process
    if process:
        process.terminate()
        process = None
        status_label.config(text="Script is stopped", fg="red")
        button_run.config(state="normal")
        button_check_updates.config(state="normal")
        button_stop.config(state="disabled")
        browser_on.config(state="normal")
        browser_off.config(state="normal")
    else:
        status_label.config(text="No active process to stop", fg="black")

def check_for_updates():
    status_label.config(text="Checking for updates...", fg="blue")
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    window.after(2000, lambda: fetch_latest_release(url))

def fetch_latest_release(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        release_data = response.json()

        if 'tag_name' in release_data:
            latest_version = release_data['tag_name']
            
            # Compare versions
            if compare_versions(latest_version, CURRENT_VERSION):
                status_label.config(text=f"Update available: {latest_version}", fg="green")
                button_check_updates.config(text="Download Update", command=lambda: download_update(release_data))
            else:
                status_label.config(text="You are on the latest version.", fg="green")
                button_check_updates.config(state="disabled")
        else:
            status_label.config(text="Error: No valid release found", fg="red")
    
    except requests.exceptions.RequestException as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

def compare_versions(latest_version, current_version):

    latest_version = latest_version.lstrip('v')
    current_version = current_version.lstrip('v')
    
    latest_parts = [int(x) for x in latest_version.split('.')]
    current_parts = [int(x) for x in current_version.split('.')]
    
    return latest_parts > current_parts

def download_update(release_data):
    if "assets" in release_data and release_data["assets"]:
        download_url = release_data["assets"][0]["browser_download_url"]
    else:
        download_url = release_data["zipball_url"]
    status_label.config(text=f"Downloading update...", fg="blue")
    threading.Thread(target=download_file, args=(download_url,)).start()

def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        file_name = "update.zip"
        with open(file_name, "wb") as f:
            f.write(response.content)
        status_label.config(text=f"Downloaded {file_name}", fg="green")
        extract_file(file_name)
    except requests.exceptions.RequestException as e:
        status_label.config(text=f"Error downloading the file: {str(e)}", fg="red")

def extract_file(file_path):
    try:
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                extract_to = os.getcwd()

                for member in zip_ref.namelist():
                    if 'icoFile' in member:
                        continue

                    filename = os.path.basename(member)

                    if filename:
                        extracted_path = os.path.join(extract_to, filename)
                        with open(extracted_path, "wb") as f_out:
                            f_out.write(zip_ref.read(member))
            
            status_label.config(text="Update completed successfully.", fg="green")
            os.remove(file_path)
    except Exception as e:
        status_label.config(text=f"Error extracting the file: {str(e)}", fg="red")

headless_var = tk.BooleanVar()
headless_var.set(False)

browser_frame = tk.Frame(window, bg="#2e2e2e")
browser_frame.pack(pady=10)

browser_on = tk.Radiobutton(browser_frame, text="Browser: On", variable=headless_var, value=True, bg="#2e2e2e", fg="white", selectcolor="#444444", indicatoron=0)
browser_on.pack(side="left", padx=5)

browser_off = tk.Radiobutton(browser_frame, text="Browser: Off", variable=headless_var, value=False, bg="#2e2e2e", fg="white", selectcolor="#444444", indicatoron=0)
browser_off.pack(side="left", padx=5)

button_run = tk.Button(window, text="Run AutoSS", command=run_script, bg="#444444", fg="white")
button_run.pack(pady=5)

button_stop = tk.Button(window, text="Stop AutoSS", command=stop_script, bg="#444444", fg="white", state="disabled")
button_stop.pack(pady=5)

button_check_updates = tk.Button(window, text="Check for Updates", command=check_for_updates, bg="#444444", fg="white")
button_check_updates.pack(pady=5)

status_label = tk.Label(window, text="AutoSS is idle", fg="white", bg="#2e2e2e")
status_label.pack(pady=5)

window.mainloop()
