import xml.etree.ElementTree as ET
from language import translator

def ask_user_questions():
    # 询问用户Windows目录路径
    win_dirs = []
    while True:
        path = input(translator.translate("请输入Windows目录路径（如C:\\Windows），或输入'完成'结束输入: "))
        if path.lower() == translator.translate('完成'):
            break
        win_dirs.append(path)

    # 询问用户是否在检测到多个Windows目录时迁移失败
    fail_on_multiple = input(translator.translate("如果检测到多个Windows目录，是否使迁移失败？（是/否）: ")).strip().lower() == translator.translate('是')

    # 询问用户是否有自定义的驱动器映射
    mappings = []
    custom_mapping = input(translator.translate("是否需要自定义驱动器映射？（是/否）: ")).strip().lower() == translator.translate('是')
    if custom_mapping:
        while True:
            source = input(translator.translate("请输入源驱动器路径（如C:\\），或输入'完成'结束输入: "))
            if source.lower() == translator.translate('完成'):
                break
            destination = input(translator.translate("请输入目标驱动器路径（如D:\\），对应源驱动器") + " " + source + " " + translator.translate(": "))
            mappings.append((source, destination))

    return win_dirs, fail_on_multiple, mappings

def generate_offline_xml(win_dirs, fail_on_multiple, mappings):
    # 创建根元素
    offline = ET.Element("offline")

    # 创建winDir元素
    win_dir = ET.SubElement(offline, "winDir")
    for path in win_dirs:
        path_element = ET.SubElement(win_dir, "path")
        path_element.text = path

    # 添加failOnMultipleWinDir元素
    fail_on_multiple_windir = ET.SubElement(offline, "failOnMultipleWinDir")
    fail_on_multiple_windir.text = "1" if fail_on_multiple else "0"

    # 添加mappings元素
    if mappings:
        mappings_element = ET.SubElement(offline, "mappings")
        for source, destination in mappings:
            path_element = ET.SubElement(mappings_element, "path")
            path_element.text = f"{source},{destination}"

    # 生成XML字符串
    xml_str = ET.tostring(offline, encoding='utf-8').decode('utf-8')
    return xml_str

def save_to_file(xml_str, filename="offline.xml"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(xml_str)
    print(translator.translate("已生成并保存XML文件到")+" " + filename)

if __name__ == "__main__":
    win_dirs, fail_on_multiple, mappings = ask_user_questions()
    xml_str = generate_offline_xml(win_dirs, fail_on_multiple, mappings)
    save_to_file(xml_str)
