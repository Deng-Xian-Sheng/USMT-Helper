import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(elem):
    """返回格式化和缩进的XML字符串"""
    rough_string = ET.tostring(elem, encoding='unicode', method='xml')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="    ")

def generate_xml(file_path):
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
        r"%SystemDrive%\Users\替换用户名\Local\Appdata\* %SystemDrive%\Users\%USERNAME%\Local\Appdata\*",
        r"%SystemDrive%\Users\替换用户名\Roaming\Appdata\* %SystemDrive%\Users\%USERNAME%\Roaming\Appdata\*"
    ]

    for pattern_text in patterns_include:
        pattern = ET.SubElement(object_set_include, 'pattern', attrib={'type': 'File'})
        pattern.text = pattern_text

    # 创建 exclude 元素
    exclude = ET.SubElement(rules, 'exclude')

    # 创建 objectSet 元素
    object_set_exclude = ET.SubElement(exclude, 'objectSet')

    # 添加 pattern 元素到 exclude 的 objectSet
    patterns_exclude = [
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Temp %SystemDrive%\Users\%USERNAME%\AppData\Local\Temp",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Packages %SystemDrive%\Users\%USERNAME%\AppData\Local\Packages",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\TileDataLayer %SystemDrive%\Users\%USERNAME%\AppData\Local\TileDataLayer",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Microsoft\Temp %SystemDrive%\Users\%USERNAME%\AppData\Local\Microsoft\Temp",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Microsoft\Credentials %SystemDrive%\Users\%USERNAME%\AppData\Local\Microsoft\Credentials",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Microsoft\Windows %SystemDrive%\Users\%USERNAME%\AppData\Local\Microsoft\Windows",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Microsoft\Windows\InputPersonalization %SystemDrive%\Users\%USERNAME%\AppData\Local\Microsoft\Windows\InputPersonalization",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Microsoft\Windows\Side bars %SystemDrive%\Users\%USERNAME%\AppData\Local\Microsoft\Windows\Side bars",
        r"%SystemDrive%\Users\替换用户名\AppData\Local\Microsoft\WindowsApps %SystemDrive%\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps",
        r"%SystemDrive%\Users\替换用户名\AppData\Roaming\Microsoft\Credentials %SystemDrive%\Users\%USERNAME%\AppData\Roaming\Microsoft\Credentials",
        r"%SystemDrive%\Users\替换用户名\AppData\Roaming\Microsoft\SystemCertificates %SystemDrive%\Users\%USERNAME%\AppData\Roaming\Microsoft\SystemCertificates",
        r"%SystemDrive%\Users\替换用户名\AppData\Roaming\Microsoft\Crypto %SystemDrive%\Users\%USERNAME%\AppData\Roaming\Microsoft\Crypto",
        r"%SystemDrive%\Users\替换用户名\AppData\Roaming\Microsoft\Vault %SystemDrive%\Users\%USERNAME%\AppData\Roaming\Microsoft\Vault",
        r"%SystemDrive%\Users\替换用户名\AppData\Roaming\Microsoft\Windows %SystemDrive%\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows"
    ]

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

# 调用函数生成 XML 文件
generate_xml('output.xml')
