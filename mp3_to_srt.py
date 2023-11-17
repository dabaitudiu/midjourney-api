import os
from pydub import AudioSegment
import sys
#
# sys.path.append(r"C:\Users\lzhnu\Work\ffmpeg-master-latest-win64-gpl\bin")
#
# ffmpeg_path = os.path.abspath(r"C:\Users\lzhnu\Work\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe")
# AudioSegment.converter = ffmpeg_path
# ffprobe_path = r"C:\Users\lzhnu\Work\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe"
# AudioSegment.ffprobe = ffprobe_path

def get_duration(audio_file):
    audio = AudioSegment.from_mp3(audio_file)
    return len(audio) / 1000  # 获取时长，单位为秒

def text_to_srt(text_file, output_srt_file, audio_file_path, audio_prefix):
    with open(text_file, 'r', encoding='utf-8') as text_file:
        lines = text_file.readlines()

    with open(output_srt_file, 'w', encoding='utf-8') as srt_file:
        start_time = 0  # 起始时间为零

        for idx, line in enumerate(lines, start=1):
            audio_filename = f"{audio_file_path}/{audio_prefix}_{idx}.mp3"
            duration = get_duration(audio_filename)

            # 将持续时间转换为适用于 SRT 的格式
            srt_duration = format_srt_duration(duration)

            print(f"正在处理: {line.strip()}, 时间: {srt_duration}")
            srt_file.write(f"{idx}\n")
            srt_file.write(f"{format_srt_time(start_time)} --> {format_srt_time(start_time + duration)}\n")
            srt_file.write(f"{line.strip()}\n\n")


            start_time += duration

def format_srt_duration(duration):
    # 将持续时间转换为小时、分钟、秒和毫秒
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((duration % 1) * 1000)

    # 将持续时间格式化为 0:00:00,000
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

def format_srt_time(seconds):
    # 将时间转换为小时、分钟、秒和毫秒
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)

    # 将时间格式化为 0:00:00,000
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"



tag_name = "全球废土_2"

if __name__ == "__main__":
    text_file_path = "data_source/articles/全球废土/全球废土_2_output.txt"  # 你的中文文本文件路径
    output_srt_file_path = f"data_source/srt/{tag_name}.srt"  # 输出的SRT文件路径
    audio_file_path = "data_source/results/voices/全球废土/全球废土_2"
    audio_file_prefix = "output_zh-CN-YunxiNeural"  # 语音文件的前缀

    text_to_srt(text_file_path, output_srt_file_path, audio_file_path, audio_file_prefix)
