import os

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

# 定义要遍历的目录
directories = [
    "venv",
]

# 定义输出文件路径
output_file = "common_files_list.txt"

# 调用函数
list_common_files(directories, output_file)
