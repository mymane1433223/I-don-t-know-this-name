import easygui
from tkinter import Tk, Label
from PIL import Image, ImageTk
import webview
def input_window(title='输入框', msg='请输入内容：', default=''):
    return easygui.enterbox(msg, title, default)
def msg_window(title='消息框', msg='这是一条消息。'):
    easygui.msgbox(msg, title)
def image_in_window(image_path):
    root=Tk()
    image = Image.open(image_path)

# 将图片转换为Tkinter可用的PhotoImage对象
    photo = ImageTk.PhotoImage(image)

# 创建一个Label组件用于显示图片
    label = Label(root, image=photo)
    label.pack()

# 启动窗口的主循环，让窗口保持显示状态
    root.mainloop()
def mp4_in_window(mp4_path,title='视频播放窗口'):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>视频播放示例</title>
</head>
<body>
    <video controls width="640" height="480" src="{mp4_path}">
        你的浏览器不支持HTML5视频播放。
    </video>
</body>
</html>
"""

# 创建窗口并加载包含视频的HTML页面
    window = webview.create_window(title, html=html_content)
    webview.start()
import win32gui

def bring_window_to_front(window_title):
    """
    将指定标题的窗口移到最前端（仅适用于Windows平台）
    :param window_title: 窗口的标题名称，字符串类型
    """
    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == window_title:
            win32gui.SetForegroundWindow(hwnd)

    win32gui.EnumWindows(enum_callback, None)
import uiautomation as auto
def get_window_xy(name:str):
# 通过窗口的标题或者类名等条件来查找窗口，这里以查找记事本窗口为例，你可以替换为你想找的窗口相关条件
    notepad_window = auto.WindowControl( Name=name)

# 等待窗口出现，如果超时时间内没出现会抛出异常，这里设置超时时间为10秒，可按需调整
   # if notepad_window.Exists():
    # 获取窗口的矩形区域信息，返回的是一个包含left（左边距，即横坐标）、top（上边距，即纵坐标）、right、bottom的元组
    window_rect = notepad_window.BoundingRectangle
    left_x = window_rect.left
    top_y = window_rect.top
    return [[left_x,top_y],[window_rect.right-left_x,window_rect.bottom-top_y]]
import win32gui


def get_window_top_left_coords(hwnd):
    """
    通过窗口句柄获取窗口左上角坐标（仅适用于Windows平台）

    参数:
    hwnd (int): 窗口的句柄

    返回:
    tuple: 包含窗口左上角x坐标和y坐标的元组，如果获取失败返回 (None, None)
    """
    try:
        rect = win32gui.GetWindowRect(hwnd)
        return rect[0], rect[1], rect[2], rect[3]
    except:
        return None, None
import win32gui
import win32api
import win32con


def get_text_from_hwnd(hwnd):
    """
    尝试从给定的窗口句柄获取文本内容（对于部分标准控件有效）

    参数:
    hwnd (int): 窗口或控件的句柄

    返回:
    str: 获取到的文本内容，如果获取失败返回空字符串
    """
    length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH) + 1
    buffer = win32gui.PyMakeBuffer(length)
    win32api.SendMessage(hwnd, win32con.WM_GETTEXT, length, buffer)
    # 将memoryview转换为字节类型数据，再进行解码操作
    text = bytes(buffer).decode('utf-8', 'replace')
    return text
if __name__ == '__main__':
    print(get_text_from_hwnd(67922))