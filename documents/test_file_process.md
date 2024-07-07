
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
