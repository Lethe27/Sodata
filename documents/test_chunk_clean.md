
### remove_duplicates_exact
```angular2html
 #1.测试remove_duplicates_exact--精确匹配去重
    input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
    text_data = FileProcessTool.process_txt_file(input_path)
    chunk_list, chunk_size = BookSplitTool.convert_book_to_chunks(text_data)
    unique_paragraphs, repeated_text = ChunkCleanTool.remove_duplicates_exact(chunk_list)
    print(f"unique_paragraphs:{len(unique_paragraphs)}\nrepeated_text:{repeated_text}")

>>>
the max length of chunk is 3019
unique_paragraphs_num:556
repeated_text_num:0
```
### remove_duplicates_minhash
```angular2html
#2.测试remove_duplicates_minhash-- MinHash去重：对于段落列表中相似性较大的段落进行去重
input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
text_data = FileProcessTool.process_txt_file(input_path)
chunk_list, chunk_size = BookSplitTool.convert_book_to_chunks(text_data)
unique_paragraphs, repeated_text = ChunkCleanTool.remove_duplicates_minhash(chunk_list)
print(f"unique_paragraphs_num:{len(unique_paragraphs)}\nrepeated_text_num:{len(repeated_text)}")

>>>
the max length of chunk is 3081
unique_paragraphs_num:112
repeated_text_num:437
```
### cascade_deduplication

```angular2html
#3.测试cascade_deduplication-- 对于任意一段小说进行精确匹配去重和MinHash模糊去重重
input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
text_data = FileProcessTool.process_txt_file(input_path)
text_clean, repeated_text = ChunkCleanTool.cascade_deduplication(text_data)
print(f"text_clean_num:{len(text_clean)}\nrepeated_text_num:{len(repeated_text)}")

>>>
text_clean_num:347163
repeated_text_num:14894
```

### clean_text
```angular2html
4.测试clean_text-- 对于小说文本片段(chunk)进行数据清洗
input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
text_data = FileProcessTool.process_txt_file(input_path)
chunk_list, chunk_size = BookSplitTool.convert_book_to_chunks(text_data)
clean_chunk_list = []
repeated_text_list = []
for chunk in chunk_list:
    text_clean, repeated_text = ChunkCleanTool.clean_text(chunk)
    clean_chunk_list.append(text_clean)
    repeated_text_list.append(repeated_text)
print(f"clean_chunk_num:{len(clean_chunk_list)}\nrepeated_text_num:{len(len(repeated_text_list))}")

>>>
the max length of chunk is 637
clean_chunk_num:2136
repeated_text_num:2136
```