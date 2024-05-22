import os
from regipy.registry import RegistryHive
from regipy.exceptions import NoRegistrySubkeysException

# 定义需要读取的注册表键路径
key_paths = [
    r"HKEY_CURRENT_USER\Software",
    r"HKEY_LOCAL_MACHINE\SOFTWARE",
    r"HKEY_USERS",
    r"HKEY_CLASSES_ROOT",
    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services"
]

# 定义应用程序名称和用户SID变量
app_name_placeholder = "[应用程序名称]"
user_sid_placeholder = "[用户SID]"

def read_registry_keys(hive_path, key_paths, app_name, user_sids):
    # 打开注册表配置单元
    hive = RegistryHive(hive_path)

    for key_path in key_paths:
        # 替换路径中的占位符
        if app_name_placeholder in key_path:
            key_path = key_path.replace(app_name_placeholder, app_name)
        
        if user_sid_placeholder in key_path:
            for user_sid in user_sids:
                user_key_path = key_path.replace(user_sid_placeholder, user_sid)
                read_key(hive, user_key_path)
        else:
            read_key(hive, key_path)

def read_key(hive, key_path):
    try:
        key = hive.get_key(key_path)
        print(f"Reading key: {key_path}")
        for subkey in key.iter_subkeys():
            print(f"Subkey: {subkey.name}")
            for value in subkey.iter_values():
                print(f"Value: {value.name} = {value.value}")

    except NoRegistrySubkeysException:
        print(f"No subkeys found in: {key_path}")
    except Exception as e:
        print(f"Error reading {key_path}: {e}")

if __name__ == "__main__":
    hive_path = "path_to_your_hive_file"  # 替换为你的注册表配置单元文件路径
    app_name = "YourAppName"  # 替换为你的应用程序名称
    user_sids = ["S-1-5-21-123456789-123456789-123456789-1001"]  # 替换为你的用户SID列表

    read_registry_keys(hive_path, key_paths, app_name, user_sids)
