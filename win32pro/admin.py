import ctypes
import sys


def is_admin():
    """
    检查当前脚本是否以管理员身份运行
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # 如果不是管理员权限，重新以管理员身份运行脚本
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)

# 以下是你原本想以管理员权限执行的代码逻辑，这里简单示例打印一句话
print("当前脚本正以管理员权限运行")