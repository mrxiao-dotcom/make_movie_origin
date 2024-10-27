import json
import os
import shutil
import re
import random


def print_key_value_pairs_from_file(file_path):
    try:
        # 打开文件并加载JSON数据
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data
    except FileNotFoundError:
        print("The file was not found.")
    except json.JSONDecodeError:
        print("The file is not a valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")


def filter_files_by_extension(directory, extension):
    # 检查扩展名是否以点开头
    if not extension.startswith('.'):
        extension = '.' + extension

    # 存储符合条件的文件
    filtered_files = []

    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名
            if file.endswith(extension):
                # 提取文件名和后缀
                name, ext = os.path.splitext(file)
                filtered_files.append(name)

    return filtered_files

def contains_chinese(s):
    return any('\u4e00' <= char <= '\u9fff' for char in s)

def read_and_convert_to_json(input_file, output_file):
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # 将文本对话转换为列表
    dialogues = text.split("学生：")
    conversation_list = []

    for dialogue in dialogues[1:]:  # 跳过第一个空字符串
        lines = dialogue.split("\n")
        student_question = lines[0].strip()
        teacher_answer = ""
        for line in lines[1:]:
            if line.startswith("老师："):
                teacher_answer = line[len("老师："):].strip()
                break
        if teacher_answer:
            conversation_list.append({
                "学员": student_question,
                "老师": teacher_answer
            })

    # 确保输出文件的目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 将列表转换为JSON并保存到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(conversation_list, f, ensure_ascii=False, indent=4)

def read_json_file(file_path):
    # 确保文件存在
    if not os.path.exists(file_path):
        print("文件不存在，请检查路径。")
        return []

    # 读取JSON文件并解析数据
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def extract_path_parts(file_path):
    # 提取文件的目录路径
    dir_path = os.path.dirname(file_path)
    # 提取文件名（包括扩展名）
    file_name = os.path.basename(file_path)
    # 提取文件扩展名
    file_extension = os.path.splitext(file_name)[1]
    # 提取不包含扩展名的文件名
    file_name_without_extension = os.path.splitext(file_name)[0]

    return {
        "directory": dir_path,
        "file_name": file_name,
        "file_extension": file_extension,
        "file_name_without_extension": file_name_without_extension
    }


def copy_images(src_file, dest_names):
    # 确保源文件存在
    if not os.path.exists(src_file):
        print(f"源文件 {src_file} 不存在，请检查路径。")
        return

    # 获取源文件的目录和扩展名
    src_dir = os.path.dirname(src_file)
    file_extension = os.path.splitext(src_file)[1]

    # 复制图片
    for name in dest_names:
        # 构建目标文件的完整路径
        dest_file = os.path.join(src_dir, f"{name}{file_extension}")
        if not os.path.exists(dest_file):
            # 复制文件
            shutil.copy(src_file, dest_file)
            print(f"图片已复制为：{name}{file_extension}")


def clear_directory(directory):
    # 检查目录是否存在
    if os.path.exists(directory):
        # 遍历目录中的所有文件和文件夹
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # 如果是文件，则删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # 如果是目录，则递归删除
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        # 如果目录不存在，则创建它
        os.makedirs(directory, exist_ok=True)
        print(f"目标目录 {directory} 已创建。")


def copy_numeric_filename_files(src_dir, dst_dir, clear=True):
    # 清空目标目录
    if clear:
        clear_directory(dst_dir)

    # 检查源目录是否存在
    if not os.path.exists(src_dir):
        print(f"源目录 {src_dir} 不存在。")
        return

    # 遍历源目录下的所有文件
    file_list = os.listdir(src_dir)
    for filename in file_list:
        name, ext = os.path.splitext(filename)
        # 检查文件名是否为纯数字
        if name.isdigit():
            # 构建完整的文件路径
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)
            if not os.path.exists(dst_file):
                # 复制文件
                shutil.copy(src_file, dst_file)
                print(f"文件 {filename} 已复制到 {dst_dir}")


def copy_and_rename_image(src_image_path, dst_directory):
    # 检查源图片是否存在
    if not os.path.exists(src_image_path):
        print("源图片不存在。")
        return

    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory, exist_ok=True)

    # 获取源图片的扩展名
    src_extension = os.path.splitext(src_image_path)[1]

    # 构建目标图片的完整路径（文件名改为“1”，扩展名保持不变）
    dst_image_path = os.path.join(dst_directory, f"1{src_extension}")

    # 复制源图片到目标目录，并重命名
    shutil.copy(src_image_path, dst_image_path)
    print(f"图片已复制并重命名为：{dst_image_path}")


def copy_outmp4_and_rename_files(source_dir, target_dir):
    """
    Copy files from source directory to target directory and rename them.

    Args:
    source_dir (str): The path to the source directory.
    target_dir (str): The path to the target directory.

    Returns:
    None
    """
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 遍历源目录中的所有文件
    for filename in os.listdir(source_dir):
        if filename.endswith('-out.mp4'):
            # 构造完整的文件路径
            source_file = os.path.join(source_dir, filename)
            # 构造目标文件名（去掉'-out'并改为大写扩展名）
            target_file = os.path.join(target_dir, filename[:-8] + '.MP4')
            # 复制文件

            if not os.path.exists(target_file):
                shutil.copy(source_file, target_file)
                print(f'Copied and renamed {filename} to {target_file}')


def delete_files_in_directory(directory, exclude_files=None):
    # 如果没有提供排除文件列表，则创建一个空列表
    if exclude_files is None:
        exclude_files = []

    # 检查目录是否存在
    if not os.path.exists(directory):
        print("目录不存在。")
        return

    # 遍历目录中的所有文件和子目录
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 判断文件是否需要被排除
        if filename in exclude_files:
            print(f"文件 {filename} 被排除，跳过删除。")
            continue

        # 判断是文件还是目录
        if os.path.isfile(file_path) or os.path.islink(file_path):
            # 删除文件或链接
            os.remove(file_path)
            print(f"已删除文件：{file_path}")
        elif os.path.isdir(file_path):
            # 如果是目录，则递归删除
            shutil.rmtree(file_path)
            print(f"已删除目录：{file_path}")


def format_json_file(file_path):
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            json_str = file.read()

        # 替换 "]," 为 "],\n" 并添加换行符
        formatted_str = json_str.replace("],[", "],\n")

        # 打印格式化后的内容
        print(formatted_str)

    except FileNotFoundError:
        print("文件未找到，请检查路径是否正确。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")


def extract_sentences(text):
    # 使用正则表达式匹配句子，包括中英文的句号、感叹号、问号和换行符
    # 同时确保这些符号不在引号内
    sentences = re.split(r'(?<![\'"])[。？！；\n]', text)

    # 定义一个空列表来存储清洗后的句子
    cleaned_sentences = []

    for sentence in sentences:
        # 去除句子中的引号
        cleaned_sentence = re.sub(r'["\'“”‘’]+', '', sentence)
        # 去除句子两端的空白字符
        cleaned_sentence = cleaned_sentence.strip()
        # 过滤掉空字符串
        if cleaned_sentence:
            cleaned_sentences.append(cleaned_sentence)

    return cleaned_sentences


def format_and_write_json(input_file_path, output_file_path):
    """
    读取原始的TXT文件内容，并将其格式化为JSON格式后写入新文件。
    """
    try:
        # 读取原始文件内容
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()

        # 将单引号替换为双引号
        content = content.replace("'", '"').replace("\n", '')

        # 将内容解析为JSON
        data = json.loads(content)

        # 标准化键名
        data = [standardize_keys(item) for item in data]

        # 将JSON对象格式化为字符串
        formatted_content = json.dumps(data, indent=4, ensure_ascii=False)

        # 写入格式化后的内容到新文件
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(formatted_content)

        print(f"File has been formatted and written to {output_file_path}")
    except json.JSONDecodeError:
        print(f"Error: The content of {input_file_path} is not valid JSON.")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")

def load_json(file_path):
    """
    从指定路径加载JSON文件。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def check_json_format(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取所有内容
            content = file.read()

            # 尝试将内容解析为JSON
            data = json.loads(content)
            print("JSON格式正确，内容已成功读取。")
            return data

    except json.JSONDecodeError as e:
        # 获取错误信息和位置
        msg = e.msg
        lineno = e.lineno
        colno = e.colno
        print(f"JSON格式错误：{msg}")
        print(f"错误位于：第 {lineno} 行，第 {colno} 列。")
    except FileNotFoundError:
        print("文件未找到，请检查路径是否正确。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")


def save_json(data, file_path):
    """
    将数据保存到指定路径的JSON文件。
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def validate_and_update_effects(json_data, effects_folder, empty=0):
    """
    验证JSON数据中的“特效”字段是否存在于特效文件夹中，如果不存在则替换为空字符串。
    同时标准化键名。
    """
    # 获取特效文件夹中的所有文件名
    effect_files = set(os.listdir(effects_folder))
    effect_list = list(effect_files)
    print("为分镜随机设计特效...")
    for item in json_data:
        # 标准化键名
        item.update(standardize_keys(item))

        effect_file = item.get('特效')

        # 检查特效文件是否存在于文件夹中
        if effect_file not in effect_files:


            if empty == 0: #这个标识如果等于0，那么不要特效，否则随机指派特效
                item['特效'] = ""
            else:
                texiao = random.choice(effect_list)
                item['特效'] = texiao
                print("特效：%s"%texiao)

    return json_data

def standardize_keys(item):
    """
    标准化字典项的键名，确保其符合预期的格式，并按顺序重命名。
    """
    expected_keys = ['画面', '角色', '文案', '特效']
    new_item = {}

    # 映射表，用于将可能的键名映射到标准键名
    key_mapping = {
        'environment': '环境',
        'env': '环境',
        'scene': '环境',
        'character': '角色',
        'role': '角色',
        'char': '角色',
        'dialogue': '文案',
        'line': '文案',
        'effect': '特效',
        'fx': '特效',
        # 可以在此处添加更多映射
    }

    # 处理每个键值对，并重命名键名
    for key, value in item.items():
        new_key = key_mapping.get(key.lower(), key)  # 尝试映射键名
        if new_key in expected_keys:
            new_item[new_key] = value

    # 确保所有预期的键都存在，如果缺少则添加空字符串
    for ek in expected_keys:
        new_item.setdefault(ek, '')

    return new_item

# 如果连续几个分镜，主角相同，则合并到一起
def merge_consecutive_entries(input_file_path, output_file_path):
    # 从文件读取文本内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 初始化合并后的列表
    merged_data = []
    current_entry = None

    for entry in data:
        # 如果当前条目与前一条目的"角色"相同，则合并"文案"
        if current_entry and entry["角色"] == current_entry["角色"]:
            current_entry["文案"] += " " + entry["文案"]
        else:
            # 如果不相同，将前一条目（如果有的话）添加到合并后的列表中
            if current_entry:
                merged_data.append(current_entry)
            # 设置当前条目为新的条目
            current_entry = entry

    # 添加最后一条目到合并后的列表中
    if current_entry:
        merged_data.append(current_entry)

    # 将处理后的数据转换回JSON格式的字符串
    processed_text = json.dumps(merged_data, indent=4, ensure_ascii=False)

    # 保存处理后的文本到文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(processed_text)

    print(f"处理后的文本已保存到: {output_file_path}")

#如果缺失：特效 ，则补特效
def process_file_and_save(input_file_path, output_file_path):
    # 从文件读取文本内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 将文本转换为JSON对象
    data = json.loads(text)

    # 遍历列表中的每个字典对象
    for item in data:
        # 如果"特效"键不存在，则添加它并赋予空字符串作为默认值
        if "特效" not in item:
            item["特效"] = ""

    # 将处理后的数据转换回JSON格式的字符串
    processed_text = json.dumps(data, indent=4, ensure_ascii=False)

    # 保存处理后的文本到文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(processed_text)

    print(f"处理后的文本已保存到: {output_file_path}")

def format_and_save_json_file(file_path):
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            json_str = file.read()

        # 替换 "]," 为 "],\n" 并添加换行符
        formatted_str = json_str.replace("][", ",\n")
        formatted_str = formatted_str.replace("']", "")
        formatted_str = formatted_str.replace("['", "")
        formatted_str = formatted_str.replace("'", "\"")

        # 将格式化后的内容写回原文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_str)

        print("文件已成功格式化并保存。")

    except FileNotFoundError:
        print("文件未找到，请检查路径是否正确。")
    except Exception as e:
        print(f"处理文件时发生错误：{e}")


def count_chinese_characters(text):
    # 使用正则表达式匹配汉字
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    # 返回汉字的数量
    return len(chinese_chars)


def extract_chinese_characters(text):
    # 使用正则表达式匹配中文字符，并保持出现顺序
    return [char for char in re.findall(r'[\u4e00-\u9fff]', text)]

def find_chinese_chars_with_line_numbers(text):
    # 使用正则表达式找到所有中文字符及其在原文中的行数
    chinese_chars_with_line_numbers = []
    lines = text.splitlines()
    for line_number, line in enumerate(lines, start=1):
        for match in re.finditer(r'[\u4e00-\u9fff]', line):
            char = match.group()
            chinese_chars_with_line_numbers.append((char, line_number))
    return chinese_chars_with_line_numbers


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return ""


def compare_chinese_characters_with_line_numbers(file1, file2):
    content1 = read_file(file1)
    content2 = read_file(file2)

    if not content1 or not content2:
        print("一个或两个文件可能是空的，或者读取文件时出错。")
        return [], []

    chinese_line_numbers1 = find_chinese_chars_with_line_numbers(content1)
    chinese_line_numbers2 = find_chinese_chars_with_line_numbers(content2)
    print("file1 和 file2字数分别是:",len(chinese_line_numbers1),len(chinese_line_numbers2))

    diff = {
        'file1': [],
        'file2': []
    }

    # 对比两个列表中的中文字符及其行数
    for char_line1, char_line2 in zip(chinese_line_numbers1, chinese_line_numbers2):
        if char_line1[0] != char_line2[0]:
            diff['file1'].append((char_line1[0], char_line1[1]))
            diff['file2'].append((char_line2[0], char_line2[1]))
            break  # 只对比到第一个不同之处

    # 如果一个文件中的中文字符比另一个多
    if len(chinese_line_numbers1) > len(chinese_line_numbers2):
        diff['file1'].extend(chinese_line_numbers1[len(chinese_line_numbers2):])
    elif len(chinese_line_numbers2) > len(chinese_line_numbers1):
        diff['file2'].extend(chinese_line_numbers2[len(chinese_line_numbers1):])

    return diff

def compare_chinese_characters_with_line_numbers_file_to_txt(file1, content2):
    content1 = read_file(file1)


    if not content1 or not content2:
        print("一个或两个文件可能是空的，或者读取文件时出错。")
        return [], []

    chinese_line_numbers1 = find_chinese_chars_with_line_numbers(content1)
    chinese_line_numbers2 = find_chinese_chars_with_line_numbers(content2)

    diff = {
        'file1': [],
        'file2': []
    }

    # 对比两个列表中的中文字符及其行数
    for char_line1, char_line2 in zip(chinese_line_numbers1, chinese_line_numbers2):
        if char_line1[0] != char_line2[0]:
            diff['file1'].append((char_line1[0], char_line1[1]))
            diff['file2'].append((char_line2[0], char_line2[1]))
            break  # 只对比到第一个不同之处

    # 如果一个文件中的中文字符比另一个多
    if len(chinese_line_numbers1) > len(chinese_line_numbers2):
        diff['file1'].extend(chinese_line_numbers1[len(chinese_line_numbers2):])
    elif len(chinese_line_numbers2) > len(chinese_line_numbers1):
        diff['file2'].extend(chinese_line_numbers2[len(chinese_line_numbers1):])

    return diff


def check_json_format(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容
            data = json.load(file)  # 假设文件是JSON格式

            # 定义期望的格式
            expected_keys = {"角色", "画面", "文案", "特效"}

            # 检查每个元素是否符合格式
            for idx, item in enumerate(data, start=1):
                current_keys = set(item.keys())
                if current_keys != expected_keys:
                    print(f"第{idx}行：缺少或多余的键。期望的键为{expected_keys}，当前的键为{current_keys}")


            return data
    except json.JSONDecodeError as e:
        print(f"文件内容不是有效的JSON格式: {e}")
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

