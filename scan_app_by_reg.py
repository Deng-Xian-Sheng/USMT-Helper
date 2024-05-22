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