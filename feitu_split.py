split_limit = 50

def split_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    output_lines = []
    current_line = lines[0].strip()

    for line in lines[1:]:
        line = line.strip()
        if len(current_line) + len(line) > 50:
            output_lines.append(current_line)
            current_line = line
        else:
            current_line += ' ' + line

    # 处理最后一行
    output_lines.append(current_line)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(output_lines))


if __name__ == "__main__":
    input_file = "data_source/books/全球废土/全球废土_2.txt"  # 你的输入文件
    output_file = "data_source/articles/全球废土/全球废土_2_output.txt"  # 输出文件

    split_text(input_file, output_file)
