import sys
import subprocess
import re
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSlider, QComboBox, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class MonitorControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.monitors = []  # Stores list of (id, name)
        self.init_ui()
        self.detect_monitors()

    def init_ui(self):
        self.setWindowTitle("Monitor Control (PyQt6)")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()

        # Monitor Selection
        self.label_select = QLabel("Select Monitor:")
        self.combo_monitors = QComboBox()
        self.combo_monitors.currentIndexChanged.connect(self.sync_values)
        
        # Brightness Section
        self.label_bright = QLabel("Brightness: --")
        self.slider_bright = QSlider(Qt.Orientation.Horizontal)
        self.slider_bright.setRange(0, 100)
        self.slider_bright.valueChanged.connect(lambda v: self.label_bright.setText(f"Brightness: {v}%"))

        # Contrast Section
        self.label_cont = QLabel("Contrast: --")
        self.slider_cont = QSlider(Qt.Orientation.Horizontal)
        self.slider_cont.setRange(0, 100)
        self.slider_cont.valueChanged.connect(lambda v: self.label_cont.setText(f"Contrast: {v}%"))

        # Buttons
        self.btn_apply = QPushButton("Apply Settings")
        self.btn_apply.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; padding: 10px;")
        self.btn_apply.clicked.connect(self.apply_settings)

        self.btn_refresh = QPushButton("Rescan Monitors")
        self.btn_refresh.clicked.connect(self.detect_monitors)

        # Add to Layout
        layout.addWidget(self.label_select)
        layout.addWidget(self.combo_monitors)
        layout.addSpacing(20)
        layout.addWidget(self.label_bright)
        layout.addWidget(self.slider_bright)
        layout.addSpacing(10)
        layout.addWidget(self.label_cont)
        layout.addWidget(self.slider_cont)
        layout.addSpacing(20)
        layout.addWidget(self.btn_apply)
        layout.addWidget(self.btn_refresh)

        self.setLayout(layout)

    def detect_monitors(self):
        """Finds monitors and populates the dropdown."""
        self.combo_monitors.clear()
        self.monitors = []
        try:
            output = subprocess.check_output(["ddcutil", "detect"]).decode()
            
            # Parsing logic
            current_id = None
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("Display"):
                    parts = line.split()
                    if len(parts) >= 2: current_id = parts[1]
                if "Model:" in line and current_id:
                    model = line.split("Model:")[1].strip()
                    self.monitors.append((current_id, model))
                    self.combo_monitors.addItem(f"Display {current_id}: {model}")
                    current_id = None

            if not self.monitors:
                self.monitors = [("1", "Default Display")]
                self.combo_monitors.addItem("1: Default Display")

            self.sync_values()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not detect monitors: {e}")

    def get_vcp(self, display_id, code):
        """Fetch current hardware value."""
        try:
            res = subprocess.check_output(
                ["ddcutil", "getvcp", str(code), "--display", str(display_id), "--terse"],
                stderr=subprocess.DEVNULL
            ).decode().split()
            return int(res[3])
        except:
            return 50

    def sync_values(self):
        """Syncs sliders with the selected monitor's actual current state."""
        if not self.monitors: return
        idx = self.combo_monitors.currentIndex()
        display_id = self.monitors[idx][0]
        
        b_val = self.get_vcp(display_id, 10)
        c_val = self.get_vcp(display_id, 12)
        
        self.slider_bright.setValue(b_val)
        self.slider_cont.setValue(c_val)

    def apply_settings(self):
        """Sends the slider values to the monitor hardware."""
        idx = self.combo_monitors.currentIndex()
        display_id = self.monitors[idx][0]
        
        b_val = self.slider_bright.value()
        c_val = self.slider_cont.value()
        
        try:
            # Setting brightness
            subprocess.run(["ddcutil", "setvcp", "10", str(b_val), "--display", display_id], check=True)
            # Setting contrast
            subprocess.run(["ddcutil", "setvcp", "12", str(c_val), "--display", display_id], check=True)
        except Exception as e:
            QMessageBox.warning(self, "Hardware Error", f"Failed to set values: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MonitorControlApp()
    window.show()
    sys.exit(app.exec())
