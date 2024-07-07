# -*- coding: utf-8 -*- 
# @File : main.py
# @Author : zh 
# @Time : 2024/4/16 下午9:27
# @Desc : 使用sodata库获得训练数据的示例
import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor
import json
 
from tqdm import tqdm
import sodata
from sodata.text_split import BookSplitTool
from sodata.chunk_clean import ChunkCleanTool
import pandas as pd

def get_meta_information_from_book(book_text, overlap_size=100):
    """
    从小说文本中提取信息并返回GPT结果
    Args:
        book_text: 传入的是一整本书的文本
        overlap_size:

    Returns:
        head_para_list: head列表
        tail_para_list: tail列表
    """
    chunk_list_tmp, chunk_size = BookSplitTool.convert_book_to_fixed_length_chunks(book_text,chunk_size = 1024)
    chunk_text = []

    # 尽量使一本小说产生多个可利用的chunk
    if len(chunk_list_tmp) > 2:
        # 数据预处理
        chunk_list_tmp[1],repeated_list= ChunkCleanTool.clean_text(chunk_list_tmp[1])
        chunk_text.append(chunk_list_tmp[1])  # 第0个文本块往往是一些干扰信息
        idx_rand = random.randint(2, len(chunk_list_tmp) - 1)  # 从后面的文本块中随机选择另一个文本块
        # 数据预处理
        chunk_list_tmp[idx_rand],repeated_list = ChunkCleanTool.clean_text(chunk_list_tmp[idx_rand])
        chunk_text.append(chunk_list_tmp[idx_rand])
    else:
        print('chunk_list_tmp', len(chunk_list_tmp))
        return [], []

    # print("---小说原文----: \n {}".format(paragraph))
    head_para_list = []
    tail_para_list = []
    for paragraph in chunk_list_tmp:
        # ---切片---
        # idx_split_rand = random.randint(200, min(chunk_size, 1000))
        # head_text, tail_text = BookSplitTool.split_text_into_head_tail(paragraph, idx_split_rand)
        head_text, tail_text =  BookSplitTool.split_text_into_HT_by_ratio(paragraph,0.4)
        head_para_list.append(head_text)
        tail_para_list.append(tail_text)
    return head_para_list, tail_para_list


def read_jsonl_to_csv(jsonl_path: str, save_path: str, line_number: int,max_workers: int=20):
    """
    读取JSONL文件，处理得到文本chunk的head和tail存储在CSV文件中，下一步可以利用prompt获得response
    Args:
        jsonl_path:  jsonl文件路径
        save_path:  保存的csv文件路径
        line_number:  处理的jsonl文件行数
    Returns:
        None
    """
    df = pd.DataFrame(columns=['head_paragraph', 'tail_paragraph'])
    cnt_row = 0
    if os.path.isfile(jsonl_path):
        with open(jsonl_path, 'r', encoding='utf-8') as file:
            buffer = []
            for idx, line in enumerate(file):
                if idx >= line_number:  # 只读取前num_lines行
                    break
                    # line_number = file.tell()  # 获取当前行的位置（用于处理JSON解码错误时输出行号）
                json_line = json.loads(line)
                book_text = json_line['text']
                buffer.append(book_text)
                while len(buffer) == max_workers:
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        # 使用tqdm显示进度条，并调用get_meta_information_from_book函数处理每个文本
                        results = list(tqdm(executor.map(get_meta_information_from_book, buffer),
                                            total=len(buffer)))  # total=len(buffer)指定tqdm总的任务数量
                    print(results)
                    # 遍历处理结果，并将结果填充到DataFrame中
                    for book_info in results:
                        head_para, tail_para = book_info
                        cnt_row += 1
                        df.loc[cnt_row - 1] = [head_para, tail_para]

                        # 清空buffer，为下一批文本做准备
                    buffer = []
                    # 将DataFrame保存为CSV文件
                    df.to_csv(save_path, mode='w', header=True, index=None)

def convert_novel_to_chunklist(book_text,chunk_size = 512):
        chunk_list, chunk_size = BookSplitTool.convert_book_to_fixed_length_chunks(book_text,chunk_size = chunk_size)
        print(f"The fixed length of this chunk is {chunk_size}")
        return chunk_list   

def read_jsonl_to_chunklist_csv(jsonl_path: str, 
                                save_path: str, 
                                column_names: str,
                                max_workers: int = 20,
                                start_line = None,
                                end_line = None,
                                concurrent_func = convert_novel_to_chunklist):
    """
    读取JSONL文件，处理得到文本chunk存储在CSV文件中
    Args:
        jsonl_path: jsonl文件路径
        save_path: 保存的chunklist csv文件路径
        column_names: 保存的csv文件列名
        max_workers:  最大并发数
        start_line:  开始行
        end_line:  结束行
        concurrent_func: 并发函数
    Returns:
         None
    """
    df = pd.DataFrame(columns=column_names)
    if os.path.isfile(jsonl_path):
        with open(jsonl_path, 'r', encoding='utf-8') as file:
            buffer = []
            for idx, line in enumerate(file,start=1):
                if start_line is not None and idx < start_line:
                    continue
                if end_line is not None and idx > end_line:
                    break
                json_line = json.loads(line)
                book_text = json_line['text']
                buffer.append(book_text)
                if len(buffer) == max_workers or idx >= end_line:
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        # 使用tqdm显示进度条，并调用并发函数处理每个文本
                        results = list(tqdm(executor.map(concurrent_func, buffer),
                                            total=len(buffer)))  # total=len(buffer)指定tqdm总的任务数量
                     # 动态收集并发的结果，并写入 DataFrame
                    for text_chunk_col in results:
                        row_data = dict(zip(column_names, text_chunk_col))  
                        df_to_add = pd.DataFrame([row_data])
                        df = pd.concat([df, df_to_add], ignore_index=True)
                    buffer = []
                    # 将DataFrame保存为CSV文件
                    df.to_csv(save_path, mode='w', header=True, index=None) 
    return df


def read_jsonl_to_ner_csv(jsonl_path: str, save_path: str,max_workers: int= 5, start_line = None,end_line = None,):
    """
    读取JSONL文件，处理得到文本chunk的head和tail存储在CSV文件中，下一步可以利用prompt获得response
    Args:
        jsonl_path:  jsonl文件路径
        save_path:  保存的csv文件路径
        line_number:  处理的jsonl文件行数
    Returns:
        None
    """
    df = pd.DataFrame(columns=["fixed_paragraph"])
    cnt_row = 0
    if os.path.isfile(jsonl_path):
        with open(jsonl_path, 'r', encoding='utf-8') as file:
            buffer = []
            for idx, line in enumerate(file):
                if start_line is not None and idx < start_line:
                    continue
                if end_line is not None and idx > end_line:
                    break
                json_line = json.loads(line)
                book_text = json_line['text']
                buffer.append(book_text)
                if len(buffer) == max_workers or idx >= end_line:
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        # 使用tqdm显示进度条，并调用get_meta_information_from_book函数处理每个文本
                        results = list(tqdm(executor.map(convert_novel_to_chunklist, buffer),
                                            total=len(buffer)))  # total=len(buffer)指定tqdm总的任务数量   
                    # 遍历处理结果，并将结果填充到DataFrame中
                    for book_info in results:
                        fixed_paragraph = book_info
                        cnt_row += 1
                        df.loc[cnt_row - 1] = [fixed_paragraph]

                    # 清空buffer，为下一批文本做准备
                    buffer = []
                    # 将DataFrame保存为CSV文件
                    df.to_csv(save_path, mode='w', header=True, index=None)
if "__main__" == __name__:
    #设置文件路径
    start_time = time.time()
    jsonl_path = os.path.join("/home/zhanghong/model_data/data/jsonl_data","BL_无海棠.jsonl")
    save_path = os.path.join("/home/zhanghong/sodata/data/csv_data","shuf_BL_chunks_81.csv")

    column_name = ["fixed_paragraph"]
    # column_name = ["head_paragraph","tail_paragraph"]
    print('正在处理文件:' + jsonl_path)
    
    read_jsonl_to_ner_csv(jsonl_path, save_path, start_line = 81, end_line = 81)#闭区间
    print("finished!")

    end_time = time.time()
    execution_time = end_time - start_time
    hours, remainder = divmod(execution_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"程序运行时间: {hours} 小时 {minutes} 分钟 {round(seconds,1)} 秒")
            
#python main.py