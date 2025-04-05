import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import threading
import scipy.io.wavfile as wav
import os
from datetime import datetime

class AudioRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("录音小窗口")
        self.recording = False
        self.fs = 44100
        self.audio_data = []

        self.record_button = tk.Button(master, text="开始录音", command=self.toggle_recording, width=20, height=2)
        self.record_button.pack(padx=10, pady=10)

        self.play_button = tk.Button(master, text="试听音频", command=self.open_playback_window, width=20, height=2)
        self.play_button.pack(padx=10, pady=10)

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.audio_data = []
        self.record_button.config(text="停止录音")
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(text="开始录音")
        self.recording_thread.join()

        audio_np = np.concatenate(self.audio_data, axis=0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.wav"
        wav.write(filename, self.fs, audio_np)
        print(f"✅ 录音已保存为 {filename}")

    def record(self):
        with sd.InputStream(samplerate=self.fs, channels=1, dtype='float32', callback=self.callback):
            while self.recording:
                sd.sleep(100)

    def callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.audio_data.append(indata.copy())

    def open_playback_window(self):
        win = tk.Toplevel(self.master)
        win.title("选择时间试听录音")

        now = datetime.now()
        entries = {}
        labels = ['年', '月', '日', '时', '分', '秒']
        formats = ['%Y', '%m', '%d', '%H', '%M', '%S']
        defaults = [now.strftime(fmt) for fmt in formats]

        for i, (label, default) in enumerate(zip(labels, defaults)):
            tk.Label(win, text=label).grid(row=0, column=i)
            spin = tk.Spinbox(win, from_=0, to=99 if label == '年' else 59, width=4)
            spin.delete(0, tk.END)
            spin.insert(0, default)
            spin.grid(row=1, column=i)
            entries[label] = spin

        def try_play():
            try:
                y = int(entries['年'].get())
                mo = int(entries['月'].get())
                d = int(entries['日'].get())
                h = int(entries['时'].get())
                mi = int(entries['分'].get())
                s = int(entries['秒'].get())

                filename = f"{y:04}{mo:02}{d:02}_{h:02}{mi:02}{s:02}.wav"
                if not os.path.exists(filename):
                    messagebox.showerror("错误", f"找不到文件：{filename}")
                    return

                samplerate, data = wav.read(filename)
                threading.Thread(target=sd.play, args=(data, samplerate)).start()
                messagebox.showinfo("正在播放", f"播放文件：{filename}")
            except Exception as e:
                messagebox.showerror("错误", str(e))

        play_btn = tk.Button(win, text="播放", command=try_play, width=10)
        play_btn.grid(row=2, column=0, columnspan=6, pady=10)

def run():
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()
