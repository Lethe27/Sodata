# -*- coding: utf-8 -*- 
# @File : test_chunk_clean.py
# @Author : zh 
# @Time : 2024/4/16 下午2:16
# @Desc : 测试文本块清洗模块
from sodata.chunk_clean import ChunkCleanTool
from sodata.text_split import BookSplitTool
from sodata.file_process import FileProcessTool


# #1.测试remove_duplicates_exact--精确匹配去重
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# text_data = FileProcessTool.process_txt_file(input_path)
# chunk_list, chunk_size = BookSplitTool.convert_book_to_chunks(text_data)
# unique_paragraphs, repeated_text = ChunkCleanTool.remove_duplicates_exact(chunk_list)
# print(f"unique_paragraphs_num:{len(unique_paragraphs)}\nrepeated_text:{repeated_text}")


# #2.测试remove_duplicates_minhash-- MinHash去重：对于段落列表中相似性较大的段落进行去重
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# text_data = FileProcessTool.process_txt_file(input_path)
# chunk_list, chunk_size = BookSplitTool.convert_book_to_chunks(text_data)
# unique_paragraphs, repeated_text = ChunkCleanTool.remove_duplicates_minhash(chunk_list)
# print(f"unique_paragraphs_num:{len(unique_paragraphs)}\nrepeated_text_num:{len(repeated_text)}")


# #3.测试clean_text-- 对于小说文本片段(chunk)进行数据清洗
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# text_data = FileProcessTool.process_txt_file(input_path)
# chunk_list, chunk_size = BookSplitTool.convert_book_to_chunks(text_data)
# clean_chunk_list = []
# repeated_text_list = []
# for chunk in chunk_list:
#     text_clean, repeated_text = ChunkCleanTool.clean_text(chunk)
#     clean_chunk_list.append(text_clean)
#     repeated_text_list.append(repeated_text)
# print(f"clean_chunk_num:{len(clean_chunk_list)}\nrepeated_text_num:{len(repeated_text_list)}")
