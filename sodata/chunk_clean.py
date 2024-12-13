# -*- coding: utf-8 -*- 
# @File : chunk_clean.py.py
# @Author : zh 
# @Time : 2024/4/15 上午11:38
# @Desc : 清除单个文本片段的无效数据
import re
import regex 
import jionlp
from datasketch import MinHash, MinHashLSH
from sodata.clean_rule import rules, PATTERNS


class ChunkCleanTool:
    """
    该类用于小说片段（chunk）的数据清洗
    注意是不能清洗整本小说，否则会有过度清洗的问题
    """
    rules = rules

    def __init__(self) -> None:
        pass

    @staticmethod
    def remove_duplicates_exact(paragraphs: list[str]):
        """
        精确匹配去重：对于段落列表中一模一样的段落进行去重
        args:
            paragraphs: 段落列表
        return:
            unique_paragraphs: 不含重复段落的段落列表
            repeated_text: 重复文本列表
        """
        unique_set = set()
        unique_paragraphs = []
        repeated_text = []
        for p in paragraphs:
            if p in unique_set:
                repeated_text.append(p)
                continue
            unique_set.add(p)
            unique_paragraphs.append(p)
        return unique_paragraphs, repeated_text

    @staticmethod
    def remove_duplicates_minhash(paragraphs: list[str], num_perm: int = 128):
        """
        MinHash去重：对于段落列表中相似性较大的段落进行去重
        args:
            paragraphs: 段落列表
            num_perm: 相似度参数，用于生成MinHash的排列数，较大的 num_perm 值会提高准确性，但也会增加计算成本
        return:
            unique_paragraphs: 不含重复段落的段落列表
            ordered_repeated:重复文本列表
        """
        lsh = MinHashLSH(threshold=0.5, num_perm=num_perm)
        minhashes = {}

        for i, p in enumerate(paragraphs):
            m = MinHash(num_perm=num_perm)
            for d in p:
                m.update(d.encode('utf8'))
            lsh.insert(f"p{i}", m)
            minhashes[f"p{i}"] = m

        unique_keys = set()
        ordered_unique_keys = []  # 用于保持原始顺序的唯一键列表
        ordered_repeated = []
        for i, p in enumerate(paragraphs):
            key = f"p{i}"
            if key in unique_keys:
                # x = []
                # x.append(paragraphs[key], paragraphs[i])
                ordered_repeated.append(paragraphs[i])
                continue
            duplicates = lsh.query(minhashes[key])
            unique_keys.update(duplicates)
            ordered_unique_keys.append(key)  # 仅当键是唯一的时候才添加

        # 使用有序的唯一键列表来生成最终的唯一段落列表
        unique_indices = [int(k[1:]) for k in ordered_unique_keys]
        unique_paragraphs = [paragraphs[i] for i in sorted(unique_indices)]  # 根据索引排序以保持原始顺序
        return unique_paragraphs, ordered_repeated
        # 级联去重过程：输入为原始小说文本text
    @staticmethod
    def cascade_deduplication(text_dirty: str):
        """
        对于任意一段小说进行精确匹配去重和MinHash模糊去重
        args:
            text_dirty: 小说段落
        return:
            text_clean: 去重后的小说段落
           repeated_text: 重复文本列表
        """
        # 以一行为单位处理
        paragraphs = text_dirty.split('\n')
        # Step 1: 精确匹配去重
        unique_paragraphs, repeated_text = ChunkCleanTool.remove_duplicates_exact(paragraphs)
        # Step 2: MinHash去重
        unique_paragraphs, repeated_text = ChunkCleanTool.remove_duplicates_minhash(unique_paragraphs)

        text_clean = '\n'.join(unique_paragraphs)
        return text_clean, repeated_text
    
    @staticmethod
    def clean_text(chunk: str):
        """
        对于小说文本片段进行数据清洗
        args:
            chunk: 小说文本片段
        return:
            chunk: 清洗后的小说文本
            ordered_repeated:重复文本列表
        """
        raw_text = chunk
        # 应用替换规则
        for pattern, replacement in rules:
            # dirty_text_list.extend(re.findall(pattern, text))
            chunk = regex.sub(pattern, replacement, chunk)

            # 通用清洗
        chunk = jionlp.clean_text(chunk, remove_parentheses=False, delete_prefix=True)
        chunk, ordered_repeated = ChunkCleanTool.cascade_deduplication(chunk)
        # dirty_text_list.append(ordered_repeated)
        if "@" in chunk or "^" in chunk or "PS：" in chunk or "更新时间" in chunk or "回复时间" in chunk or "回复日期" in chunk or (
                "《" in chunk and "》" in chunk):
            return '',[]
        return chunk,ordered_repeated



class TextAICleanTool:
    def __init__(self) -> None:
        pass


    @staticmethod
    def bio_tagging(text, entities):
        """
        使用BIO标注自定义实体
        Args:
            text: 待标注文本
            entities: 实体列表，每个元素为(start_index, end_index, entity_type)
        Returns:
            tag: 标注结果列表，存储每个元素的标注结果
        """
        tags = ['O'] * len(text)  # 初始化标签列表，全部标记为'O'
        for start, end, entity_type in entities:
            tags[start] = 'B-' + entity_type  # 实体开始位置标记为'B-'
            for i in range(start + 1, end):
                tags[i] = 'I-' + entity_type  # 实体内部位置标记为'I-'
        return tags


    @staticmethod
    def find_entities(text):
        """
        使用正则表达式查找实体
        Args:
            text: 待标注文本
        Returns:
            entities: 实体列表，每个元素为(start_index, end_index, entity_type)
        """
        entities = []
        for entity_type, pattern_list in PATTERNS.items():
            for pattern, _ in pattern_list:  # 提取了正则表达式对象
                for match in regex.finditer(pattern, text):
                    # 添加(start_index, end_index, entity_type)到实体列表中,end_index是匹配pattern的下一个索引
                    entities.append((match.start(), match.end(), entity_type))
        return entities

    @staticmethod
    def get_bio_chunk(text_chunk):
        """
        对单个文本块进行实体识别，并返回BIO标注结果
        Args:
            text_chunk: 切分后的单个文本块
        Returns:
            chars_output: 用于写入文件的文本块
            tags_output: BIO标注后的文本块
        """
        entities_found = TextAICleanTool.find_entities(text_chunk)  # 查找测试文本中的实体
        bio_tags = TextAICleanTool.bio_tagging(text_chunk, entities_found)  # 对测试文本进行BIO标注
        chars_output = ""
        # 遍历字符串除了最后一个字符的所有字符
        for i in range(len(text_chunk) - 1):
            if text_chunk[i] == ' ':  # 只判断是否为空格字符
                chars_output += text_chunk[i]
            else:
                chars_output += text_chunk[i] + " " 
        chars_output += text_chunk[-1]

        tags_output = ' '.join(bio_tags)
        return chars_output,tags_output
    