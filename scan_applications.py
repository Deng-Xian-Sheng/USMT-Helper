import os
import subprocess
import winreg
from xml.etree.ElementTree import Element, SubElement, tostring
from language import translator

def get_installed_apps(registry_path, hive=winreg.HKEY_LOCAL_MACHINE):
    apps = []
    try:
        with winreg.OpenKey(hive, registry_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                sub_key_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, sub_key_name) as sub_key:
                    try:
                        name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
                        apps.append((name, version))
                    except FileNotFoundError:
                        pass
    except Exception as e:
        print(f"Error accessing registry path {registry_path}: {e}")
    return apps

def scan_file_system_for_apps(drive):
    program_files = os.path.join(drive, "Program Files")
    program_files_x86 = os.path.join(drive, "Program Files (x86)")
    apps = []

    for folder in [program_files, program_files_x86]:
        if os.path.exists(folder):
            for app in os.listdir(folder):
                app_path = os.path.join(folder, app)
                if os.path.isdir(app_path):
                    apps.append(f"Directory: {app}")
    return apps

def scan_installed_apps(offline_drive):
    apps = []
    apps.extend(get_installed_apps(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"))
    apps.extend(get_installed_apps(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", hive=winreg.HKEY_CURRENT_USER))
    apps.extend(scan_file_system_for_apps(offline_drive))
    return apps

def save_apps_to_txt(apps, filename="installed_apps.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        for app in apps:
            file.write(app + "\n")
    print(translator.translate("已保存应用程序列表到") + " " + filename)

def prompt_user_to_edit_txt(filename="installed_apps.txt"):
    print(translator.translate("请编辑文件") + f" {filename}，" + translator.translate("保留需要迁移的应用程序，然后按回车继续..."))
    if os.name == 'nt':
        subprocess.call(['notepad', filename])
    else:
        print(translator.translate("请手动打开并编辑文件") + f" {filename}")
    input(translator.translate("编辑完成后按回车继续..."))

def load_selected_apps(filename="installed_apps.txt"):
    with open(filename, 'r', encoding='utf-8') as file:
        selected_apps = [line.strip() for line in file if line.strip()]
    return selected_apps

def check_apps_on_current_system(apps):
    current_installed_apps = scan_installed_apps("")
    found_apps = []
    for app in apps:
        for current_app in current_installed_apps:
            if app in current_app:
                found_apps.append(current_app)
                break
    return found_apps

def save_found_apps_to_txt(apps, filename="found_apps.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        for app in apps:
            file.write(app + "\n")
    print(translator.translate("已保存存在的应用程序列表到") + " " + filename)

def search_app_installation_path(app_name):
    possible_paths = []
    for drive in ['C:\\', 'D:\\', 'E:\\']:
        program_files = os.path.join(drive, "Program Files")
        program_files_x86 = os.path.join(drive, "Program Files (x86)")
        for folder in [program_files, program_files_x86]:
            if os.path.exists(folder):
                for app in os.listdir(folder):
                    if app_name.lower() in app.lower():
                        possible_paths.append(os.path.join(folder, app))
    return possible_paths

def search_user_data(app_name):
    user_data = []
    user_profile = os.environ['USERPROFILE']
    for folder in ['Documents', 'AppData\\Local', 'AppData\\Roaming']:
        path = os.path.join(user_profile, folder)
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    if app_name.lower() in dir.lower():
                        user_data.append(os.path.join(root, dir))
                for file in files:
                    if app_name.lower() in file.lower():
                        user_data.append(os.path.join(root, file))
    return user_data

def search_registry_entries(app_name):
    registry_entries = []
    hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
    paths = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
             r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]
    for hive in hives:
        for path in paths:
            try:
                with winreg.OpenKey(hive, path) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name) as sub_key:
                            try:
                                name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                                if app_name.lower() in name.lower():
                                    registry_entries.append(f"{path}\\{sub_key_name}")
                            except FileNotFoundError:
                                pass
            except Exception as e:
                print(f"Error accessing registry path {path} in hive {hive}: {e}")
    return registry_entries

def generate_usmt_custom_xml(app_name, installation_paths, user_data_paths, registry_entries):
    root = Element('migration')
    application = SubElement(root, 'application', name=app_name)
    
    installation = SubElement(application, 'installation')
    for path in installation_paths:
        path_element = SubElement(installation, 'path')
        path_element.text = path

    user_data = SubElement(application, 'userData')
    for path in user_data_paths:
        path_element = SubElement(user_data, 'path')
        path_element.text = path

    registry = SubElement(application, 'registry')
    for entry in registry_entries:
        entry_element = SubElement(registry, 'entry')
        entry_element.text = entry

    tree_str = tostring(root, 'utf-8').decode('utf-8')
    filename = f"{app_name}_usmt.xml"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(tree_str)
    print(translator.translate(f"{app_name}的USMT自定义XML文件已生成：{filename}"))

if __name__ == "__main__":
    offline_drive = input(translator.translate("请输入脱机系统的驱动器路径（例如D:\\）："))
    installed_apps = scan_installed_apps(offline_drive)
    save_apps_to_txt(installed_apps)
    prompt_user_to_edit_txt()
    selected_apps = load_selected_apps()
    print(translator.translate("用户选择的应用程序："))
    for app in selected_apps:
        print(app)

    found_apps = check_apps_on_current_system(selected_apps)
    save_found_apps_to_txt(found_apps)
    print(translator.translate("存在的应用程序："))
    for app in found_apps:
        print(app)

    for app in found_apps:
        print(translator.translate(f"搜索应用程序的安装路径、用户数据、注册表项：{app}"))
        installation_paths = search_app_installation_path(app)
        user_data_paths = search_user_data(app)
        registry_entries = search_registry_entries(app)

        with open(f"{app}_details.txt", 'w', encoding='utf-8') as file:
            file.write(translator.translate("安装路径：") + "\n")
            for path in installation_paths:
                file.write(path + "\n")
            file.write(translator.translate("用户数据路径：") + "\n")
            for path in user_data_paths:
                file.write(path + "\n")
            file.write(translator.translate("注册表项：") + "\n")
            for entry in registry_entries:
                file.write(entry + "\n")
        
        print(translator.translate(f"{app}的详细信息已保存到{app}_details.txt"))
        generate_usmt_custom_xml(app, installation_paths, user_data_paths, registry_entries)
