import winreg as reg

def decode_binary_string(data):
    try:
        # 尝试解码为UTF-16LE格式的字符串
        return data.decode('utf-16le')
    except UnicodeDecodeError:
        return None

def read_registry_keys(path):
    try:
        # 打开注册表路径
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, path) as key:
            # 获取子项的数量
            count = reg.QueryInfoKey(key)[0]
            # 遍历每一个子项
            for i in range(count):
                # 获取子项的名称
                name = reg.EnumKey(key, i)
                # 尝试打开子项
                with reg.OpenKey(key, name) as subkey:
                    try:
                        # 遍历子项中的每个值
                        value_count = reg.QueryInfoKey(subkey)[1]
                        for j in range(value_count):
                            value_name, value_data, value_type = reg.EnumValue(subkey, j)
                            if value_type == reg.REG_BINARY:  # 检查值类型是否为二进制
                                # 尝试解码二进制数据
                                readable_string = decode_binary_string(value_data)
                                if readable_string:
                                    
                                    print(f"Subkey: {name}, Value Name: {value_name}, Value: {readable_string}")
                    except EnvironmentError:
                        print(f"Failed to read values from {name}")
    except EnvironmentError:
        print(f"Failed to open key at path: {path}")

# 调用函数
read_registry_keys(r"SAM2\SAM\Domains\Account\Users")



# import winreg as reg

# def get_sid(username):
#     try:
#         # 打开SAM数据库（需先加载此数据库）
#         with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, "SAM2\\SAM\\Domains\\Account\\Users\\Names".format(username)) as user_key:
#             # 读取默认值，其中包含了用户的RID（相对ID）
#             print(f"User key for {user_key} found")
#             rid, _ = reg.QueryValueEx(user_key, "")
#             print(f"RID for {username}: {rid}")
            
#             # 使用RID去获取SID信息
#             with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, f"SAM2\\SAM\\Domains\\Account\\Users\\{rid}") as sid_key:
#                 sid, _ = reg.QueryValueEx(sid_key, "V")
#                 print(f"SID for {username}: {sid[:8]}-{sid[8:12]}-{sid[12:16]}-{sid[16:20]}-{sid[20:]}")
#     except Exception as e:
#         print(f"Error: {e}")

# # 使用此函数，传入用户名
# get_sid("x1761")
