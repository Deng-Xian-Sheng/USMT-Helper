import subprocess
import time

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

# 加载注册表，重复加载没问题
load_reg(r"HKLM\SAM2",r"D:\wim\Windows.old\WINDOWS\System32\config\SAM")

try:
    # 读取加载的注册表
    pass
finally:
    # 卸载注册表
    pass
    # unload_reg(r"HKLM\SAM2")