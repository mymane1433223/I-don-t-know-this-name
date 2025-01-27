import sys
def get_behandtext(num:int):
    '''获得后缀参数 1为第一个参数'''
    return sys.argv[num]
def get_all_text():
    '''获得所有参数'''
    return sys.argv[1:]
import os
def clear_screen():
    """
    清除屏幕上的所有内容。
    根据操作系统选择正确的命令。
    """
    if os.name == 'posix':  # Unix/Linux/Mac等
        os.system('clear')
    elif os.name == 'nt':   # Windows
        os.system('cls')
def print_clocr(rgb,text):
    def rgb_to_ansi_escape(r, g, b):
        """
    将RGB颜色值转换为ANSI转义序列，用于设置前景色（文本颜色）
    :param r: 红色分量，取值范围0 - 255
    :param g: 绿色分量，取值范围0 - 255
    :param b: 蓝色分量，取值范围0 - 255
    :return: 对应的ANSI转义序列字符串
        """
        return f"\033[38;2;{r};{g};{b}m"
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    color_escape = rgb_to_ansi_escape(r, g, b)
    return (color_escape + text + "\033[0m")
import pyperclip

def write_to_clipboard(content):
    """
    将指定内容写入剪贴板的函数
    :param content: 要写入剪贴板的内容，字符串类型
    """
    pyperclip.copy(content)
import difflib


def difflib_similarity(s1, s2):
    """
    使用difflib库计算两个字符串的相似度

    参数：
    s1 (str)：第一个字符串
    s2 (str)：第二个字符串

    返回：
    float：相似度，取值范围在0到1之间，越接近1表示越相似
    """
    similarity = difflib.SequenceMatcher(None, s1, s2).ratio()
    return similarity
import ctypes
from ctypes import wintypes

import win32clipboard


def copy_files(file_paths: list):
    # 定义所需的 Windows 结构和函数
    CF_HDROP = 15

    class DROPFILES(ctypes.Structure):
        _fields_ = [("pFiles", wintypes.DWORD),
                    ("pt", wintypes.POINT),
                    ("fNC", wintypes.BOOL),
                    ("fWide", wintypes.BOOL)]

    offset = ctypes.sizeof(DROPFILES)
    length = sum(len(p) + 1 for p in file_paths) + 1
    size = offset + length * ctypes.sizeof(wintypes.WCHAR)
    buf = (ctypes.c_char * size)()
    df = DROPFILES.from_buffer(buf)
    df.pFiles, df.fWide = offset, True
    for path in file_paths:
        path = path.replace('/', '\\')
        array_t = ctypes.c_wchar * (len(path) + 1)
        path_buf = array_t.from_buffer(buf, offset)
        path_buf.value = path
        offset += ctypes.sizeof(path_buf)
    buf[offset:offset + ctypes.sizeof(wintypes.WCHAR)] = b'\0\0'

    # 将数据放入剪切板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(CF_HDROP, buf)
    win32clipboard.CloseClipboard()

import pyperclip


def read_clipboard_cross_platform():
    """
    跨平台读取剪贴板中的内容

    返回:
    str: 剪贴板中的文本内容，如果剪贴板中无文本内容则返回空字符串
    """
    try:
        return pyperclip.paste()
    except:
        return ""
import os

def get_file_name(file_path):
    """
    获取文件的名称（不包含路径）

    参数:
    file_path (str): 文件的路径

    返回:
    str: 文件的名称
    """
    filename = os.path.basename(file_path)
    return filename
if __name__ == '__main__':
    copy_files([r'D:\python\python\爬虫\抖音爬视频\bs4pro.py'])