import tkinter as tk
import serial
import serial.tools.list_ports
import threading
import time

BAUDRATE = 115200

class ESPMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 状态监控")

        self.canvas = tk.Canvas(root, width=200, height=200)
        self.canvas.pack(pady=20)

        self.circle = self.canvas.create_oval(50, 50, 150, 150, fill="gray")

        self.status_label = tk.Label(root, text="未连接", font=("Arial", 14))
        self.status_label.pack()

        self.ser = None
        self.running = True
        self.blink = False

        # 启动线程
        threading.Thread(target=self.connect_loop, daemon=True).start()
        self.update_ui()

    def find_esp32(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.vid in (0x10C4, 0x1A86, 0x303A):  # 常见 VID（含 ESP32-S3/C3）
                return p.device
        return None

    def connect_loop(self):
        while self.running:
            if not self.ser:
                port = self.find_esp32()
                if port:
                    try:
                        self.ser = serial.Serial(port, BAUDRATE, timeout=1)
                        self.status_label.config(text=f"已连接: {port}")
                        threading.Thread(target=self.read_loop, daemon=True).start()
                    except:
                        self.ser = None
            time.sleep(1)

    def read_loop(self):
        while self.ser and self.ser.is_open:
            try:
                line = self.ser.readline().decode().strip()
                if line:
                    self.handle_message(line)
            except:
                self.ser = None
                self.status_label.config(text="断开，重连中...")

    def handle_message(self, msg):
        if msg == "RUNNING":
            self.set_running()
        elif msg == "WAIT":
            self.set_wait()
        elif msg == "DONE":
            self.set_done()

    def set_running(self):
        self.current_state = "RUNNING"
        self.canvas.itemconfig(self.circle, fill="green")

    def set_wait(self):
        self.current_state = "WAIT"

    def set_done(self):
        self.current_state = "DONE"
        self.canvas.itemconfig(self.circle, fill="gray")

    def update_ui(self):
        if hasattr(self, "current_state") and self.current_state == "WAIT":
            self.blink = not self.blink
            color = "red" if self.blink else "gray"
            self.canvas.itemconfig(self.circle, fill=color)

        self.root.after(500, self.update_ui)


if __name__ == "__main__":
    root = tk.Tk()
    app = ESPMonitorApp(root)
    root.mainloop()
