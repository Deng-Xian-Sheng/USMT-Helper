# import winreg
import time
import shutil
import fake_winreg as winreg
import toml
import fnmatch

def log_str(log_data: tuple)->str:
    return f"源路径: {log_data[0]}\n目标路径: {log_data[1]}\n错误信息: {log_data[2]}\n\n"

def append_log_to_file(log_message, log_file_path):
    """
    封装一个向指定文件追加日志的函数。

    参数:
    log_message (str): 需要记录的日志信息。
    log_file_path (str): 日志文件的路径，包括文件名。

    返回:
    None

    示例：
    append_log_to_file('This is a sample log entry.', 'my_log.txt')
    """
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            print(log_message)
            log_file.write(log_message)
    except Exception as e:
        print(f"写日志错误：{e}")

# 读取TOML配置文件
with open('migrate_config.toml', 'r', encoding='utf-8') as f:
    migrate_config = toml.load(f)


for v in migrate_config['file']:
    if v['path_src'] == "":
        print("migrate_config.toml 配置文件错误, path_src 不能为空")
        exit(1)
    if v['path_dst'] == "":
        print("migrate_config.toml 配置文件错误, path_dst 不能为空")
        exit(1)
    for vv in v['no']:
        if vv == "":
            print("migrate_config.toml 配置文件错误, no 不能为空")
            exit(1)
    try:
        shutil.copytree(v['path_src'],v['path_dst'],symlinks=True,dirs_exist_ok=v['overlap'],ignore=shutil.ignore_patterns(*v['no']))
    except Exception as e:
        if isinstance(e.args,tuple):
            append_log_to_file(f"错误代码: {e.args[0]}\n错误信息: {e.args[1]}\n\n","log.txt")
        if isinstance(e.args[0], tuple):
            append_log_to_file(f"错误代码: {e.args[0]}\n错误信息: {e.args[1]}\n\n","log.txt")
        if isinstance(e.args[0], list):
            for v in e.args:
                for vv in v:
                    append_log_to_file(log_str(vv),"log.txt")

root_key_to_winreg_const = {
    "HKEY_CLASSES_ROOT":winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER":winreg.HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE":winreg.HKEY_LOCAL_MACHINE,
    "HKEY_USERS":winreg.HKEY_USERS,
    "HKEY_PERFORMANCE_DATA":winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG":winreg.HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA":winreg.HKEY_DYN_DATA,
}

def is_excluded(path, exclusions):
    return any(fnmatch.fnmatch(path.lower(), exc.lower()) for exc in exclusions)

# 如果不在Windows系统上，定义WindowsError
if not hasattr(__builtins__, 'WindowsError'):
    class WindowsError(OSError):
        pass

def parse_registry_path(path):
    parts = path.split('\\', 1)
    key_name = parts[0].upper()
    subkey = parts[1] if len(parts) > 1 else ""
    
    if key_name in root_key_to_winreg_const:
        return root_key_to_winreg_const[key_name], subkey
    else:
        raise ValueError(f"不支持的根键: {key_name}")

def copy_registry_key(src_key, dst_key, src_subkey, dst_parent, dst_name):
    dst_subkey = f"{dst_parent}\\{dst_name}" if dst_parent else dst_name
    try:
        src_handle = winreg.OpenKey(src_key, src_subkey, 0, winreg.KEY_READ)
        dst_handle = winreg.CreateKey(dst_key, dst_subkey)
        
        print(f"\n正在复制键: {src_subkey} -> {dst_subkey}")
        
        index = 0
        while True:
            try:
                name, data, type = winreg.EnumValue(src_handle, index)
                winreg.SetValueEx(dst_handle, name, 0, type, data)
                print(f"  复制值: {name} = {data}")
                index += 1
            except OSError:
                break
        
        winreg.CloseKey(src_handle)
        winreg.CloseKey(dst_handle)
        
        print(f"完成复制键: {src_subkey} -> {dst_subkey}")
    except OSError as e:
        print(f"复制 {src_subkey} 到 {dst_subkey} 时出错: {e}")

def copy_registry_path(src_key, dst_key, src_path, dst_path, exclusions):
    try:
        src_handle = winreg.OpenKey(src_key, src_path, 0, winreg.KEY_READ)
        dst_handle = winreg.CreateKey(dst_key, dst_path)
        
        print(f"\n正在复制路径: {src_path} -> {dst_path}")
        
        # 复制值
        index = 0
        while True:
            try:
                name, data, type = winreg.EnumValue(src_handle, index)
                full_path = f"{src_path}\\{name}"
                if not is_excluded(full_path, exclusions):
                    winreg.SetValueEx(dst_handle, name, 0, type, data)
                    print(f"  复制值: {name} = {data}")
                else:
                    print(f"  排除值: {name}")
                index += 1
            except OSError:
                break
        
        # 复制子键
        index = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(src_handle, index)
                full_path = f"{src_path}\\{subkey_name}"
                if not is_excluded(full_path, exclusions):
                    print(f"  进入子键: {subkey_name}")
                    copy_registry_path(src_key, dst_key, 
                                       full_path, 
                                       f"{dst_path}\\{subkey_name}", 
                                       exclusions)
                else:
                    print(f"  排除子键: {subkey_name}")
                index += 1
            except OSError:
                break
        
        winreg.CloseKey(src_handle)
        winreg.CloseKey(dst_handle)
        
        print(f"完成复制路径: {src_path} -> {dst_path}")
    except OSError as e:
        print(f"复制路径 {src_path} 到 {dst_path} 时出错: {e}")

def copy_registry(src, dst, exclusions):
    src_key, src_path = parse_registry_path(src)
    dst_key, dst_path = parse_registry_path(dst)
    
    print(f"开始复制注册表:")
    print(f"源: {src}")
    print(f"目标: {dst}")
    print(f"排除项: {exclusions}\n")
    
    if '\\' not in src_path.strip('\\') and '\\' not in dst_path.strip('\\'):
        # 单个键到单个键的复制
        copy_registry_key(src_key, dst_key, src_path, "", dst_path)
    elif '\\' not in src_path.strip('\\'):
        # 单个键到路径的复制
        dst_parent, dst_name = dst_path.rsplit('\\', 1)
        copy_registry_key(src_key, dst_key, src_path, dst_parent, dst_name)
    else:
        # 路径到路径的复制
        copy_registry_path(src_key, dst_key, src_path, dst_path, exclusions)
    
    print("\n注册表复制完成")

# 使用示例
src = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion"
dst = r"HKEY_CURRENT_USER\Software\MyApp\WindowsSettings"
exclusions = [
    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
    "*.tmp"
]

copy_registry(src, dst, exclusions)