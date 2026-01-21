import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class FlexibleMonitorControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Control")
        self.root.geometry("350x400")

        self.monitors = []  # List of (display_index, model_name)

        # UI Components
        tk.Label(root, text="Monitor Control", font=("Arial", 14, "bold")).pack(pady=10)

        # Monitor Selector
        tk.Label(root, text="Select Display:").pack()
        self.monitor_selector = ttk.Combobox(root, state="readonly", width=30)
        self.monitor_selector.pack(pady=5)

        # Sliders
        self.bright_slider = self.create_slider("Brightness", 10)
        self.cont_slider = self.create_slider("Contrast", 12)

        # Buttons
        tk.Button(root, text="Apply All Settings", command=self.apply_settings,
                  bg="#2196F3", fg="white", height=2).pack(pady=20, fill="x", padx=40)

        tk.Button(root, text="Rescan Monitors", command=self.detect_monitors).pack()

        # Initial Run
        self.detect_monitors()

    def create_slider(self, label, code):
        tk.Label(self.root, text=label).pack(pady=(10,0))
        slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", length=250)
        slider.pack()
        return slider

    def detect_monitors(self):
        """A more robust way to find displays by looking for the 'Display' keyword."""
        self.monitors = []
        try:
            # We use standard output here because terse can be finicky
            output = subprocess.check_output(["ddcutil", "detect"]).decode()

            # Simple line-by-line parsing
            current_idx = None
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("Display"):
                    # Extract the number after "Display"
                    parts = line.split()
                    if len(parts) >= 2:
                        current_idx = parts[1]
                if "Model:" in line and current_idx:
                    model = line.split("Model:")[1].strip()
                    self.monitors.append((current_idx, model))
                    current_idx = None # Reset for next display

            if not self.monitors:
                # FALLBACK: If detection fails, assume at least one display exists
                self.monitors = [("1", "Default Display")]

            self.monitor_selector['values'] = [f"{m[0]}: {m[1]}" for m in self.monitors]
            self.monitor_selector.current(0)
            self.sync_sliders()

        except Exception as e:
            messagebox.showerror("Error", f"Detection failed: {e}")

    def sync_sliders(self):
        """Update sliders with current hardware values."""
        display_id = self.get_selected_id()
        self.bright_slider.set(self.get_vcp_value(display_id, "10"))
        self.cont_slider.set(self.get_vcp_value(display_id, "12"))

    def get_selected_id(self):
        selection = self.monitor_selector.get()
        return selection.split(":")[0] if selection else "1"

    def get_vcp_value(self, display_id, code):
        try:
            output = subprocess.check_output(
                ["ddcutil", "getvcp", code, "--display", display_id, "--terse"]
            ).decode().split()
            return int(output[3])
        except:
            return 50 # Default if read fails

    def apply_settings(self):
        display_id = self.get_selected_id()
        b_val = self.bright_slider.get()
        c_val = self.cont_slider.get()

        try:
            # Apply both settings
            subprocess.run(["ddcutil", "setvcp", "10", str(b_val), "--display", display_id])
            subprocess.run(["ddcutil", "setvcp", "12", str(c_val), "--display", display_id])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlexibleMonitorControl(root)
    root.mainloop()
