import os
import re

# 定义一个函数来执行替换操作
def replace_in_file(file_path):
    # 读取文件内容，指定编码为 UTF-8-BOM
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    # 正则表达式匹配 cu:【字符串】 = { culture_is_discriminated_in = root }
    pattern = r'cu:(\S+) = {\s*culture_is_discriminated_in = root\s*}'
    
    # 替换为新的格式
    modified_content = re.sub(pattern, r'cultural_acceptance_base = { target = cu:\1 value < acceptance_status_4 }', content)
    
    # 如果内容发生了变化，则保存文件，保持 UTF-8-BOM 编码
    if modified_content != content:
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.write(modified_content)
        print(f"Updated file: {file_path}")
    else:
        print(f"No changes made to file: {file_path}")

# 遍历指定目录下的所有txt文件
def process_directory(directory):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        # 只处理txt文件
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            replace_in_file(file_path)

# 设置目标目录
directory = './'  # 当前目录，或者你可以修改为具体的路径

# 执行目录处理
process_directory(directory)
