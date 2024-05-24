from elevate import elevate
import subprocess
import time

# todo 尝试寻找更优雅的提权方式
# 以管理员身份运行特定逻辑，并且封装输出
# 管理员权限
elevate()
"""
import os
import sys
import inspect
import subprocess
import multiprocessing
import queue

def write_function_to_file(func, filename):
    source_code = inspect.getsource(func)
    with open(filename, 'w') as file:
        file.write(source_code)
        file.write('\n')
        file.write('import sys\n')
        file.write('import queue\n')
        file.write('import threading\n')
        file.write(inspect.getsource(RedirectOutput))
        file.write('\n')
        file.write('if __name__ == "__main__":\n')
        file.write('    q = queue.Queue()\n')
        file.write('    with RedirectOutput(q):\n')
        file.write('        result = {}()\n'.format(func.__name__))
        file.write('    while not q.empty():\n')
        file.write('        print(q.get())\n')

class RedirectOutput:
    def __init__(self, q):
        self.q = q
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def write(self, message):
        self.q.put(message)

    def flush(self):
        pass

    def __enter__(self):
        sys.stdout = self
        sys.stderr = self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

def run_as_admin(script_path):
    try:
        subprocess.run(['powershell', '-Command', f'Start-Process python "{script_path}" -Verb RunAs'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run script as admin: {e}")

def execute_function_in_new_process(func, output_queue):
    script_path = "temp_script.py"
    write_function_to_file(func, script_path)
    
    process = multiprocessing.Process(target=run_as_admin, args=(script_path,))
    process.start()

    # Allow the process to start and immediately return
    return

# Example usage
def example_function():
    print("This is a test function.")
    return "Function execution completed."

if __name__ == "__main__":
    output_queue = multiprocessing.Queue()
    execute_function_in_new_process(example_function, output_queue)

"""

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

# 加载注册表，重复加载没问题
load_reg(r"HKLM\testsys",r"D:\wim\Windows\System32\config\SYSTEM")

try:
    # 读取加载的注册表
    pass
finally:
    # 卸载注册表
    unload_reg(r"HKLM\testsys")

time.sleep(10)