import tkinter as tk
import threading
import time
import sounddevice as sd
from window import input_window
import numpy as np
import queue
from tkinter import messagebox
import getwav
def bb():
    getwav.run()
a=''
devices = sd.query_devices()
for idx, device in enumerate(devices):
    a+=f"{idx}: {device['name']}"+'\n'
a=int(input_window(msg=f'请选择实体麦克风的设备\n{a}'))
REAL_MIC_INDEX=a

import soundfile as sf

# 加载你要播放的音频文件（WAV 格式最佳）


# 找出设备编号
devices = sd.query_devices()
for i, device in enumerate(devices):
    if "CABLE Input" in device["name"]:
        print(f"找到虚拟音频设备: {device['name']} 设备编号: {i}")
        virtual_device = i
        break
VIRTUAL_MIC_INDEX = virtual_device # 虚拟麦克风（VB-CABLE）的设备编号，例如 5

samplerate = 44100
blocksize = 1024
channels = 1  # 单声道

running_flag = False
worker_thread = None

def background_task(option1, option2, debug_text):
    print(f"任务启动，参数：选项1={option1}, 选项2={option2}, 调试输入='{debug_text}'")
    sb=0
    while running_flag:
        if sb==0 and option2:
            data, fs = sf.read("peng.mp3")
            sd.play(data, fs, device=virtual_device)
            sd.wait()
        if sb==0 and option1:
            audio_queue = queue.Queue(maxsize=20)
            
            def input_callback(indata, frames, time, status):
                if status:
                    print("Input status:", status)
                try:
                    # 将录入的数据复制后放入队列
                    audio_queue.put(indata.copy(), block=False)
                except queue.Full:
                    print("Queue is full! Dropping frames.")
            
            def output_callback(outdata, frames, time, status):
                if status:
                    print("Output status:", status)
                try:
                    # 尝试从队列中获取数据，填充到输出缓冲区
                    data = audio_queue.get(block=False)
                    # 如果数据长度不足，则用0填充
                    if len(data) < len(outdata):
                        outdata[:len(data)] = data
                        outdata[len(data):] = np.zeros((len(outdata) - len(data), channels))
                    else:
                        outdata[:] = data
                except queue.Empty:
                    # 队列为空时输出静音
                    outdata.fill(0)
            
            print("Available audio devices:")
            print(sd.query_devices())
            
            # 同时打开输入流和输出流
            with sd.InputStream(device=REAL_MIC_INDEX,
                                channels=channels,
                                samplerate=samplerate,
                                blocksize=blocksize,
                                callback=input_callback):
                with sd.OutputStream(device=VIRTUAL_MIC_INDEX,
                                     channels=channels,
                                     samplerate=samplerate,
                                     blocksize=blocksize,
                                     callback=output_callback):
                    print("正在转发麦克风音频到虚拟麦克风... 按 Ctrl+C 停止")
                    try:
                        while running_flag:
                            sd.sleep(1000)  # 保持程序运行
                    except KeyboardInterrupt:
                        print("\n程序已停止")
            

        
    print("任务结束")

def toggle_task():
    global running_flag, worker_thread

    if not running_flag:
        option1 = var1.get()
        option2 = var2.get()
        debug_text = entry_var.get() if option2 else ""
        if option2 and not debug_text:
            messagebox.showwarning("参数缺失", "您已启用调试模式，请输入调试参数！")
            return  # 中止运行

        running_flag = True
        button.config(text="停止运行")
        worker_thread = threading.Thread(target=background_task, args=(option1, option2, debug_text), daemon=True)
        worker_thread.start()
    else:
        running_flag = False
        button.config(text="运行")

# 当选项2被勾选时显示输入框，否则隐藏
def on_option2_toggle():
    if var2.get():
        entry_label.pack(anchor='w', padx=40)
        entry.pack(anchor='w', padx=40, pady=5)
    else:
        entry_label.pack_forget()
        entry.pack_forget()

# 创建主窗口
window = tk.Tk()
window.title("虚拟麦克风")
window.geometry("400x370")

# 复选框1
var1 = tk.BooleanVar()
check1 = tk.Checkbutton(window, text="选项一：映射实际麦克风到虚拟麦克风", variable=var1)
check1.pack(anchor='w', pady=5, padx=20)

# 复选框2
var2 = tk.BooleanVar()
check2 = tk.Checkbutton(window, text="选项二：播放音频", variable=var2, command=on_option2_toggle)
check2.pack(anchor='w', pady=5, padx=20)

# 输入框（初始隐藏）
entry_var = tk.StringVar()
entry_label = tk.Label(window, text="请输入要播放音频的路径：")
entry = tk.Entry(window, textvariable=entry_var, width=30)

# 运行按钮
button = tk.Button(window, text="运行", command=toggle_task, width=20, height=2)
button.pack(pady=30)
button = tk.Button(window, text="录制/播放音频", command=bb, width=20, height=2)
button.pack(pady=30)
# 启动窗口
window.mainloop()
