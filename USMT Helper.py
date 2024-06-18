from math import e
import os
import xml.etree.ElementTree as ET

def generate_xml(file_path,in_exclude:list[str]):
    # 创建根元素
    migration = ET.Element('migration', attrib={'urlid': 'http://www.microsoft.com/migration/1.0/migxmlext/file1'})

    # 创建 component 元素
    component = ET.SubElement(migration, 'component', attrib={'type': 'Documents', 'context': 'System'})

    # 创建 displayName 元素
    display_name = ET.SubElement(component, 'displayName')
    display_name.text = 'File Migration'

    # 创建 role 元素
    role = ET.SubElement(component, 'role', attrib={'role': 'Data'})

    # 创建 rules 元素
    rules = ET.SubElement(role, 'rules', attrib={'context': 'System'})

    # 创建 include 元素
    include = ET.SubElement(rules, 'include')

    # 创建 objectSet 元素
    object_set_include = ET.SubElement(include, 'objectSet')

    # 添加 pattern 元素到 include 的 objectSet
    patterns_include = [
        r"%CSIDL_PROGRAM_FILES%\* [*]",
        r"%CSIDL_PROGRAM_FILESX86%\* [*]"
    ]

    for pattern_text in patterns_include:
        pattern = ET.SubElement(object_set_include, 'pattern', attrib={'type': 'File'})
        pattern.text = pattern_text

    # 创建 exclude 元素
    exclude = ET.SubElement(rules, 'exclude')

    # 创建 objectSet 元素
    object_set_exclude = ET.SubElement(exclude, 'objectSet')

    # 添加 pattern 元素到 exclude 的 objectSet
    for pattern_text in in_exclude:
        pattern = ET.SubElement(object_set_exclude, 'pattern', attrib={'type': 'File'})
        pattern.text = pattern_text
    
    tree = ET.ElementTree(migration)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

    print("生成的XML已保存到" + file_path)


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

def read_txt_file_by_line(file_path):
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
    # 让用户输入脱机系统根目录
    os_root = input("请输入脱机系统根目录(例如:D:\\)：")

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
            exclude_32.append(f"%CSIDL_PROGRAM_FILESX86%\\{exclude}\\* [*]")

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
            exclude_64.append(f"%CSIDL_PROGRAM_FILES%\\{exclude}\\* [*]")

    # 扫描C:\\Program Files\Common Files和C:\\Program Files (x86)\Common Files，将里面的内容输出到txt，由用户决定保留哪些。
    list_common_files([
        os.path.join(os_root,"Program Files\\Common Files"), # type: ignore
       os.path.join(os_root,"Program Files (x86)\\Common Files") # type: ignore
    ], "common_files_list.txt")
    all_files = read_txt_file_by_line("common_files_list.txt")
    
    print("请修改common_files_list.txt,保留你想迁移的,删除不想迁移的,然后按回车键继续...")
    input()

    # 然后取反，将需要排除的添加到file1.xml
    baoliu_files = read_txt_file_by_line("common_files_list.txt")

    # 取反
    exclude_files = list(set(all_files) - set(baoliu_files))
    exclude_files2 = exclude_files.copy()
    for i in range(len(exclude_files)):
        exclude_files[i] = f"%CSIDL_PROGRAM_FILES_COMMON%\\{exclude_files[i]}\\* [*]"
    for i in range(len(exclude_files2)):
        exclude_files2[i] = f"%CSIDL_PROGRAM_FILES_COMMONX86%\\{exclude_files2[i]}\\* [*]"
   
    # 生成file1.xml，里面指定迁移%CSIDL_PROGRAM_FILES% %CSIDL_PROGRAM_FILESX86%
    generate_xml("file1.xml",exclude_32 + exclude_64 + exclude_files + exclude_files2)
