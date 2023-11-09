import re
import csv

tag_name = "黜龙1"
dir_name = "data_source/"
file_name = dir_name + tag_name + ".txt"

# 读取文本文件
with open(file_name, "r", encoding="utf-8") as file:
    text = file.read()

# 定义分隔符和最低长度限制
delimiter = r"[\n.!?，、。\"'？！”“：… ‘’]"  # 可以根据需要添加更多的分隔符
min_segment_length = 40  # 最低长度限制

# 切割文本并生成句子列表
sentences = []
segments = re.split(delimiter, text)
current_segment = ""
for segment in segments:
    if len(current_segment) + len(segment) + 1 < min_segment_length:
        current_segment += segment + " "
    else:
        if current_segment:
            sentences.extend(current_segment.strip().split(". "))  # 使用句号分割句子
        current_segment = segment

# 处理剩余的文本
if current_segment:
    sentences.extend(current_segment.strip().split(". "))

# 写入CSV文件
output_filename = dir_name + tag_name + "_output.csv"
with open(output_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Sentence"])  # 写入CSV文件的列标题
    for sentence in sentences:
        if len(sentence) < 3:
            continue
        writer.writerow([sentence])

print("CSV文件已生成：" + output_filename)
