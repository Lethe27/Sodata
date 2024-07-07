# -*- coding: utf-8 -*-
# @File : file_process.py
# @Author : zh
# @Time : 2024/4/9 15:38
# @Desc : 数据处理过程中涉及到的文件操作
import json
import os
import ast
import random
import jsonlines
import pandas as pd

from sodata.chunk_clean import TextAICleanTool
from sodata.text_split import BookSplitTool
class FileProcessTool:

    def __init__(self) -> None:
        pass

    @staticmethod
    def count_lines(file_path: str) -> int:
        """
        计算文件行数
        Args:
            file_path: 文件路径
        Returns:
            lines_num: 行数
        """
        lines_num = 0
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(2 ** 20)
                if not data:
                    break
                lines_num += data.count(b'\n')
        return lines_num

    @staticmethod
    def read_jsonl_file(file_path, start_line=None, end_line=None):
        """
        读取JSONL文件内容并打印
        Args:
            file_path (str): JSONL文件路径
            start_line (int): 起始行数，默认为None，表示从文件开头开始
            end_line (int): 结束行数，默认为None，表示读取至文件结尾
        Returns:
            None
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if start_line is not None and line_number < start_line:
                    continue
                if end_line is not None and line_number > end_line:
                    break

                try:
                    # 解析每一行的JSON对象
                    obj = json.loads(line.strip())
                    print(f"Line {line_number}: {obj}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line {line_number}: {e}")
                    continue
    @staticmethod
    def process_txt_file(filepath: str,
                         encodings: list[str] = ['utf-8', 'gb18030', 'gbk', 'gb2312', 'latin-1', 'ascii']) -> str:
        """
        尝试使用不同的编码读取和转换文本文件。
        Args:
            filepath: 待处理的txt文件路径
            encodings: 尝试的编码列表
        Returns:
            content:返回处理后的文本数据
        """
        content = None
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    content = file.read()
                # 成功读取后转换编码到utf-8（如果已经是utf-8则不需要转换）
                return content.encode('utf-8').decode('utf-8')
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(f"Failed to decode {filepath} with given encodings.")

    @staticmethod
    def save_to_jsonl(text_data: str, output_file: str) -> None:
        """
        将文本数据保存为JSON Lines格式。
        Args:
            text_data: 待保存的整本小说文本数据
            output_file: 输出文件路径
        Returns:
        """
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(json.dumps({"text": text_data}, ensure_ascii=False) + '\n')
        print(f"save to {output_file}!!!")
    
    @staticmethod
    def save_labels_to_json(label_list: list[str], output_file: str) -> None:
        """
        将label保存为JSON Lines格式-->作为ner的label文件。
        Args:
            label_list: 定义的label实体列表
            output_file: 输出文件路径
        Returns:
        """
        label = {"O": 0}  
        current_index = 1  
        for entity in label_list:  
            label[f"B-{entity}"] = current_index  
            current_index += 1  
            label[f"I-{entity}"] = current_index  
            current_index += 1  
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(label, ensure_ascii=False))
        print(f"save to {output_file}!!!")
        
    @staticmethod
    def process_folder_and_save_to_jsonl(txt_folder_path: str, output_file: str) -> None:
        """
        递归遍历文件夹，处理每个txt文件，然后将数据保存为一整个JSONL格式。
        Args:
            txt_folder_path:  待转换的txt文本路径
            output_file:  输出文件路径
        Returns:
        """
        for root, dirs, files in os.walk(txt_folder_path):
            for file in files:
                if file.endswith('.txt'):
                    filepath = os.path.join(root, file)
                    try:
                        text_data = FileProcessTool.process_txt_file(filepath)
                        FileProcessTool.save_to_jsonl(text_data, output_file)
                        print(f"Processed and saved {file} successfully.")
                    except UnicodeDecodeError as e:
                        print(e)
        print("finished!!")
    
    @staticmethod  
    def processed_rows(input_file, output_file):
        """
        处理CSV文件，将每个文本的chunk列表元素拆分成单个元素占一列
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
        Returns:
            None
        """
        rows = []
        df = pd.read_csv(input_file, header=0)

        for index, row in df.iterrows():
            for col in df.columns:
                # 将字符串转换为列表
                df.at[index, col] = ast.literal_eval(row.loc[col])
            for i in range(len(row.iloc[0])):
                # 通过位置索引来获取每个列表的元素
                row_data = {col: row[col][i] for col in df.columns}
                rows.append(row_data)

        data = pd.DataFrame(rows)
        data.to_csv(output_file, index=False)

        # 记录原始行数和拆分后行数
        original_rows = df.shape[0]
        split_rows = data.shape[0]
        print(f"原始行数: {original_rows}, 拆分后行数: {split_rows}")
    
    @staticmethod 
    def convert_chunkCSV_to_bioJSONL(input_file, output_file_folder, limit_size=10):
        """
        将含有切分后chunk的CSV文件转换为BIO标注后chunk的JSONL文件
        Args:
            input_file: 输入文件路径
            output_file_folder: 输出文件夹路径
            limit_size: bio标注的文本chunk限制长度
        Returns:
            None
        """
        data = pd.read_csv(input_file, header=0)
        chars_list = []
        tags_list = []
        for index, row in data.iterrows():
            fixed_text_chunk = str(row["fixed_paragraph"])


            if len(fixed_text_chunk) > limit_size:
                chars_output, tags_output = TextAICleanTool.get_bio_chunk(fixed_text_chunk)
                chars_list.append(chars_output)
                tags_list.append(tags_output)


        _, file_name = os.path.split(input_file)
        file_prefix, _ = os.path.splitext(file_name)

        # 将 bio_head_list 写入 JSONL 文件
        for i in range(len(chars_list)):
            text_data = chars_list[i]
            label_data = tags_list[i]
            mode = 'w' if i == 0 else 'a'  # 如果是第一次迭代，使用 'w' 模式，否则使用 'a' 模式
            with open(os.path.join(output_file_folder, file_prefix + '_Bio.jsonl'), mode=mode,
                        encoding='utf-8') as file:
                file.write(json.dumps({"text_chunk": text_data, "label": label_data}, ensure_ascii=False,
                                        separators=(',', ': ')) + '\n')
        print("-" * 20 + f"fixed_text_chunk已写入{file_prefix + '_Bio.jsonl'}" + "-" * 20)

    @staticmethod 
    def read_data_and_shuffle(input_file_path, random_state=42):
            """
                读取JSONL/CSV/TSV数据集并打乱数据
            Args:
                input_file_path:  文件路径
                random_state:  随机种子
            Returns:
                    shuffled_data: 打乱后的数据集
            """
            _, file_extension = os.path.splitext(input_file_path)
            if file_extension == '.jsonl':
                data = []
                with jsonlines.open(input_file_path, 'r') as reader:
                    for obj in reader:
                        data.append(obj)
                random.seed(random_state)
                random.shuffle(data)
                return data
            elif file_extension in ['.csv', '.tsv']:
                separator = '\t' if file_extension == '.tsv' else ','
                data = pd.read_csv(input_file_path, sep=separator)
                shuffled_data = data.sample(frac=1, random_state=random_state)
                return shuffled_data
            else:
                raise ValueError("Unsupported file format. Only JSONL, CSV, and TSV are supported.")
    @staticmethod
    def collect_error_pattern(pattern_file ,limit_size :int = 3):
        """
        从pattern文件中收集错误模式
        Args:
            pattern_file:  pattern文件路径
            limit_size:  出现次数
        Returns:
             add_pattern:采集到的错误模式列表
        """
        data=pd.read_csv(pattern_file,header=0)
        add_pattern = []
        for index, row in data.iterrows():
            if row["Count"]>limit_size:
                add_pattern.append(row["Error Key"])
        return add_pattern
    @staticmethod   
    def split_bioJSONL(input_file_path, output_path, p1: float, p2: float, random_state: int = 42):
    
        """
        将数据集切分为训练集、测试集和开发集
        Args:
            input_file_path: 原始文件路径
            output_path: 输出文件夹路径
            p1: 训练集占比
            p2: 测试集占比
            random_state: 随机种子
        Returns:
            None
        """
        # 读取数据
        data = FileProcessTool.read_data(input_file_path)

        # 计算每个部分的样本数
        total_samples = len(data)
        train_samples = int(total_samples * p1)
        test_samples = int(total_samples * p2)
        dev_samples = total_samples - train_samples - test_samples

        # 切分数据集
        train_data = data[:train_samples]
        test_data = data[train_samples:train_samples + test_samples]
        dev_data = data[train_samples + test_samples:]

        # 确保剩余的样本数量与预期的 dev 样本数量一致
        assert len(dev_data) == dev_samples

        # 保存切分后的数据集

        _, file_name = os.path.split(input_file_path)
        file_prefix, file_suffix = os.path.splitext(file_name)

        train_output_path = os.path.join(output_path, f"{file_prefix}_train{file_suffix}")
        test_output_path = os.path.join(output_path, f"{file_prefix}_test{file_suffix}")
        dev_output_path = os.path.join(output_path, f"{file_prefix}_dev{file_suffix}")

        if file_suffix == '.jsonl':
            with jsonlines.open(train_output_path, 'w') as writer:
                writer.write_all(train_data)
            with jsonlines.open(test_output_path, 'w') as writer:
                writer.write_all(test_data)
            with jsonlines.open(dev_output_path, 'w') as writer:
                writer.write_all(dev_data)
        elif file_suffix in ['.csv', '.tsv']:
            train_data.to_csv(train_output_path, index=False)
            test_data.to_csv(test_output_path, index=False)
            dev_data.to_csv(dev_output_path, index=False)

        print("已经成功切分数据集！！！")
        print(f"Train set size: {len(train_data)}")
        print(f"Test set size: {len(test_data)}")
        print(f"Dev set size: {len(dev_data)}")

    def convert_novel_to_chunklist(book_text,chunk_size = 512):
        chunk_list, chunk_size = BookSplitTool.convert_book_to_fixed_length_chunks(book_text,chunk_size = chunk_size)
        print(f"The fixed length of this chunk is {chunk_size}")
        return chunk_list   
    @staticmethod 
    def read_novelJSONL_to_chunklist_csv(jsonl_path: str, save_path: str, line_number: int, column_names: str, max_workers: int = 20, concurrent_func = convert_novel_to_chunklist):
        """
        读取JSONL文件，处理得到文本chunk的head和tail存储在CSV文件中，下一步可以利用prompt获得response
        Args:
            jsonl_path:  jsonl文件路径,{"text":"……整个文本……"}
            save_path:  保存的chunklist csv文件路径
            line_number:  处理的jsonl文件行数
            column_name:  保存的csv文件列名
            max_workers:  最大并发数
            concurrent_func:  并发函数,是需要用于切分chunk的函数，返回值是chunk_list,具体怎么切分需要重新构造
        Returns:
            df: 保存的DataFrame
        """
        df = pd.DataFrame(columns= column_names)
        if os.path.isfile(jsonl_path):
            with open(jsonl_path, 'r', encoding='utf-8') as file:
                buffer = []
                for idx, line in enumerate(file):
                    if idx >= line_number:  # 只读取前num_lines行
                        break
                    json_line = json.loads(line)
                    book_text = json_line['text']
                    buffer.append(book_text)
                    from concurrent.futures import ThreadPoolExecutor
                    from tqdm import tqdm
                    if len(buffer) == max_workers or idx == line_number - 1:
                        with ThreadPoolExecutor(max_workers=max_workers) as executor:
                            # 使用tqdm显示进度条，并调用并发函数处理每个文本
                            results = list(tqdm(executor.map(concurrent_func, buffer),
                                                total=len(buffer))) 
                        # 动态收集并发的结果，并写入 DataFrame
                        for text_chunk_col in results:

                            row_data = dict(zip(column_names, text_chunk_col))  
                            df_to_add = pd.DataFrame([row_data])
                            df = pd.concat([df, df_to_add], ignore_index=True)
                        
                        # 清空buffer，为下一批文本做准备
                        buffer = []
                        # 将DataFrame保存为CSV文件
                        df.to_csv(save_path, mode='w', header=True, index=None)

        return df

