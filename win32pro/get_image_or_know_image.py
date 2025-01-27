import cv2
import numpy as np
import pyautogui
import time

def wherestr_x_y(template_path, threshold=0.8):
    # 读取模板图片
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    # 获取屏幕截图
    screen = pyautogui.screenshot()
    # 将PIL图像转换为OpenCV格式
    screen_np = np.array(screen)
    frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用模板匹配
    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # 收集匹配位置
    locations = []
    for pt in zip(*loc[::-1]):
        locations.append((pt[0], pt[1]))

    return locations
import pyautogui

def right(x=None, y=None):
    """
    模拟鼠标右键点击。

    :param x: 鼠标点击的X坐标（默认为当前位置）。
    :param y: 鼠标点击的Y坐标（默认为当前位置）。
    """
    if x is not None and y is not None:
        pyautogui.rightClick(x, y)
    else:
        pyautogui.rightClick()

# 使用函数前需要确保你的鼠标光标位于你想要点击的位置，
# 或者提供具体的x和y坐标。
import pyautogui

def goto(x, y):
    """
    将鼠标移动到屏幕上的指定位置。

    :param x: 目标位置的X坐标。
    :param y: 目标位置的Y坐标。
    """
    pyautogui.moveTo(x, y)

# 调用函数并传入坐标值，例如将鼠标移动到屏幕的中心位置。
cv = pyautogui.size()  # 获取屏幕尺寸
import pyautogui

def left(x=None, y=None):
    """
    模拟鼠标左键点击。

    :param x: 鼠标点击的X坐标（默认为当前位置）。
    :param y: 鼠标点击的Y坐标（默认为当前位置）。
    """
    if x is not None and y is not None:
        pyautogui.click(x, y)
 
    else:
        pyautogui.click()

# 使用函数前需要确保你的鼠标光标位于你想要点击的位置，
# 或者提供具体的x和y坐标。
def screenshot_region(left, top, width, height,name):
    left=int(left)
    top=int(top)
    width=width-left
    height=height-top
   # print(left,top,width,height)
    """
    Takes a screenshot of a specific region on the screen.
    
    Parameters:
    left (int): The x-coordinate of the top-left corner of the region.
    top (int): The y-coordinate of the top-left corner of the region.
    width (int): The width of the region.
    height (int): The height of the region.
    
    Returns:
    PIL.Image: A PIL Image object containing the screenshot.
    """
    a=pyautogui.screenshot(region=(left, top, width, height))
    a.save(name)
def kuaijiejian(a:object):
    b=''
    for i in a:
        if i !=a[-1]:
            b+="'"+str(i)+"'"+','
        else:
            b+="'"+str(i)+"'"
    exec(f'import pyautogui\npyautogui.hotkey({b})')

   # else:
    #    print("指定的窗口在超时时间内未出现，无法获取坐标。")
     #   1/0
if __name__ == '__main__':
    # 调用函数并传入坐标值，例如将鼠标移动到屏幕的中心位置。
    #cv = pyautogui.size()  # 获取屏幕尺寸
    #print(cv)
    #screenshot_region(1211,149,1920,1080)
   # screenshot_region(1488,796,1588,816,'10.jpg')
  #  kuaijiejian(['ctrl','c'])
   pass