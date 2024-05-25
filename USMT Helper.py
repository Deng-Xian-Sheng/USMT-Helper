# 让用户输入被迁移用户在Users/xxx的用户名
# 让用户输入脱机系统的盘符
# 根据用户名查找sid
# 根据sid替换reg.xml中的路径
# 根据用户名替换file.xml的路径
# 生成file1.xml，里面指定迁移Program Files和Program Files (x86)
"""
指定排除
Internet Explorer：Internet Explorer 浏览器的安装目录。
Windows Defender：Windows 防病毒软件的文件。
Windows Mail：Windows 自带邮件客户端的文件。
Windows Media Player：Windows 媒体播放器的文件。
Windows NT：包含 Windows NT 相关文件。
Windows Photo Viewer：Windows 照片查看器的文件。

Internet Explorer：32 位版本的 Internet Explorer 浏览器。
Microsoft.NET：.NET Framework 的安装目录，用于运行基于 .NET 的应用程序。
Windows Defender：32 位版本的 Windows 防病毒软件文件。
Windows Mail：32 位版本的 Windows 自带邮件客户端文件。
Windows Media Player：32 位版本的 Windows 媒体播放器文件。
Windows NT：包含与 Windows NT 相关的 32 位文件。
Windows Photo Viewer：32 位版本的 Windows 照片查看器文件。

C:\Program Files
- Common Files
- Internet Explorer
- Microsoft.NET
- Windows Defender
- Windows Mail
- Windows Media Player
- Windows Photo Viewer
- Windows Portable Devices
- Windows Security
- Windows Sidebar
- WindowsApps
- WindowsPowerShell

C:\Program Files (x86)
- Common Files
- Internet Explorer
- Microsoft.NET
- Windows Defender
- Windows Mail
- Windows Media Player
- Windows Photo Viewer
- Windows Portable Devices
- Windows Security
- Windows Sidebar
- WindowsPowerShell


Program Files:
- Windows Defender
- Internet Explorer
- Common Files (包含多个系统组件如System32等)
- WindowsApps (存放Windows Store应用)
- Windows Media Player
- Microsoft.NET

Program Files (x86):
- Internet Explorer
- Microsoft.NET (用于32位应用)
- Common Files (同样包含多个系统组件，但针对32位)
- Windows Mail
- Windows NT (包含一些向后兼容的组件)

"""
# 扫描Program Files/Common Files和Program Files (x86)/Common Files，将里面的内容输出到txt，由用户决定保留哪些。
# 然后取反，将需要排除的添加到file1.xml