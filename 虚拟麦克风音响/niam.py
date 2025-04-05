import sounddevice as sd
import soundfile as sf

# 加载你要播放的音频文件（WAV 格式最佳）
data, fs = sf.read("peng.mp3")

# 找出设备编号
devices = sd.query_devices()
for i, device in enumerate(devices):
    if "CABLE Input" in device["name"]:
        print(f"找到虚拟音频设备: {device['name']} 设备编号: {i}")
        virtual_device = i
        break

# 播放到虚拟麦克风
sd.play(data, fs, device=virtual_device)
sd.wait()
