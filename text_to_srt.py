def generate_srt(text_content, srt_file):
    srt = ""
    start_time = 0
    end_time = 5  # 初始结束时间为5秒

    with open(text_content, "r", encoding="utf-8") as file:
        lines = file.readlines()

    counter = 1

    for line in lines:
        line = line.strip()
        if line:
            srt += str(counter) + "\n"
            srt += format_time(start_time) + " --> " + format_time(end_time) + "\n"
            srt += line + "\n\n"

            start_time = end_time

            end_time += int(len(line) * 0.7)  # 每个字幕间隔5秒
            counter += 1

    with open(srt_file, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt)


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},000"


text_file = "data_source/books/全球废土/全球废土_1.txt"  # 替换为你的输入文本文件
output_srt_file = "data_source/srt/全球废土_1.srt"  # 替换为你想要生成的SRT文件名

generate_srt(text_file, output_srt_file)






