import requests
import json
import asr
import tts
import sys
from auto_record import auto_record
import playaudio
import temp_reply
class ai_robot:
    API_KEY = 'kNpGoAVgiXIMH1z298Gvv1Q2'
    SECRET_KEY = 'bWzYBEqE7FxGaYFkzmSaYaChpWRew29B'

    # 生成一次message
    def __init__(self):
        self.messages = [
            {"role": 'user', "content": "你好"},
            {"role": "assistant", "content": "你好,有什么我可以帮助你的吗？"}
        ]

    def get_access_token(self):
        url = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {'grant_type': 'client_credentials', 'client_id': self.API_KEY, 'client_secret': self.SECRET_KEY}
        return str(requests.post(url, params=params).json().get('access_token'))

    # 启动文心一言
    def get_url(self):
        url = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=' + self.get_access_token()
        return url

    ##将messages上传给文心一言，并获得答案
    def get_assistant_reply(self, url):
        payload = json.dumps({"messages": self.messages})
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        # translate the answers by the robot
        response_data = json.loads(response.text)
        return response_data.get('result')

    ##用户message扩充
    def message_usr_append(self, question):
        self.messages.append({"role": "user", "content": question})

    ##机器人message扩充
    def message_assistant_append(self, reply):
        self.messages.append({'role': "assistant", 'content': reply})

    ##开始录音，并进行智能回答
    def start_chat(self):
        url = self.get_url() ##增加时间延长
        # start recording and convert the speech into text
        Epoch = True
        while Epoch:
            micro = auto_record()#建立一个自动录音对象
            flag = micro.listen()  ##开始听
            if flag:  ##如果声音强度足够
                micro.record() #开始录音
                #play dong to indicate that user's question has been recorded.
                playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/dong.wav')
                
                #填充机器人搜索答案的时间
                #temp_reply.tts('/home/pi/snowboy/voice_wakeup/txt/temp_reply.txt','/home/pi/snowboy/voice_wakeup/wav/temp_reply') #成生初始回复
                #直接播放已经生成好的音频，不用重复使用文心一言
                playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/temp_reply.wav')
                
                ###以下代码会加长延时
                sound_file = micro.sound_flie_path()
                question = asr.asr(sound_file)
                # put the input by users into the message
                self.message_usr_append(question)
                assistant_reply = self.get_assistant_reply(url)
                self.message_assistant_append(assistant_reply)
                
                # convet text to speech
                tts.tts(assistant_reply)
                
            else:
                Epoch = False


if __name__ == '__main__':
    AI = ai_robot()
    AI.start_chat()





