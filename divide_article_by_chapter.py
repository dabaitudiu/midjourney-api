import re
import constants

book_name = f"data_source/books/{constants.book_name}/{constants.book_name}"

# 读取原始txt文件
with open(book_name + ".txt", "r", encoding="utf-8") as f:
    content = f.read()

# 使用正则表达式匹配章节标题
chapter_pattern = re.compile(r"第(\w+)章 (\w+)")
matches = list(chapter_pattern.finditer(content))

# 初始化章节编号
chapter_number = 1
chapter_content = []

for i, match in enumerate(matches):
    # 获取章节编号和标题
    chapter_number = match.group(1)
    chapter_title = match.group(2)

    # 找到章节的起始位置和结束位置
    start = match.end()
    end = matches[i + 1].start() if i < len(matches) - 1 else None

    # 提取章节内容
    chapter_content = content[start:end].strip()

    # 将章节内容保存为一个新的txt文件
    filename = f"{book_name}_{i}.txt"
    with open(filename, "w", encoding="utf-8") as chapter_file:
        chapter_file.write(f"第{i}章 {chapter_title}\n{chapter_content}")
