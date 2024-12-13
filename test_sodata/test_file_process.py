# -*- coding: utf-8 -*- 
# @File : test_file_process.py.py 
# @Author : zh 
# @Time : 2024/4/10 11:01 
# @Desc : 测试文件处理模块
import os

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
# print(f"save to {output_file}!!!")

# #4.测试save_labels_to_jsonl--保存jsonl格式文件
# label = ["INV_CHAR","INV_SEG","INV_TITLE"]
# output_path = "/home/zhanghong/sodata/data/jsonl_data/label.jsonL"
# FileProcessTool.save_labels_to_json(label, output_path)

# #5.测试process_folder_and_save_to_jsonl--递归遍历文件夹，处理每个txt文件，然后将数据保存为一整个JSONL格式
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# output_path = "/home/zhanghong/sodata/data/json_data/《天官赐福》.jsonl"
# FileProcessTool.process_folder_and_save_to_jsonl(input_path, output_path)

# #6.测试processed_rows--处理CSV文件，将每个文本的chunk列表元素拆分成单个元素占一列
#
# input_path = os.path.join("/home/zhanghong/sodata/data/csv_data", "shuf_BL_chunks_36-75.csv")
# output_path = os.path.join("/home/zhanghong/sodata/data/csv_data", "shuf_BL_chunks_36-75_split.csv")
# FileProcessTool.processed_rows(input_path, output_path)

# #7.测试convert_chunkCSV_to_bioJSON--将含有切分后chunk的CSV文件转换为BIO标注后chunk的JSON文件
# input_file = os.path.join("/home/zhanghong/sodata/data/csv_data", "shuf_BL_chunks_81.csv")
# output_file_folder = "/home/zhanghong/sodata/data/jsonl_data"
# FileProcessTool.convert_chunkCSV_to_bioJSONL(input_file, output_file_folder)

# #8.测试split_bioJSONL--将数据集切分为训练集、测试集和开发集
input_file_path = "/home/zhanghong/sodata/data/jsonl_data/origin_chunks_50_bio.jsonl"
output_path = "/home/zhanghong/sodata/data/jsonl_data"
FileProcessTool.split_bioJSONL(input_file_path, output_path, 0.78, 0.15)
