import pandas as pd
import re

# 去除标点符号的简单函数
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def find_sentence_position(csv_file, query):
    try:
        # 读取CSV文件，跳过有问题的行
        df = pd.read_csv(csv_file, on_bad_lines='skip').fillna('')

        # 去掉输入句子中的标点符号
        query_clean = remove_punctuation(query)

        # 遍历每一行，找出匹配的诗句
        for _, row in df.iterrows():
            # 分割诗句和翻译
            content_sentences = re.split(r'[。！？]', row['content'])  # 分割古诗句
            translation_sentences = re.split(r'[。！？]', row['trans'])  # 分割翻译

            # 去除标点符号后匹配诗句
            for i, sentence in enumerate(content_sentences):
                sentence_clean = remove_punctuation(sentence.strip())

                if query_clean in sentence_clean:
                    return {
                        '诗句': sentence.strip(),  # 保留标点符号
                        '翻译': translation_sentences[i].strip() if i < len(translation_sentences) else "无对应翻译"
                    }

        return None

    except Exception as e:
        print(f"处理CSV文件时发生错误: {e}")
        return None

# 输入CSV文件路径和查询句子
csv_file = r".\poems.csv"
query = input("请输入要搜索的古诗句子: ")

# 查找结果
result = find_sentence_position(csv_file, query)

# 输出结果
if result:
    print("找到匹配的结果:")
    for key, value in result.items():
        print(f"{key}: {value}")
else:
    print("没有找到匹配的诗句。")








