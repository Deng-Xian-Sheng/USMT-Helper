# 导入所需的库
from regipy.registry import RegistryHive
from regipy.exceptions import RegistryKeyNotFoundException
import os

# 定义要加载的注册表文件路径
offline_root = r"D:\wim\Windows.old"
SYSTEM_HIVE_PATH = os.path.join(offline_root, r"Windows\System32\Config\SYSTEM")
SAM_HIVE_PATH = os.path.join(offline_root, r"Windows\System32\Config\SAM")
SOFTWARE_HIVE_PATH = os.path.join(offline_root, r"Windows\System32\Config\SOFTWARE")

# 定义注册表键路径
UNINSTALL_PATHS = [
    r'Software\Microsoft\Windows\CurrentVersion\Uninstall',
    r'Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
]

def get_installed_programs(hive_path, uninstall_paths):
    try:
        registry_hive = RegistryHive(hive_path)
    except FileNotFoundError:
        print(f"Hive file not found: {hive_path}")
        return []

    installed_programs = []

    for path in uninstall_paths:
        try:
            uninstall_key = registry_hive.get_key(path)
            for subkey in uninstall_key.iter_subkeys():
                program = {"UniqueID": subkey.name}  # 使用子键名称作为唯一ID
                for value in subkey.iter_values():
                    if value.name in ['DisplayName', 'DisplayVersion']:
                        program[value.name] = value.value
                if program:
                    installed_programs.append(program)
        except RegistryKeyNotFoundException:
            print(f"Registry key not found: {path} in {hive_path}")
            continue

    return installed_programs

def debug_registry_hive(sam_hive_path):
    try:
        sam_hive = RegistryHive(sam_hive_path)
        print(f"Successfully opened SAM hive: {sam_hive_path}")
        root_key = sam_hive.root
        print(f"Root key: {root_key.name}")
        for subkey in root_key.iter_subkeys():
            print(f"Subkey: {subkey.name}")
            if subkey.name == 'Domains':
                for domain_subkey in subkey.iter_subkeys():
                    print(f"  Domain subkey: {domain_subkey.name}")
                    if domain_subkey.name == 'Account':
                        for account_subkey in domain_subkey.iter_subkeys():
                            print(f"    Account subkey: {account_subkey.name}")
    except Exception as e:
        print(f"Error accessing SAM hive for debugging: {e}")

def get_user_sids(sam_hive_path):
    try:
        sam_hive = RegistryHive(sam_hive_path)
        users_key = sam_hive.get_key(r'SAM\Domains\Account\Users')
        print(f"Found Users key in SAM hive: {users_key.name}")
        sids = [subkey.name for subkey in users_key.iter_subkeys() if subkey.name != 'Names']
        return sids
    except FileNotFoundError:
        print(f"SAM hive file not found: {sam_hive_path}")
        return []
    except RegistryKeyNotFoundException:
        print(f"Registry key 'SAM\\Domains\\Account\\Users' not found in SAM hive")
        return []
    except Exception as e:
        print(f"Unexpected error accessing SAM hive: {e}")
        return []

def main():
    # 调试 SAM hive 文件结构
    debug_registry_hive(SAM_HIVE_PATH)

    installed_programs = []

    # 获取HKEY_LOCAL_MACHINE下的软件信息
    installed_programs.extend(get_installed_programs(SOFTWARE_HIVE_PATH, UNINSTALL_PATHS))

    # 获取所有用户的SID
    user_sids = get_user_sids(SAM_HIVE_PATH)
    user_hives_root = os.path.join(offline_root, r"Users")

    # 获取每个用户HKEY_CURRENT_USER下的软件信息
    for sid in user_sids:
        user_hive_path = os.path.join(user_hives_root, sid, r"NTUSER.DAT")
        if os.path.exists(user_hive_path):
            installed_programs.extend(get_installed_programs(user_hive_path, UNINSTALL_PATHS))
        else:
            print(f"NTUSER.DAT not found for user SID: {sid}")

    # 输出结果
    for program in installed_programs:
        print(f"ID: {program.get('UniqueID', 'N/A')}, Name: {program.get('DisplayName', 'N/A')}, Version: {program.get('DisplayVersion', 'N/A')}")

if __name__ == '__main__':
    main()
