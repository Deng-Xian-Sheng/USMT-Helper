# 让用户输入被迁移用户在Users/xxx的用户名
# 处理在USMT中使用NTUSER.DAT的问题,让reg.xml中的路径正确
# 根据用户名替换file.xml的路径
# 生成file1.xml，里面指定迁移Program Files和Program Files (x86)
# 指定排除
"""
32位
Windows NT
Internet Explorer
Microsoft.NET
Windows Defender
Windows Mail
Windows Media Player
Windows Photo Viewer
Windows Portable Devices
Windows Security
Windows Sidebar
WindowsPowerShell

64位
Windows NT
Internet Explorer
Microsoft.NET
Windows Defender
Windows Mail
Windows Media Player
Windows Photo Viewer
Windows Portable Devices
Windows Security
Windows Sidebar
WindowsPowerShell
WindowsApps
"""
# 扫描Program Files/Common Files和Program Files (x86)/Common Files，将里面的内容输出到txt，由用户决定保留哪些。
# 然后取反，将需要排除的添加到file1.xml