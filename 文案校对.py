import re
from 格式化分镜文档 import *


if __name__ == '__main__':
    print("hi 我是文案校对.py")
    #上传('高阶推文_竖屏短视频尺寸.mp4')

    yuanwen = True
    fenjing = True
    fenjinggao = False

    文档集合 = '文档集合'
    file_path1 = f'{文档集合}/段落列表.txt'
    file_path2 = f'原文.txt'
    input_file_path = '文档集合/分镜.txt'
    ################## 校对原文与分段 ############
    if yuanwen:

        file_path1 = f'{文档集合}/段落列表.txt'
        file_path2 = f'原文.txt'
        diff = compare_chinese_characters_with_line_numbers(file_path1, file_path2)

        print(f"文件1中的差异（字符，位置）: {diff['file1']}",file_path1)
        print(f"文件2中的差异（字符，位置）: {diff['file2']}",file_path2)

    ############### 校对分镜与分段 ###############
    if fenjing:
        json_data = check_json_format(input_file_path)
        fenjing = ""
        for itor in json_data:
            fenjing += itor['文案']+'\n'
        diff = compare_chinese_characters_with_line_numbers_file_to_txt(file_path1,fenjing)
        print(diff)

    if fenjinggao:

        check_json_format(input_file_path)
        json_data = load_json(input_file_path)