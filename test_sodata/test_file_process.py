# -*- coding: utf-8 -*- 
# @File : test_file_process.py.py 
# @Author : zh 
# @Time : 2024/4/10 11:01 
# @Desc : 测试文件处理模块

# 调用函数
from sodata.file_process import FileProcessTool

# #1.测试process_folder_and_save_to_jsonl--小说文本转换成jsonl格式
# FileProcessTool.process_folder_and_save_to_jsonl('/home/zhanghong/sodata/data/BL',  '/home/zhanghong/sodata/data/json_data/BL.jsonl')

# #2.测试count_lines--计算文件行数
# print(FileProcessTool.count_lines('/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'))


# #3.测试save_to_jsonl--保存jsonl格式文件
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# output_path = "/home/zhanghong/sodata/data/json_data/《天官赐福》.jsonL"
# text_data = FileProcessTool.process_txt_file(input_path)
# FileProcessTool.save_to_jsonl(text_data, output_path)
    