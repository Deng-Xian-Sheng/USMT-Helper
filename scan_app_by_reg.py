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
winreg.LoadKey()
# 不在区分这个东西是谁的，而是判断这个东西能不能迁移，把不能迁移的挑出来。
# usmt必须要储存文件才能迁移吗？有硬连接迁移的办法，但是适用性低。
# 让gpt列举注册表项，并说明子级结构
