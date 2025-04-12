import os
import platform
import tkinter as tk
from tkinter import messagebox
import threading
import time

class ShutdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Shutdown Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.remaining_time = 0
        self.shutdown_scheduled = False
        self.timer_thread = None
        self.cancel_flag = threading.Event()

        # UI Elements
        self.label = tk.Label(root, text="Enter shutdown time (in hours):", font=("Arial", 12))
        self.label.pack(pady=10)

        self.time_entry = tk.Entry(root, font=("Arial", 14), justify="center")
        self.time_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Timer", font=("Arial", 12), command=self.start_shutdown)
        self.start_button.pack(pady=5)

        self.cancel_button = tk.Button(root, text="Cancel Shutdown", font=("Arial", 12), command=self.cancel_shutdown, state=tk.DISABLED)
        self.cancel_button.pack(pady=5)

        self.timer_label = tk.Label(root, text="", font=("Courier", 32, "bold"), fg="red")
        self.timer_label.pack(pady=20)

    def start_shutdown(self):
        try:
            hours = float(self.time_entry.get())
            self.remaining_time = int(hours * 3600)
            if self.remaining_time <= 0:
                raise ValueError

            self.shutdown_scheduled = True
            self.cancel_flag.clear()
            self.cancel_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)

            self.timer_thread = threading.Thread(target=self.update_timer)
            self.timer_thread.start()

            self.schedule_shutdown()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of hours.")

    def schedule_shutdown(self):
        if platform.system() == "Windows":
            os.system(f"shutdown /s /t {self.remaining_time}")
        elif platform.system() == "Linux":
            os.system(f"shutdown -h +{self.remaining_time // 60}")
        else:
            messagebox.showerror("Unsupported OS", "This script only supports Windows and Linux.")

    def cancel_shutdown(self):
        self.cancel_flag.set()
        self.shutdown_scheduled = False
        self.timer_label.config(text="Shutdown Canceled")
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

        if platform.system() == "Windows":
            os.system("shutdown /a")
        elif platform.system() == "Linux":
            os.system("shutdown -c")

    def update_timer(self):
        while self.remaining_time > 0 and not self.cancel_flag.is_set():
            mins, secs = divmod(self.remaining_time, 60)
            hours, mins = divmod(mins, 60)
            time_str = f"{hours:02}:{mins:02}:{secs:02}"
            self.timer_label.config(text=time_str)
            time.sleep(1)
            self.remaining_time -= 1

        if not self.cancel_flag.is_set():
            self.timer_label.config(text="Shutting down...")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownTimerApp(root)
    root.mainloop()
