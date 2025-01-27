import ctypes
import sys
from ctypes import wintypes

# 定义一些必要的Windows API中的结构体和常量等

# 用于TOKEN_PRIVILEGES结构体，指定权限属性
SE_PRIVILEGE_ENABLED = 0x00000002

class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", wintypes.DWORD),
        ("HighPart", wintypes.LONG)
    ]

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", wintypes.DWORD)
    ]

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1)
    ]

# 加载advapi32.dll库，用于后续调用相关权限操作的函数
advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)

# 获取当前进程的令牌句柄
OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
OpenProcessToken.restype = wintypes.BOOL

GetCurrentProcess = ctypes.WinDLL('kernel32', use_last_error=True).GetCurrentProcess
GetCurrentProcess.restype = wintypes.HANDLE

token_handle = wintypes.HANDLE()
if not OpenProcessToken(GetCurrentProcess(), 0x000F, ctypes.byref(token_handle)):
    print(f"获取进程令牌失败，错误码: {ctypes.get_last_error()}")
    sys.exit(1)

# 查找要调整的权限对应的LUID（以SeDebugPrivilege为例，它是一种高权限，这里去除它来模拟降权）
LookupPrivilegeValueW = advapi32.LookupPrivilegeValueW
LookupPrivilegeValueW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, ctypes.POINTER(LUID)]
LookupPrivilegeValueW.restype = wintypes.BOOL

luid = LUID()
if not LookupPrivilegeValueW(None, "SeDebugPrivilege", ctypes.byref(luid)):
    print(f"查找权限LUID失败，错误码: {ctypes.get_last_error()}")
    sys.exit(1)

# 构建TOKEN_PRIVILEGES结构体，设置要修改的权限属性为禁用（去除权限）
token_privileges = TOKEN_PRIVILEGES()
token_privileges.PrivilegeCount = 1
token_privileges.Privileges[0].Luid = luid
token_privileges.Privileges[0].Attributes = 0  # 设置为0表示禁用该权限

# 调整进程令牌的权限
AdjustTokenPrivileges = advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.argtypes = [wintypes.HANDLE, wintypes.BOOL, ctypes.POINTER(TOKEN_PRIVILEGES),
                                  wintypes.DWORD, ctypes.POINTER(TOKEN_PRIVILEGES), ctypes.POINTER(wintypes.DWORD)]
AdjustTokenPrivileges.restype = wintypes.BOOL

if not AdjustTokenPrivileges(token_handle, False, ctypes.byref(token_privileges), 0, None, None):
    print(f"调整令牌权限失败，错误码: {ctypes.get_last_error()}")
    sys.exit(1)

# 关闭进程令牌句柄
CloseHandle = ctypes.WinDLL('kernel32', use_last_error=True).CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

if not CloseHandle(token_handle):
    print(f"关闭令牌句柄失败，错误码: {ctypes.get_last_error()}")
    sys.exit(1)

# 以下是模拟降权后执行的操作，这里以访问普通用户有权限访问的文件路径为例
try:
    with open("C:\\Users\\<当前用户名>\\test.txt", "w") as file:
        file.write("这是降权后以普通用户权限操作写入的内容。\n")
    print("成功以普通用户权限进行文件写入操作。")
except PermissionError:
    print("权限不足，可能降权操作未生效或者文件权限设置有问题。")
except FileNotFoundError:
    print("文件路径不存在，请检查。")
except Exception as e:
    print(f"出现其他异常: {e}")