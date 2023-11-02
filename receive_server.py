from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/receive_request', methods=['POST'])
def receive_request():
    try:
        data = request.get_json()  # 获取POST请求的JSON数据
        if data is not None:
            print("Received Request")
            if data['type'] == 'end':
                print("trigger_id: ", data['trigger_id'])
                print("url: ", data['attachments'][0]['url'])
                print("content: ", data['content'])
                img_response = requests.get(data['attachments'][0]['url'])
                image_data = img_response.content
                # 指定保存图像的文件名
                filename = "data_source/images/"+data['trigger_id'] + ".png"
                # 使用urllib库保存图像
                with open(filename, 'wb') as image_file:
                    image_file.write(image_data)
            return jsonify({"message": "Request received successfully"}), 200
        else:
            return jsonify({"error": "Invalid JSON data in the request"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880)  # 启动服务器，监听所有网络接口，端口号为 8080
