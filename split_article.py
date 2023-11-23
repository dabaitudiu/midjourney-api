import re
import csv

main_name = "仙道求索"
suffix_name = "_第1章"
tag_name = main_name + suffix_name
dir_name = "data_source/books/" + main_name + "/"
output_dir_name = "data_source/articles/" + main_name + "/"
file_name = dir_name + tag_name + ".txt"

# 读取文本文件
with open(file_name, "r", encoding="utf-8") as file:
    text = file.read()

# 定义分隔符和最低长度限制
delimiter = r"([\n.!?’,，。‘…—！？])"  # 可以根据需要添加更多的分隔符
min_segment_length = 30  # 最低长度限制

# 切割文本并生成句子列表
sentences = []
segments = re.split(delimiter, text)
current_segment = ""
for i in range(0, len(segments), 2):  # 每两个元素一组，第一个元素是文本段，第二个元素是分隔符
    segment = segments[i]

    delimiter = segments[i + 1] if i + 1 < len(segments) else ""  # 获取分隔符
    # print(segment, delimiter)
    if delimiter != '\n':
        current_segment += segment + delimiter

    if len(current_segment) < min_segment_length:
        continue

    sentences.extend(current_segment.split(". "))  # 使用句号分割句子
    current_segment = ""

# 处理剩余的文本
if current_segment:
    sentences.extend(current_segment.strip().split(". "))

output_filename = output_dir_name + tag_name + "_output.txt"
with open(output_filename, "w", encoding="utf-8") as txt_file:
    txt_file.write("Sentence\n")  # 写入文本文件的标题
    for sentence in sentences:
        if len(sentence) < 3:
            print(sentence + " length < 3")
            continue
        print(f"check sentence, length: {len(sentence)}, sentence: {sentence}")
        txt_file.write(sentence + "\n")

print(f'CSV文件已生成：{output_filename}')
