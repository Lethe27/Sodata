### cascade_deduplication
```angular2html
#1.测试cascade_deduplication-- 对于任意一本小说进行精确匹配去重和MinHash模糊去重
input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
text_data = FileProcessTool.process_txt_file(input_path)
text_clean, repeated_text = ChunkCleanTool.cascade_deduplication(text_data)
print(f"text_clean_num:{len(text_clean)}\nrepeated_text_num:{len(repeated_text)}")

>>>
text_clean_num:347163
repeated_text_num:14894
```