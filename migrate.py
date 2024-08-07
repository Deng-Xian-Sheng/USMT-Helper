import shutil
import winreg
import toml

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
        if isinstance(e.args[0], tuple):
            append_log_to_file(f"错误代码: {e.args[0]}\n错误信息: {e.args[1]}\n\n","log.txt")
        else:
            if isinstance(e.args[0], list):
                for v in e.args:
                    for vv in v:
                        append_log_to_file(log_str(vv),"log.txt")
        else:
            if isinstance(e.args[0], list):
                for v in e.args:
                    for vv in v:
                        append_log_to_file(log_str(vv),"log.txt")


def get_hkey(path):
    hkey_mapping = {
        'HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
        'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
        'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        'HKEY_USERS': winreg.HKEY_USERS,
        'HKEY_PERFORMANCE_DATA': winreg.HKEY_PERFORMANCE_DATA,
        'HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG
    }
    
    for hkey_name, hkey_value in hkey_mapping.items():
        if path.startswith(hkey_name):
            return hkey_value
    
    raise ValueError(f"无效的注册表路径: {path}")

# 读取配置文件
for v in migrate_config['reg']:
    # 这里是每一个源路径和目标路径
    winreg.OpenKey(get_hkey(v['path_key_src'])winreg.KEY_READ)    

    pass