# 项目目的

将txt格式的小说文本以固定的长度切分成训练样本，即：text -> list(chunks)

` 安装： pip install sodata `
## 一、功能模块
该模块主要为三个功能：数据清洗、文本切分，文件处理
### 1.数据清洗
数据清洗模块的主要功能是：对小说文本中进行清洗，删除其无效数据，过滤得到纯文本；
数据清洗模块分为：固定清洗规则（clean_rule.py）、整文本清洗模块（text_clean.py）和文本块清洗模块 (chunk_clean.py)
1. 固定清洗规则 （clean_rule.py）
> * split_pattern    #不影响语义分割文本的正则表达式
> * rules   #特定小说数据清洗替换规则
2. 文本块清洗模块  (chunk_clean.py)

**class: ChunkCleanTool** ：文本chunk的清洗
> - [ ] remove_duplicates_exact: 精确匹配去重：对于段落列表中一模一样的段落进行去重
> - [ ] remove_duplicates_minhash: MinHash去重：对于段落列表中相似性较大的段落进行去重
> - [ ] clean_text：对于小说文本片段进行数据清洗
3. 整文本清洗模块（text_clean.py）
class: TextCleanTool ：文本chunk的清洗
> - [ ] cascade_deduplication: 级联去重：对于任意一段小说进行精确匹配去重和MinHash去重


### 2.文本切分
文本切分(text_split.py) 是为了切分出不影响语义的且近固定长度的训练样本（文本chunk）

**class：ChineseRecursiveTextSplitter**：该类继承于RecursiveCharacterTextSplitter，用于中文文本的递归切分
> - [ ] _split_text_with_regex_from_end：根据给定的分隔符（separator）将文本（text）分割成多个部分
> - [ ] _split_text：分割文本并返回分割后的文本块

**Class: BookSplitTool :该类用于切分小说**
> - [ ] split_text_into_head_tail: 将一个文本块按照tail_length分割成head和tail
> - [ ] custom_sampling: 从三个区间中随机抽样
> - [ ] convert_book_to_chunks: 将小说切成随机长度的chunk
> - [ ] convert_chunk_to_head_tail_seg: 将chunk切分成两段，切分的位置在min_idx与max_idx之间
> - [ ] convert_chunk_to_segments: 将一个chunk切分成若干segments
> - [ ] convert_book_into_segment: 将一整本书切分成若干segment
### 3.文件处理
文件处理模块（file_process.py）主要是对整个流程中的文件读取、重构、保存等

**class：FileProcessTool**
> - [ ] count_lines: 计算文件行数。
> - [ ] process_txt_file:尝试使用不同的编码读取和转换文本文件。
> - [ ] save_to_jsonl:将文本数据保存为JSON Lines格式。
> - [ ] process_folder_and_save_to_jsonl:遍历处理文件夹中的小说txt文件，将数据保存为一整个JSONL文件。

### 4.文本处理（待补充）
文本处理模块的主要功能是处理小说文本，生成对应的章节目录列表