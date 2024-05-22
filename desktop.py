import os
from win32com.client import Dispatch

def list_shortcuts_and_exe_files(desktop_path):
    shortcut_files = []
    exe_files = []

    for item in os.listdir(desktop_path):
        item_path = os.path.join(desktop_path, item)
        if os.path.isfile(item_path):
            if item_path.endswith('.lnk'):
                shortcut_files.append(item_path)
            elif item_path.endswith('.exe'):
                exe_files.append(item_path)

    return shortcut_files, exe_files

def parse_shortcut(shortcut_path):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    return shortcut.Targetpath

def get_last_folder_name(path):
    folder_path = os.path.dirname(path)
    last_folder_name = os.path.basename(folder_path)
    return last_folder_name, folder_path

def main():
    desktop_path = r'D:\wim\Windows.old\Users\x1761\Desktop'
    shortcut_files, exe_files = list_shortcuts_and_exe_files(desktop_path)

    print("Parsed Shortcuts:")
    for shortcut in shortcut_files:
        target_path = parse_shortcut(shortcut)
        last_folder_name, folder_path = get_last_folder_name(target_path)
        print(f"Shortcut: {shortcut}")
        print(f"Target Path: {target_path}")
        print(f"Last Folder Name: {last_folder_name}")
        print(f"Folder Path: {folder_path}")
        print()

    print("EXE Files:")
    for exe_file in exe_files:
        print(f"EXE File: {exe_file}")

if __name__ == '__main__':
    main()
