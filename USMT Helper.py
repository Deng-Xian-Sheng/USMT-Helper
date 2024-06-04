import os
import subprocess
def load_reg(key_name:str,file_path:str):
    try:
        subprocess.run(['reg', 'load', key_name, file_path], check=True)
    except Exception as e:
        print(e)

def unload_reg(key_name:str):
    try:
        subprocess.run(['reg', 'unload', key_name], check=True)
    except Exception as e:
        print(e)

# 必须在转移的目标系统上运行本程序
print("请在转移的目标系统上运行本程序")

# 让用户输入被迁移用户在Users/xxx的用户名
username = input("请输入被迁移用户在Users/xxx的用户名：")

# 让用户输入脱机系统根目录
os_root = input("请输入脱机系统根目录(例如:D:\\)：")

# 处理在USMT中使用NTUSER.DAT的问题,让reg.xml中的路径正确
# 首先先挂载NTUSER.DAT
hku_tmp_user = r"HKU\TempUser" + username
load_reg(hku_tmp_user,os.path.join(os_root,"Users",username,"NTUSER.DAT"))

# 替换 替换路径 为 hku_tmp_user

# 根据用户名替换file.xml的路径
# 生成file1.xml，里面指定迁移Program Files和Program Files (x86)
# 指定排除
"""
32位
Windows NT
Internet Explorer
Microsoft.NET
Windows Defender
Windows Mail
Windows Media Player
Windows Photo Viewer
Windows Portable Devices
Windows Security
Windows Sidebar
WindowsPowerShell

64位
Windows NT
Internet Explorer
Microsoft.NET
Windows Defender
Windows Mail
Windows Media Player
Windows Photo Viewer
Windows Portable Devices
Windows Security
Windows Sidebar
WindowsPowerShell
WindowsApps
"""
# 扫描Program Files/Common Files和Program Files (x86)/Common Files，将里面的内容输出到txt，由用户决定保留哪些。
# 然后取反，将需要排除的添加到file1.xml