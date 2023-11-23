import traceback

from flask import Flask, request, jsonify
import re
import requests
import csv
import time
from lib.prompt import BANNED_PROMPT
import constants

app = Flask(__name__)

url = 'http://127.0.0.1:8062/v1/api/trigger/imagine'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

book_name = constants.book_name
chapter_name = constants.chapter_number
article_en_title = f"{book_name}_{chapter_name}_en"

xian_xia_prefix2 = "4K, CG, realistic, full details, eastern aesthetics, cinematic art, "
xian_xia_prefix = "film scene, 2D, ink and oil painting, jianghu, wuxia, cinematic art, "
desert_land_prefix = "best quality, realistic, CG, full details, broken world, cinematic art, "

prefix = xian_xia_prefix
suffix = " --ar 16:9"

# 全局变量，用于缓存 CSV 文件的内容
csv_data = None

# 全局变量，用于记录当前处理的行索引
current_index = 0


def read_csv_file():
    global csv_data
    csv_file_path = f'data_source/articles_en/{book_name}/{article_en_title}.csv'

    try:
        with open(csv_file_path, "r", encoding="cp1252") as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)  # 读取第一行
            csv_data = list(csv_reader)  # 缓存 CSV 文件的内容
    except Exception as e:
        # 处理文件读取异常
        csv_data = None


def get_next_row():
    global csv_data
    global current_index

    if csv_data is None or current_index >= len(csv_data):
        read_csv_file()

    if csv_data:
        row = csv_data[current_index]
        current_index += 1
        print(f"current_index: {current_index}, total: {len(csv_data)}")
        return row
    else:
        return None


image_handler_url = 'http://0.0.0.0:4000/receive_request'


@app.route('/send_task', methods=['POST'])
def send_task():
    try:
        # sleep for a second in case of message collision
        time.sleep(1)
        row = get_next_row()
        if row:
            print("current row: ", row)
            data = {
                "prompt": prefix + str(row) + suffix
            }
            requests.post(url, headers=headers, json=data)
            return jsonify({"data": row, "message": "Request received successfully"}), 200
        else:
            return jsonify({"error": "Failed to read CSV file"}), 500
    except Exception as e:
        traceback.print_exc()  # 打印异常的堆栈信息
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)  # 替换为实际的端口号


def replace_banned(prompt: str):
    words = set(w.lower() for w in prompt.split())
    banned_words = words & BANNED_PROMPT
    backup = prompt
    if banned_words:
        for word in banned_words:
            prompt = prompt.replace(word, '')
        print(f"检测到违规词, 旧: {backup}, 新: {prompt}")
        return prompt
    return prompt
