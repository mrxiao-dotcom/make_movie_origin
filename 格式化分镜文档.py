from CommonFunction import *



if __name__ == '__main__':
    # 文件夹路径
    input_file_path = '文档集合/分镜.txt'  # 请替换为实际的原始文件路径

    format_and_save_json_file(input_file_path)



    print("分镜文件已更新。")

"""

    effects_folder = r'特效'  # 请替换为实际的特效文件夹路径
    input_file_path = '文档集合/分镜.txt'  # 请替换为实际的原始文件路径
    output_file_path = '文档集合/分镜.txt'  # 请替换为实际的目标文件路径
    json_file_path = '文档集合/分镜.txt'  # 请替换为实际的目标文件路径

    # 格式化并写入JSON文件
    format_and_write_json(input_file_path, output_file_path)

    #补特效模块
    processed_text = process_file_and_save(input_file_path, output_file_path)

    #合并模块
    merge_consecutive_entries(input_file_path, output_file_path)


    # 加载JSON数据
    json_data = load_json(output_file_path)
    print(json_data)

    # 验证并更新特效字段
    updated_json_data = validate_and_update_effects(json_data, effects_folder, 0)

    # 保存更新后的JSON数据
    save_json(updated_json_data, json_file_path)
    
"""