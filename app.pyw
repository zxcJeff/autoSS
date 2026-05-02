import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import requests
import os
import zipfile
import sys
import queue
import time
import re

GITHUB_OWNER = "zxcJeff"
GITHUB_REPO = "autoSS"
CURRENT_VERSION = "1.1.6"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

window = tk.Tk()
window.title("I51 | AutoSS v{}".format(CURRENT_VERSION))
window.geometry("650x780")

try:
    window.iconbitmap(os.path.join(SCRIPT_DIR, r"icoFile\icon.ico"))
except:
    pass

window.resizable(False, False)
window.config(bg="#1e1e1e")

process = None
process_stdin = None
output_queue = queue.Queue()

def strip_ansi_codes(text):
    """Remove ANSI escape sequences from text"""
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    ansi_escape2 = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    text = ansi_escape2.sub('', text)
    return text

def update_output_display():
    """Update the output text widget with queued messages"""
    try:
        while True:
            msg = output_queue.get_nowait()
            output_text.insert(tk.END, msg)
            output_text.see(tk.END)
            output_text.update_idletasks()
    except queue.Empty:
        pass
    finally:
        window.after(100, update_output_display)

def send_cookies_accepted():
    """Send Enter key to accept cookies/bypass CAPTCHA"""
    global process_stdin
    if process_stdin and process:
        try:
            process_stdin.write('\n')
            process_stdin.flush()
            output_queue.put("\n[ACTION] 🍪 Cookies Accepted - Enter key sent\n")
            status_label.config(text="Cookies accepted", fg="#4CAF50")
            
            cookies_button.config(bg="#66bb6a")
            window.after(200, lambda: cookies_button.config(bg="#4CAF50" if not headless_var.get() else "#9c27b0"))
        except Exception as e:
            output_queue.put(f"[ERROR] Could not send signal: {str(e)}\n")
            status_label.config(text="Failed to send signal", fg="#f44336")
    else:
        output_queue.put("[WARNING] No active process running\n")
        status_label.config(text="No active process", fg="#ff9800")

def run_script():
    global process
    
    auto_path = os.path.join(SCRIPT_DIR, "auto.py")
    
    if not os.path.exists(auto_path):
        status_label.config(text="Error: auto.py not found!", fg="red")
        output_queue.put("[ERROR] auto.py not found!\n")
        return
    
    output_text.delete(1.0, tk.END)
    
    if headless_var.get():
        headless_mode = "True"
    else:
        headless_mode = "False"
    
    browser_on.config(state="disabled")
    browser_off.config(state="disabled")
    status_label.config(text="▶ Script is running...", fg="#4CAF50")
    output_queue.put("[INFO] Starting AutoSS script...\n")
    output_queue.put(f"[INFO] Headless mode: {headless_mode}\n")
    output_queue.put(f"[INFO] Script path: {auto_path}\n")
    output_queue.put("-" * 60 + "\n\n")
    
    if not headless_var.get():
        cookies_button.pack(pady=(10, 5))
    else:
        cookies_button.pack_forget()
    
    button_run.config(state="disabled")
    button_check_updates.config(state="disabled")
    button_stop.config(state="normal")
    
    process_thread = threading.Thread(target=start_process, args=(headless_mode, auto_path))
    process_thread.daemon = True
    process_thread.start()

def start_process(headless_mode, auto_path):
    global process, process_stdin
    try:
        output_queue.put("[INFO] Executing script...\n")
        
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            process = subprocess.Popen(
                [sys.executable, "-u", auto_path, headless_mode],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                universal_newlines=True,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            process = subprocess.Popen(
                [sys.executable, "-u", auto_path, headless_mode],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                universal_newlines=True
            )
        
        process_stdin = process.stdin
        
        for line in iter(process.stdout.readline, ''):
            if line:
                clean_line = strip_ansi_codes(line)
                clean_line = clean_line.replace('\r', '')
                if clean_line.strip():
                    output_queue.put(f"  {clean_line}\n")
                    
                    if any(keyword in clean_line.lower() for keyword in ['captcha', 'press enter', 'input', 'enter', 'skip', 'verification', 'cookie']):
                        output_queue.put("\n" + "!" * 60 + "\n")
                        output_queue.put("⚠️  SCRIPT WAITING FOR INPUT! ⚠️\n")
                        output_queue.put("Click '🍪 COOKIES ACCEPTED' button below\n")
                        output_queue.put("!" * 60 + "\n\n")

                        cookies_button.config(bg="#ff6b6b")
                        window.after(1000, lambda: cookies_button.config(bg="#4CAF50" if not headless_var.get() else "#9c27b0"))
                
                time.sleep(0.01)
        
        process.wait()
        
        output_queue.put("\n" + "-" * 60 + "\n")
        if process.returncode == 0:
            output_queue.put("[SUCCESS] ✓ Script completed successfully!\n")
            status_label.config(text="✓ Script completed", fg="#4CAF50")
        else:
            output_queue.put(f"[ERROR] ✗ Script exited with code {process.returncode}\n")
            status_label.config(text="✗ Script error", fg="#f44336")
        
        process_stdin = None
            
    except Exception as e:
        error_msg = f"[ERROR] {str(e)}\n"
        output_queue.put(error_msg)
        status_label.config(text=f"Error: {str(e)}", fg="#f44336")
        import traceback
        output_queue.put(f"[ERROR] Details: {traceback.format_exc()}\n")
    finally:
        button_run.config(state="normal")
        button_check_updates.config(state="normal")
        button_stop.config(state="disabled")
        browser_on.config(state="normal")
        browser_off.config(state="normal")
        process = None
        process_stdin = None

        cookies_button.pack_forget()

def stop_script():
    global process, process_stdin
    if process:
        output_queue.put("\n[WARNING] Stopping script...\n")
        try:
            if process_stdin:
                process_stdin.close()
            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()
        except:
            pass
        process = None
        process_stdin = None
        status_label.config(text="■ Script stopped", fg="#f44336")
        output_queue.put("[INFO] Script stopped by user\n")
        button_run.config(state="normal")
        button_check_updates.config(state="normal")
        button_stop.config(state="disabled")
        browser_on.config(state="normal")
        browser_off.config(state="normal")

        cookies_button.pack_forget()
    else:
        output_queue.put("[WARNING] No active process to stop\n")
        status_label.config(text="No active process to stop", fg="#ff9800")

def check_for_updates():
    status_label.config(text="Checking for updates...", fg="#2196F3")
    output_queue.put("[INFO] Checking for updates...\n")
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    window.after(2000, lambda: fetch_latest_release(url))

def fetch_latest_release(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        release_data = response.json()

        if 'tag_name' in release_data:
            latest_version = release_data['tag_name']
            
            if compare_versions(latest_version, CURRENT_VERSION):
                status_label.config(text=f"Update available: {latest_version}", fg="#4CAF50")
                output_queue.put(f"[INFO] Update available: {latest_version}\n")
                button_check_updates.config(text="Download Update", command=lambda: download_update(release_data))
            else:
                status_label.config(text="✓ Latest version", fg="#4CAF50")
                output_queue.put("[INFO] You are on the latest version\n")
                button_check_updates.config(state="disabled")
        else:
            status_label.config(text="Error: No valid release found", fg="#f44336")
            output_queue.put("[ERROR] No valid release found\n")
    
    except requests.exceptions.RequestException as e:
        status_label.config(text=f"Error: {str(e)}", fg="#f44336")
        output_queue.put(f"[ERROR] {str(e)}\n")

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
    status_label.config(text=f"Downloading update...", fg="#2196F3")
    output_queue.put("[INFO] Downloading update...\n")
    threading.Thread(target=download_file, args=(download_url,), daemon=True).start()

def download_file(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_name = "update.zip"
        total_size = int(response.headers.get('content-length', 0))
        
        with open(file_name, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    output_queue.put(f"\r[INFO] Downloading: {percent:.1f}%")
        
        output_queue.put(f"\n[INFO] Downloaded {file_name}\n")
        status_label.config(text=f"Downloaded {file_name}", fg="#4CAF50")
        extract_file(file_name)
    except requests.exceptions.RequestException as e:
        output_queue.put(f"[ERROR] Download failed: {str(e)}\n")
        status_label.config(text=f"Error downloading: {str(e)}", fg="#f44336")

def extract_file(file_path):
    try:
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                extract_to = SCRIPT_DIR
                output_queue.put("[INFO] Extracting files...\n")
                
                for member in zip_ref.namelist():
                    if 'icoFile' in member:
                        continue
                    
                    filename = os.path.basename(member)
                    
                    if filename:
                        extracted_path = os.path.join(extract_to, filename)
                        with open(extracted_path, "wb") as f_out:
                            f_out.write(zip_ref.read(member))
                        output_queue.put(f"[INFO] Extracted: {filename}\n")
            
            output_queue.put("[SUCCESS] ✓ Update completed! Please restart the application.\n")
            status_label.config(text="✓ Update complete! Restart app.", fg="#4CAF50")
            os.remove(file_path)
    except Exception as e:
        output_queue.put(f"[ERROR] Extract failed: {str(e)}\n")
        status_label.config(text=f"Error extracting: {str(e)}", fg="#f44336")

def set_headless_mode():
    headless_var.set(True)
    update_button_styles()
    output_queue.put("[INFO] Switched to Browserless Mode\n")
    # Hide cookies button in headless mode
    cookies_button.pack_forget()

def set_browser_mode():
    headless_var.set(False)
    update_button_styles()
    output_queue.put("[INFO] Switched to Browser Visible Mode\n")
    # Show cookies button only if script is running
    if process and process_stdin:
        cookies_button.pack(pady=(10, 5))

def clear_output():
    """Clear the console output"""
    output_text.delete(1.0, tk.END)
    output_queue.put("[INFO] Console cleared\n")

# Variables
headless_var = tk.BooleanVar()
headless_var.set(True)

# Main container
main_frame = tk.Frame(window, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True, padx=20, pady=15)

# Title
title_label = tk.Label(main_frame, text="⚡AUTO SS⚡", font=("Segoe UI", 16, "bold"), 
                       bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=(0, 10))

# Mode selection
mode_frame = tk.Frame(main_frame, bg="#1e1e1e")
mode_frame.pack(pady=(0, 15))

browser_off = tk.Button(mode_frame, text="Browserless Mode", command=set_headless_mode,
                        bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                        relief="flat", padx=15, pady=5, width=15)
browser_off.pack(side="left", padx=5)

browser_on = tk.Button(mode_frame, text="Accept Cookies", command=set_browser_mode,
                       bg="#3d3d3d", fg="#cccccc", font=("Segoe UI", 10),
                       relief="flat", padx=15, pady=5, width=15)
browser_on.pack(side="left", padx=5)

# Action buttons
button_run = tk.Button(main_frame, text="▶ RUN SCRIPT", command=run_script,
                       bg="#2196F3", fg="white", font=("Segoe UI", 11, "bold"),
                       relief="flat", padx=20, pady=8, width=20)
button_run.pack(pady=(0, 8))

button_stop = tk.Button(main_frame, text="■ STOP SCRIPT", command=stop_script,
                        bg="#f44336", fg="white", font=("Segoe UI", 11, "bold"),
                        relief="flat", padx=20, pady=8, width=20, state="disabled")
button_stop.pack(pady=(0, 8))

# Update and Clear buttons frame
action_frame = tk.Frame(main_frame, bg="#1e1e1e")
action_frame.pack(pady=(0, 10))

button_check_updates = tk.Button(action_frame, text="🔄 CHECK UPDATES", command=check_for_updates,
                                 bg="#ff9800", fg="white", font=("Segoe UI", 9),
                                 relief="flat", padx=10, pady=6, width=15)
button_check_updates.pack(side="left", padx=5)

button_clear = tk.Button(action_frame, text="🗑️ CLEAR", command=clear_output,
                         bg="#555555", fg="white", font=("Segoe UI", 9),
                         relief="flat", padx=10, pady=6, width=15)
button_clear.pack(side="left", padx=5)

# Console output area
output_frame = tk.Frame(main_frame, bg="#1e1e1e")
output_frame.pack(fill="both", expand=True, pady=(5, 5))

output_label = tk.Label(output_frame, text="📟 CONSOLE OUTPUT", font=("Segoe UI", 9, "bold"),
                        bg="#1e1e1e", fg="#888888")
output_label.pack(anchor="w", pady=(0, 3))

output_text = scrolledtext.ScrolledText(
    output_frame,
    height=16,
    bg="#0a0a0a",
    fg="#00ff00",
    font=("Consolas", 9),
    relief="flat",
    borderwidth=1,
    wrap=tk.WORD,
    insertbackground="white"
)
output_text.pack(fill="both", expand=True)

# Cookies Accepted button (below console display)
cookies_frame = tk.Frame(main_frame, bg="#1e1e1e")
cookies_frame.pack(fill="x", pady=(5, 5))

cookies_button = tk.Button(cookies_frame, text="🍪 COOKIES ACCEPTED", command=send_cookies_accepted,
                           bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"),
                           relief="flat", padx=20, pady=10, width=25)

# Status bar
status_frame = tk.Frame(main_frame, bg="#2d2d2d", height=30)
status_frame.pack(fill="x", pady=(5, 0))
status_frame.pack_propagate(False)

status_label = tk.Label(status_frame, text="✓ Ready - Headless mode", fg="#4CAF50", 
                        bg="#2d2d2d", font=("Segoe UI", 9))
status_label.pack(expand=True, fill="both")

def update_button_styles():
    if headless_var.get():
        browser_off.config(bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"))
        browser_on.config(bg="#3d3d3d", fg="#cccccc", font=("Segoe UI", 10))
        status_label.config(text="✓ Ready - Headless mode", fg="#4CAF50")
        # Hide cookies button in headless mode
        cookies_button.pack_forget()
    else:
        browser_on.config(bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"))
        browser_off.config(bg="#3d3d3d", fg="#cccccc", font=("Segoe UI", 10))
        status_label.config(text="✓ Ready - Browser visible", fg="#4CAF50")
        # Only show cookies button if script is running
        if process and process_stdin:
            cookies_button.pack(pady=(10, 5))

# Trace for variable changes
if hasattr(headless_var, 'trace_add'):
    headless_var.trace_add('write', lambda *args: update_button_styles())
else:
    headless_var.trace('w', lambda *args: update_button_styles())

# Hover effects
def on_hover_enter(event, button):
    if button == browser_on:
        if not headless_var.get():
            button.config(bg="#66bb6a")
        else:
            button.config(bg="#5a5a5a")
    elif button == browser_off:
        if headless_var.get():
            button.config(bg="#66bb6a")
        else:
            button.config(bg="#5a5a5a")
    elif button == button_run:
        button.config(bg="#42a5f5")
    elif button == button_stop:
        button.config(bg="#ef5350")
    elif button == button_check_updates:
        button.config(bg="#ffa726")
    elif button == cookies_button:
        button.config(bg="#66bb6a")
    elif button == button_clear:
        button.config(bg="#777777")

def on_hover_leave(event, button):
    if button == browser_on:
        if headless_var.get():
            button.config(bg="#3d3d3d")
        else:
            button.config(bg="#4CAF50")
    elif button == browser_off:
        if headless_var.get():
            button.config(bg="#4CAF50")
        else:
            button.config(bg="#3d3d3d")
    elif button == button_run:
        button.config(bg="#2196F3")
    elif button == button_stop:
        button.config(bg="#f44336")
    elif button == button_check_updates:
        button.config(bg="#ff9800")
    elif button == cookies_button:
        button.config(bg="#4CAF50")
    elif button == button_clear:
        button.config(bg="#555555")

# Apply hover effects
for button in [browser_on, browser_off, button_run, button_stop, button_check_updates, cookies_button, button_clear]:
    button.bind("<Enter>", lambda e, btn=button: on_hover_enter(e, btn))
    button.bind("<Leave>", lambda e, btn=button: on_hover_leave(e, btn))

# Start output display update loop
update_output_display()

# Initialize styles
update_button_styles()

window.mainloop()
