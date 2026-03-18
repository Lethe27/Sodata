
### process_folder_and_save_to_jsonl
```angular2html
#1.测试process_folder_and_save_to_jsonl--小说文本转换成jsonl格式
FileProcessTool.process_folder_and_save_to_jsonl('/home/zhanghong/sodata/data/BL',  '/home/zhanghong/sodata/data/json_data/BL.jsonl')

>>>
Processed and saved 《锦瑟》作者：priest.txt successfully.
Processed and saved 《默读》作者：priest.txt successfully.
Processed and saved 《杀破狼》作者：priest.txt successfully.
Processed and saved 《残次品》作者：priest.txt successfully.
Processed and saved 《山河表里》作者：priest.txt successfully.
Processed and saved 《六爻》作者：priest.txt successfully.
Processed and saved 《镇魂》作者：priest.txt successfully.
Processed and saved 《烈火浇愁》作者：priest.txt successfully.
Processed and saved 《过门》作者：priest.txt successfully.
Processed and saved 《大哥》作者：priest.txt successfully.
Processed and saved 墨香铜臭《重生之人渣反派自救系统》.txt successfully.
Processed and saved 《魔道祖师》（精校版全本 番外完）作者：墨香铜臭.txt successfully.
Processed and saved 《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt successfully.
finished!!
```
### count_lines
```angular2html
#2.测试count_lines--计算文件行数
print(FileProcessTool.count_lines('/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'))

>>> 22156
```
### process_txt_file & save_to_jsonl
```
#3.测试process_txt_file--以多种编码读取txt文件 
#save_to_jsonl--保存jsonl格式文件
input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
output_path = "/home/zhanghong/sodata/data/json_data/《天官赐福》.jsonL"
text_data = FileProcessTool.process_txt_file(input_path)
FileProcessTool.save_to_jsonl(text_data, output_path)

>>> save to /home/zhanghong/sodata/data/json_data/《天官赐福》.jsonL!!!
```
### save_labels_to_jsonl
```
#4.测试save_labels_to_jsonl--保存label数据至jsonl文件,用于序列标注模型
label = ["INV_CHAR","INV_SEG","INV_TITLE"]
output_path = "/home/zhanghong/sodata/data/jsonl_data/label.jsonL"
FileProcessTool.save_labels_to_json(label, output_path)

>>> save to /home/zhanghong/sodata/data/jsonl_data/label.jsonl!!!
```
### process_folder_and_save_to_jsonl
```
#5.测试process_folder_and_save_to_jsonl--递归遍历文件夹，处理每个txt文件，然后将数据保存为一整个JSONL格式
input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
output_path = "/home/zhanghong/sodata/data/json_data/《天官赐福》.jsonl"
FileProcessTool.process_folder_and_save_to_jsonl(input_path, output_path)
>>>
Processed and saved 墨香铜臭《重生之人渣反派自救系统》.txt successfully.
Processed and saved 《魔道祖师》（精校版全本 番外完）作者：墨香铜臭.txt successfully.
Processed and saved 《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt successfully.
finished!!
```
### process_rows
```
# #6.测试processed_rows--处理CSV文件，将每个文本的chunk列表元素拆分成单个元素占一列
input_path = os.path.join("/home/zhanghong/sodata/data/csv_data", "shuf_BL_chunks_36-75.csv")
output_path = os.path.join("/home/zhanghong/sodata/data/csv_data", "shuf_BL_chunks_36-75_split.csv")
FileProcessTool.processed_rows(input_path, output_path)

>>>原始行数: 40, 拆分后行数: 8757
```
### convert_chunkCSV_to_bioJSON
```
# #7.测试convert_chunkCSV_to_bioJSON--将含有切分后chunk的CSV文件转换为BIO标注后chunk的JSON文件
input_file = os.path.join("/home/zhanghong/sodata/data/csv_data", "shuf_BL_chunks_81.csv")
output_file_folder = "/home/zhanghong/sodata/data/jsonl_data"
FileProcessTool.convert_chunkCSV_to_bioJSONL(input_file, output_file_folder)

>>>
--------------------fixed_text_chunk已写入shuf_BL_chunks_81_Bio.jsonl--------------------
```
### split_bioJSONL
```
# #8.测试split_bioJSONL--将数据集切分为训练集、测试集和开发集
input_file_path = "/home/zhanghong/sodata/data/jsonl_data/origin_chunks_50_bio.jsonl"
output_path = "/home/zhanghong/sodata/data/jsonl_data"
FileProcessTool.split_bioJSONL(input_file_path, output_path, 0.78, 0.15)
>>>
已经成功切分数据集！！！
Train set size: 39
Test set size: 7
Dev set size: 4
```
