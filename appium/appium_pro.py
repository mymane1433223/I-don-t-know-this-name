import uiautomator2 as u2
import os
d=''
def get_device_info():
    """获取手机详细信息
    Returns:
        dict: 包含手机品牌、型号等信息的字典
    """
    global d
    try:
        # 获取设备基本信息
        info = d.device_info
        
        # 使用shell命令获取更多信息
        brand = d.shell('getprop ro.product.brand').output.strip()
        model = d.shell('getprop ro.product.model').output.strip()
        manufacturer = d.shell('getprop ro.product.manufacturer').output.strip()
        android_version = d.shell('getprop ro.build.version.release').output.strip()
        
        device_info = {
            'brand': brand,              # 品牌
            'model': model,              # 型号
            'manufacturer': manufacturer, # 制造商
            'android_version': android_version,  # 安卓版本
            'sdk_version': info.get('sdkInt'),  # SDK版本
            'serial': info.get('serial'),       # 序列号
            'display': info.get('display'),     # 显示信息
        }
        
        return device_info
        
    except Exception as e:
        print(f"获取设备信息失败: {str(e)}")
        return None

def is_xiaomi():
    """判断是否是小米手机
    Returns:
        bool: True表示是小米手机
    """
    try:
        info = get_device_info()
        if info:
            return 'xiaomi' in info['brand'].lower() or 'xiaomi' in info['manufacturer'].lower()
        return False
    except:
        return False
def is_screen_on():
    """检查手机屏幕是否处于点亮状态
    Returns:
        bool: True表示屏幕点亮，False表示屏幕关闭
    """
    global d
    try:
        # 方法1：使用info获取屏幕状态
        if d.info.get('screenOn'):
            return True
            
        # 方法2：解析dumpsys power输出
        result = d.shell('dumpsys power | grep "Display Power"').output
        return "state=ON" in result
        
    except Exception as e:
        print(f"检查屏幕状态失败: {str(e)}")
        return False

def init(name=''):
    global d
    if name=='':
        d=u2.connect()
    else:d=u2.connect(name)
    try:
       d.unlock()
 #   d.keyevent("KEYCODE_POWER") 
  #  d.shell('input keyevent 26')
    except:
        os.system('adb shell svc power stayon true')
    print(get_device_info())
    if is_xiaomi():
        d.shell('settings put secure enabled_accessibility_services com.android.uiautomator.bridge/androidx.test.uiautomator.UiAutomatorService')
    return d
def look(poss=''):
    global d
    try:
        d.unlock()
    except:
        os.system('adb shell svc power stayon true')
    gotoxy(201,1615,234,472,0.25)
    for i in poss:
        d(text=i).click()
def openapk(apkname):
    global d
    d(text=apkname).click()

def getapp():
    global d
    return d.app_list()

def clicktext(text):
    global d
    d(text=text).click()
def wherexpath(xpath):
    global d
    return d.xpath(xpath).all()
def clickxy(x,y):
    global d
    d.click(x,y)
def gotoxy(x1,y1,x2,y2,tim):
    global d
    d.swipe(x1,y1,x2,y2,duration=tim)
def retext(ret):
    global d
    return d.xpath(ret).get_text()
def text_exists(text):
    """检查指定文字是否存在于当前界面
    Args:
        text: 要查找的文字
    Returns:
        bool: 存在返回True，不存在返回False
    """
    global d
    return d.xpath(f'//*[@text="{text}"]').exists

# 也可以添加一个更灵活的xpath版本
def xpath_exists(xpath):
    """检查指定xpath的元素是否存在
    Args:
        xpath: xpath表达式
    Returns:
        bool: 存在返回True，不存在返回False
    """
    global d
    return d.xpath(xpath).exists
def input_text(xpath, text):
    """通过xpath定位元素并输入文字
    Args:
        xpath: 输入框的xpath表达式
        text: 要输入的文字内容
    """
    global d
    d.xpath(xpath).set_text(text)

def clickxpath(xpath):
    """通过xpath点击元素
    Args:
        xpath: xpath表达式字符串
    """
    global d
    d.xpath(xpath).click()
def get_text_by_index(xpath, index):
    """获取相同xpath的第index个元素的文本
    Args:
        xpath: xpath表达式
        index: 要获取的元素索引(从0开始)
    Returns:
        str: 元素的文本内容，如果元素不存在返回空字符串
    """
    global d
    elements = d.xpath(xpath).all()
    if len(elements) > index:
        return elements[index].text
    else:
        print(f"找不到第{index+1}个元素")
        return ""
def click_xpath_index(xpath, index):
    """点击相同xpath的第index个元素
    Args:
        xpath: xpath表达式
        index: 要点击的元素索引(从0开始)
    """
    global d
    elements = d.xpath(xpath).all()  # 获取所有匹配的元素
    if len(elements) > index:
        elements[index].click()
    else:
        print(f"找不到第{index+1}个元素")
def count_xpath(xpath):
    """计算指定xpath在当前屏幕中匹配的元素数量
    Args:
        xpath: xpath表达式
    Returns:
        int: 匹配的元素数量
    """
    global d
    elements = d.xpath(xpath).all()
    return len(elements)
def get_text_with_children(xpath):
    """获取元素及其子元素的所有文本
    Args:
        xpath: 父元素的xpath表达式
    Returns:
        str: 合并后的文本内容
    """
    global d
    # 获取所有子元素的文本
    texts = []
    elements = d.xpath(f"{xpath}/descendant::*[@text]").all()
    for element in elements:
        if element.text:
            texts.append(element.text)
    return " ".join(texts)  # 返回所有文本组合
def get_index_text_with_children(xpath, index=0):
    """获取指定xpath的第index个元素及其所有子元素的文本
    Args:
        xpath: xpath表达式
        index: 要获取的第几个元素(从0开始)
    Returns:
        str: 所有文本内容拼接的字符串
    """
    global d
    try:
        # 使用descendant获取所有子元素的文本
        elements = d.xpath(f"({xpath})[{index+1}]/descendant::*[@text]").all()
        
        # 收集所有非空文本
        texts = []
        for elem in elements:
            if elem.text and elem.text.strip():
                texts.append(elem.text.strip())
                
        # 用空格连接所有文本
        return " ".join(texts)
        
    except Exception as e:
        print(f"获取文本失败: {str(e)}")
        return ""
def get_xy_by_index( xpath, index):
    global d
    """获取指定xpath和索引的元素坐标
    Args:
        xpath: xpath表达式
        index: 要获取的第几个元素(从0开始)
    Returns:
        tuple: (left, top, right, bottom) 元素的四个边界坐标
        None: 如果元素不存在
    """
    try:
        elements = d.xpath(xpath).all()
        if len(elements) > index:
            return elements[index].bounds
        print(f"找不到第{index+1}个元素")
        return None
    except Exception as e:
        print(f"获取元素坐标失败: {str(e)}")
        return None

def shell(cmd:str):
    global d
    return d.shell(cmd)