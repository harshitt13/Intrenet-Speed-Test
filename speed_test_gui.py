import tkinter as tk
from tkinter import ttk, Canvas
import speedtest
import math

class SpeedTestApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("800x600")

        # Create the widgets for the application
        self.create_widgets()

    def create_widgets(self):
        # Create and pack the main label
        ttk.Label(self.root, text="Internet Speed Test", font=("Helvetica", 16)).pack(pady=20)

        # Create and pack labels for displaying speed test results
        self.download_label = self.create_label("Download Speed: ")
        self.upload_label = self.create_label("Upload Speed: ")
        self.ping_label = self.create_label("Ping: ")

        # Create and pack the start test button
        ttk.Button(self.root, text="Start Test", command=self.run_speed_test).pack(pady=20)

        # Create and pack canvases for speedometers
        self.download_canvas = self.create_canvas(side=tk.LEFT)
        self.upload_canvas = self.create_canvas(side=tk.RIGHT)

    def create_label(self, text):
        # Helper method to create and pack a label
        label = ttk.Label(self.root, text=text, font=("Helvetica", 12))
        label.pack(pady=10)
        return label

    def create_canvas(self, **kwargs):
        # Helper method to create and pack a canvas
        canvas = Canvas(self.root, width=200, height=200)
        canvas.pack(padx=20, **kwargs)
        return canvas

    def run_speed_test(self):
        # Run the speed test and update the UI with the results
        st = speedtest.Speedtest()
        st.download()
        st.upload()

        # Convert speeds to Mbps
        download_speed = st.results.download / 1_000_000
        upload_speed = st.results.upload / 1_000_000
        ping = st.results.ping

        # Update the labels with the results
        self.update_labels(download_speed, upload_speed, ping)
        # Draw the speedometers with the results
        self.draw_speedometer(self.download_canvas, download_speed, "Download")
        self.draw_speedometer(self.upload_canvas, upload_speed, "Upload")

    def update_labels(self, download_speed, upload_speed, ping):
        # Update the text of the labels with the speed test results
        self.download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        self.upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        self.ping_label.config(text=f"Ping: {ping} ms")

    def draw_speedometer(self, canvas, speed, label):
        # Draw a speedometer on the given canvas
        canvas.delete("all")
        canvas.create_arc((10, 10, 190, 190), start=0, extent=180, fill="white", outline="black", width=2)
        angle = (speed / 100) * 180  # Calculate the angle for the speedometer needle
        x = 100 + 90 * math.cos(math.radians(angle))
        y = 100 - 90 * math.sin(math.radians(angle))
        canvas.create_line(100, 100, x, y, fill="red", width=2)
        canvas.create_text(100, 120, text=f"{label} Speed", font=("Helvetica", 10))
        canvas.create_text(100, 140, text=f"{speed:.2f} Mbps", font=("Helvetica", 12))

if __name__ == "__main__":
    # Create the main application window and run the application
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()
