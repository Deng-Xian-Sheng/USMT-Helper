from math import e
import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom

def load_reg(key_name:str,file_path:str):
    try:
        subprocess.run(['reg', 'load', key_name, file_path], check=True)
    except Exception as e:
        print(e)

def unload_reg(key_name:str):
    try:
        subprocess.run(['reg', 'unload', key_name], check=True)
    except Exception as e:
        print(e)

def replace_text_in_file(file_path, text_to_replace, replacement_text):
    """
    替换文件中的文本。

    参数:
    file_path (str): 文件路径。
    text_to_replace (str): 要替换的文本。
    replacement_text (str): 替换后的文本。
    """
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        # 替换文本
        new_file_contents = file_contents.replace(text_to_replace, replacement_text)

        # 将修改后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_file_contents)

        print("文本替换完成")
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"发生错误: {e}")

def prettify_xml(elem):
    """返回格式化和缩进的XML字符串"""
    rough_string = ET.tostring(elem, encoding='unicode', method='xml')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="    ")

def generate_xml(file_path,in_exclude:list[str]):
    # 创建根元素
    migration = ET.Element('migration', attrib={'urlid': 'http://www.microsoft.com/migration/1.0/migxmlext/customfiles'})

    # 创建 component 元素
    component = ET.SubElement(migration, 'component', attrib={'type': 'Documents', 'context': 'User'})

    # 创建 displayName 元素
    display_name = ET.SubElement(component, 'displayName')
    display_name.text = 'File Migration'

    # 创建 role 元素
    role = ET.SubElement(component, 'role', attrib={'role': 'Data'})

    # 创建 rules 元素
    rules = ET.SubElement(role, 'rules', attrib={'context': 'User'})

    # 创建 include 元素
    include = ET.SubElement(rules, 'include')

    # 创建 objectSet 元素
    object_set_include = ET.SubElement(include, 'objectSet')

    # 添加 pattern 元素到 include 的 objectSet
    patterns_include = [
        r"%SystemDrive%\Program Files\* %SystemDrive%\Program Files\*",
        r"%SystemDrive%\Program Files (x86)\* %SystemDrive%\Program Files (x86)\*"
    ]

    for pattern_text in patterns_include:
        pattern = ET.SubElement(object_set_include, 'pattern', attrib={'type': 'File'})
        pattern.text = pattern_text

    # 创建 exclude 元素
    exclude = ET.SubElement(rules, 'exclude')

    # 创建 objectSet 元素
    object_set_exclude = ET.SubElement(exclude, 'objectSet')

    # 添加 pattern 元素到 exclude 的 objectSet
    patterns_exclude = []
    for v in in_exclude:
        patterns_exclude.append(v + " " + v)

    for pattern_text in patterns_exclude:
        pattern = ET.SubElement(object_set_exclude, 'pattern', attrib={'type': 'File'})
        pattern.text = pattern_text

    # 将生成的 XML 转换为格式化的字符串
    xml_string = prettify_xml(migration)

    # 打印生成的 XML 字符串
    print(xml_string)

    # 将生成的 XML 保存到文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_string)

def list_common_files(directories, output_file):
    """
    遍历指定目录的第一层内容，并将其写入到指定的输出文件中。

    :param directories: 要遍历的目录列表
    :param output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        for directory in directories:
            if os.path.exists(directory):
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    if os.path.isfile(item_path) or os.path.isdir(item_path):
                        file.write(f"{item}\n")
            else:
                print(f"目录 {directory} 不存在\n\n")
    print(f"已保存到 {output_file}")

def read_txt_file_line_by_line(file_path):
    """
    逐行读取一个文本文件并返回行的列表。

    参数:
    file_path (str): 文本文件的路径。

    返回:
    list: 从文件中读取的行列表。
    """
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip())  # 去除换行符
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在。")
    except IOError:
        print(f"读取文件 {file_path} 时发生错误。")
    
    return lines

if __name__ == "__main__":
    # 必须在转移的目标系统上运行本程序
    print("请在转移的目标系统上运行本程序")

    # 让用户输入被迁移用户在Users/xxx的用户名
    username = input("请输入被迁移用户在Users/xxx的用户名：")

    # 让用户输入脱机系统根目录
    os_root = input("请输入脱机系统根目录(例如:D:\\)：")

    # 处理在USMT中使用NTUSER.DAT的问题,让reg.xml中的路径正确
    # 首先先挂载NTUSER.DAT
    hku_tmp_user = r"HKU\TempUser" + username
    load_reg(hku_tmp_user,os.path.join(os_root,"Users",username,"NTUSER.DAT"))
    print(os.path.join(os_root,"Users",username,"NTUSER.DAT") + "已挂载到注册表" + hku_tmp_user)
    print("如果" + os.path.join(os_root,"Users",username,"NTUSER.DAT") +"储存于移动磁盘,而造成磁盘占用,请在操作完成后,前往注册表卸载它")

    # 替换 替换路径 为 hku_tmp_user
    replace_text_in_file("reg.xml","替换路径",hku_tmp_user)

    # 根据用户名替换file.xml的路径
    replace_text_in_file("file.xml","替换用户名",username)

    # 指定排除
    exclude_32 = []
    for exclude in """
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
    """.split("\n"):
        # 去除换行符
        exclude = exclude.strip()
        if exclude:
            exclude_32.append("%SystemDrive%\\Program Files (x86)\\" + exclude)

    exclude_64 = []
    for exclude in """
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
    """.split("\n"):
        # 去除换行符
        exclude = exclude.strip()
        if exclude:
            exclude_64.append("%SystemDrive%\\Program Files\\" + exclude)

    # 扫描Program Files/Common Files和Program Files (x86)/Common Files，将里面的内容输出到txt，由用户决定保留哪些。
    list_common_files([
        os.path.join(os_root,"Program Files/Common Files"),
       os.path.join(os_root,"Program Files (x86)/Common Files")
    ], "common_files_list.txt")
    all_files = read_txt_file_line_by_line("common_files_list.txt")
    
    print("请修改common_files_list.txt,保留你想迁移的,删除不想迁移的,然后按回车键继续...")
    input()

    # 然后取反，将需要排除的添加到file1.xml
    baoliu_files = read_txt_file_line_by_line("common_files_list.txt")

    # 取反
    exclude_files = list(set(all_files) - set(baoliu_files))
    exclude_files2 = exclude_files.copy()
    for i in range(len(exclude_files)):
        exclude_files[i] = "%SystemDrive%\\Program Files\\Common Files" + exclude_files[i]
    for i in range(len(exclude_files2)):
        exclude_files2[i] = "%SystemDrive%\\Program Files (x86)\\Common Files" + exclude_files2[i]
   
    # 生成file1.xml，里面指定迁移Program Files和Program Files (x86)
    generate_xml("file1.xml",exclude_32 + exclude_64 + exclude_files + exclude_files2)
