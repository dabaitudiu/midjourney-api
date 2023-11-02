import csv
import datetime
import re
from flask import Flask, request, jsonify
import requests

from cut_image import cut_and_save_image

app = Flask(__name__)

# 用于存储状态信息的字典，初始状态都设置为False
status_dict = {}

prefixTail = "art,"
suffixHead = "--ar"


@app.route('/receive_request', methods=['POST'])
def receive_request():
    try:
        data = request.get_json()  # 获取POST请求的JSON数据
        if data is not None:
            trigger_id = data['trigger_id']
            match = re.search(r'\((\d+%)', data['content'])
            if match:
                percent = match.group(1)
                print(f'{trigger_id} Progress: {percent}')
            else:
                print("Received Request")
            if data['type'] == 'end':
                print("trigger_id: ", trigger_id)
                print("url: ", data['attachments'][0]['url'])
                print("content: ", data['content'])

                current_datetime = datetime.datetime.now()
                ctime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

                download_and_save_image(data['attachments'][0]['url'], ctime)
                update_csv(trigger_id, data['content'], ctime)
            return jsonify({"message": "Request received successfully"}), 200
        else:
            return jsonify({"error": "Invalid JSON data in the request"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def download_and_save_image(url, ctime):
    try:
        img_response = requests.get(url)
        image_data = img_response.content
        filename = "data_source/images/" + ctime + ".png"
        with open(filename, 'wb') as image_file:
            image_file.write(image_data)
        cut_and_save_image(ctime)
        # 更新状态为True
        status_dict[ctime] = True
    except Exception as e:
        print(f"Error downloading and saving image for ctime {ctime}: {str(e)}")


def update_csv(trigger_id, content, ctime):
    try:
        with open("data_source/data.csv", mode='a', newline='') as csv_file:
            fieldnames = ['ctime', 'trigger_id', 'content', 'status']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # 如果CSV文件不存在，写入表头
            if csv_file.tell() == 0:
                writer.writeheader()

            # 使用字符串方法找到 '>' 和 '--ar' 的位置
            start_index = content.find(prefixTail)
            end_index = content.find(suffixHead)

            # 提取 '>' 之后和 '--ar' 之前的内容
            if start_index != -1 and end_index != -1:
                content = content[start_index + 1:end_index].strip()

            # 写入一行数据
            writer.writerow(
                {'ctime': ctime, 'trigger_id': trigger_id, 'content': content, 'status': status_dict.get(ctime, False)})
    except Exception as e:
        print(f"Error updating CSV for trigger_id {trigger_id}: {str(e)}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880)  # 启动服务器，监听所有网络接口，端口号为 8080
