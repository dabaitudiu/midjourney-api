import re
import csv


def split_text(content_text):
    # 使用正则表达式划分句子，考虑省略号的情况
    sentences = re.split(r'(?<=[.!?])\s+', content_text)

    # 初始化结果列表
    inner_result = []

    for sentence in sentences:
        # 去除首尾空格
        sentence = sentence.strip()
        # 检查句子长度以及是否包含省略号
        if sentence and len(sentence.split()) >= 10 and "..." not in sentence:
            inner_result.append(sentence)

    return inner_result


tag_name = "sea2"
dir_name = "data_source/"
file_name = dir_name + tag_name + ".txt"

# 从文本文件中读取内容
with open(file_name, 'r') as file:
    text = file.read()

# 调用函数进行切割
result = split_text(text)

# 将句子写入CSV文件
output_filename = dir_name + tag_name + "_output.csv"
with open(output_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(result)

print("CSV文件已生成:" + output_filename)