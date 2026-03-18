# -*- coding: utf-8 -*- 
# @File : test_text_clean.py 
# @Author : zh 
# @Time : 2024/4/10 16:26 
# @Desc : 测试文本清洗模块

from sodata.text_clean import TextCleanTool
from sodata.text_split import BookSplitTool
from sodata.file_process import FileProcessTool

#1.测试cascade_deduplication-- 对于任意一段小说进行精确匹配去重和MinHash模糊去重重
input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
text_data = FileProcessTool.process_txt_file(input_path)
text_clean, repeated_text = TextCleanTool.cascade_deduplication(text_data)
print(f"text_clean_num:{len(text_clean)}\nrepeated_text_num:{len(repeated_text)}")
