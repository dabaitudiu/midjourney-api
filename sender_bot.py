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

xian_xia_prefix2 = "4K, CG, realistic, Chinese aesthetics, jianghu, wuxia, cinematic art, "
xian_xia_prefix = "2d game art, ink and watercolor painting, comics style, Zen, eastern aesthetics, cinematic art, "
desert_land_prefix = "best quality, realistic, CG, full details, broken world, cinematic art, "

prefix = xian_xia_prefix2
suffix = " --ar 3:4"

@app.route('/send_task', methods=['POST'])
def receive_request():
    try:
        data = request.get_json()  # 获取POST请求的JSON数据
            return jsonify({"message": "Request received successfully"}), 200
        else:
            return jsonify({"error": "Invalid JSON data in the request"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


# 读取生成的CSV文件
with open(f'data_source/articles_en/{book_name}/{article_en_title}.csv', "r", encoding="cp1252") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # 跳过第一行，即列标题
    counter = 0
    for row in reader:
        sentence = row[0]
        sentence = replace_banned(sentence)
        data = {
            "prompt": prefix + sentence + suffix
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"请求成功，prompt 值为: {sentence}")
            print("响应内容:")
            print(response.text)
        else:
            print(f"请求失败，prompt 值为: {sentence}")
            print(f"状态码: {response.status_code}")
            print("响应内容:")
            print(response.text)

        if counter < 3:
            counter += 1
        else:
            if counter > 0:
                counter -= 1

        if counter == 3 or counter == 0:
            time.sleep(120)
        else:
            time.sleep(60)


