import requests
import csv
import time
from lib.prompt import BANNED_PROMPT

url = 'http://127.0.0.1:8062/v1/api/trigger/imagine'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

prefix = "scifi, realistic, cinematic, hand drawing, "
suffix = " --ar 3:4"


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
with open("data_source/sea1_output.csv", "r", encoding="cp1252") as csv_file:
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
            if counter >0:
                counter -= 1

        if counter == 3 or counter == 0:
            time.sleep(300)
        else:
            time.sleep(150)



