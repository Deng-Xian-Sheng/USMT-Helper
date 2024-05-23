import subprocess
import winreg

# 用户特定的设置应写入 HKCU\Software
# 特定于计算机的设置应写入 HKLM\Software

# path里或许也有应用程序
# HKEY_USERS
# HKEY_CURRENT_USER\Software
# HKEY_LOCAL_MACHINE\SOFTWARE\\Microsoft\Windows\CurrentVersion\Uninstall
# HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall
# [software vendor name]\[application name]HKLM\Software\Microsoft\Internet Explorer
# HKEY_CURRENT_USER\Software\Microsoft\Installer\Products 
# HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Persisted

def load_registry_hive(hive_path, key_name):
    try:
        subprocess.run(['reg', 'load', key_name, hive_path], check=True)
        print(f'Registry hive loaded to {key_name}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to load registry hive: {e}')

def unload_registry_hive(key_name):
    try:
        subprocess.run(['reg', 'unload', key_name], check=True)
        print(f'Registry hive unloaded from {key_name}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to unload registry hive: {e}')

# 加载注册表
load_registry_hive()

try:
    # 读取加载的注册表
    pass
finally:
    # 卸载注册表
    unload_registry_hive()


# 不在区分这个东西是谁的，而是判断这个东西能不能迁移，把不能迁移的挑出来。

"""
看来我的搜索工具出了点问题，我无法直接从网上为你获取信息。不过，我可以根据以往的知识来回答你的问题。

在Windows中，第三方应用程序通常会在以下几个注册表键中插入条目：

1. **HKEY_CURRENT_USER\Software** 和 **HKEY_LOCAL_MACHINE\Software**：
   这两个位置是最常见的，用于存储应用程序特定的设置。应用程序通常会在这些键下创建一个以自己名称为名的子键。

2. **HKEY_USERS**：
   用于存储所有用户的设置，较少用于第三方应用程序。

3. **HKEY_CLASSES_ROOT**：
   用于关联文件类型和程序。应用程序可能会在这里注册自己能打开的文件类型。

子键的结构通常是按照应用程序的名称来创建的，例如：

- HKEY_LOCAL_MACHINE\Software\[应用程序名称]
- HKEY_CURRENT_USER\Software\[应用程序名称]

这些键下的具体结构取决于应用程序的需求和设计，可能包括各种配置设置、文件路径等。

如果你需要更详细的信息，我建议你可以使用注册表编辑器（Regedit）来查看特定应用程序所使用的注册表键。如果你有特定应用程序的名称，我也可以尝试帮你查找更具体的信息。
"""


"""
在Windows中，第三方应用程序通常会在以下几个注册表键中插入项目。这些键的结构及路径如下：

1. **HKEY_LOCAL_MACHINE (HKLM)**
   - **HKLM\Software**: 用于存储应用程序的全局设置，所有用户共享。
     - 应用程序通常会在 **HKLM\Software\<公司名称>\<应用程序名称>** 下创建子键和设置。
   - **HKLM\Software\Classes**: 用于注册文件类型关联和COM类。
   - **HKLM\System\CurrentControlSet\Services**: 用于服务相关设置。
   
2. **HKEY_CURRENT_USER (HKCU)**
   - **HKCU\Software**: 存储当前用户的应用程序设置。
     - 应用程序通常会在 **HKCU\Software\<公司名称>\<应用程序名称>** 下创建子键和设置。

3. **HKEY_CLASSES_ROOT (HKCR)**
   - **HKCR** 是 **HKLM\Software\Classes** 和 **HKCU\Software\Classes** 的合并视图。
   - 应用程序通常会在 **HKCR\<文件扩展名>** 下注册文件类型关联。

4. **HKEY_USERS (HKU)**
   - **HKU\<SID>\Software**: 用于特定用户的设置，\<SID> 是用户的安全标识符。
     - 应用程序通常会在 **HKU\<SID>\Software\<公司名称>\<应用程序名称>** 下创建子键和设置。

5. **HKEY_CURRENT_CONFIG (HKCC)**
   - **HKCC\System\CurrentControlSet\Hardware Profiles\Current**: 存储当前硬件配置文件的设置。

以下是几个具体示例：

- **HKLM\Software\Microsoft\Windows\CurrentVersion\Run**: 存储开机自动启动的程序。
- **HKCU\Software\Microsoft\Windows\CurrentVersion\Run**: 存储当前用户的开机自动启动程序。

这些路径和结构可以根据应用程序的需要进行扩展和定制。第三方应用程序通常会根据标准路径创建和管理注册表键，以便在系统中正确配置和运行。

如果你需要更详细的信息或有特定的注册表键查询，请告诉我，我可以进行更具体的搜索或提供进一步的帮助。
"""