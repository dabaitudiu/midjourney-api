import json
import os
import requests
import time
from xml.etree import ElementTree
import __init__

# 你注册申请的微软tts的api——key
subscription_key = os.getenv("TTS_KEY")


class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.tts = "你是最棒的哦，哇哈哈哈"
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self, data, child_path, voices, index):
        base_url = 'https://eastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'TTSForPython'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
        voice.set(' rate ', '1.1')
        voice.text = data

        for j in range(len(voices)):
            print("current voice: ", voices[j])
            voice.set('name', voices[j])
            body = ElementTree.tostring(xml_body)
            response = requests.post(constructed_url, headers=headers, data=body)
            if response.status_code == 200:
                with open(child_path + voices[j] + "_" + index + '.mp3', 'wb') as audio:
                    audio.write(response.content)
                    print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
            else:
                print("\nStatus code: " + str(
                    response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
                print("Reason: " + str(response.reason) + "\n")

        # voice.set('name', 'zh-CN-YunxiNeural')


    def get_voices_list(self):
        base_url = 'https://eastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nGet Voices List Success \n")
        else:
            print("\nStatus code: " + str(
                response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
        return response.text


# def load_source_data_text(path):
#     app = TextToSpeech(subscription_key)
#     app.get_token()
#     df_temp = pd.read_csv(path)
#     for index, row in df_temp.iterrows():
#         new_path = path.split(".csv")[0].replace("data_split","data_audio")
#         if not os.path.exists(new_path):
#             os.makedirs(new_path)
#         path_child =os.path.join(new_path,str(index))
#         app.save_audio(row['text'],path_child)
#     return new_path
#
#
# if __name__ == "__main__":
#     load_source_data_text("data/data_split/智慧公园/story_2.csv")

article_path = "data_source/articles/全球废土/全球废土_2_output.txt"

if __name__ == "__main__":
    app = TextToSpeech(subscription_key)
    app.get_token()
    # text = app.get_voices_list()
    # 将JSON文本解析为Python字典
    # data = json.loads(text)

    # 检查Locale为"zh-CN"的记录，将满足条件的ShortName添加到列表中
    # short_names = []
    #
    # for i in range(len(data)):
    #     if data[i].get("Locale") == "zh-CN":
    #         short_names.append(data[i].get("ShortName"))

    # 打印结果
    # print(short_names)
    # # 打开一个文本文件以写入模式
    # with open("voice_list.txt", "w") as file:
    #     # 遍历列表中的每个元素，并将其写入文件
    #     # 使用encode将Unicode字符转换为bytes，然后使用decode将其转换回字符串
    #     for name in short_names:
    #         file.write(name +"\n")

    with open(article_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        count = 1
        for line in lines:
            print(f"line: {count}, sentence: {line}")
            # zh-CN-YunfengNeural
            app.save_audio(line.strip(), "data_source/results/voices/全球废土/全球废土_2/", ["zh-CN-YunxiNeural"], str(count))
            count += 1

    # app.save_audio("这，就是我最后的战争，无穷无尽。。。你们真的天真的以为谈判就能带来和平？不要搞笑了好吗？？ 杀尽一切！！士兵们，跟着我，冲锋！！！","data_source/results/voices/", short_names)
