import snowboydecoder
import sys
import signal
import temp_reply
import playaudio
import cv2
from ai_robot import ai_robot
import fan
import threading # 视频播放与语音聊天同步
# import voice_wakeup
#迭代循环

def two_choice():
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('/home/pi/snowboy/voice_wakeup/txt/first_reply_init.txt','/home/pi/snowboy/voice_wakeup/wav/first_reply_init')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/first_reply_init.wav')
        choice=Choice() #此处不能与类名相同
        choice.choice()
        
def ai_chat():
        # 进入聊天模式
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('/home/pi/snowboy/voice_wakeup/txt/chat.txt','/home/pi/snowboy/voice_wakeup/wav/chat')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/chat.wav')
        # self.play_video('smile3.mp4')
        AI = ai_robot()
        AI.start_chat()
    
def play_video(video_path):
        # 创建一个videocapture对象
        cap=cv2.VideoCapture(video_path)
        
        # 获取视频的宽和高
        video_width = int (cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height =int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 创建窗口，并设置全屏且处于中央
        cv2.namedWindow('smile',cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('smile',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        
        # 获取视频的帧频
        fps = cap.get(cv2.CAP_PROP_FPS)
        while cap.isOpened() :
                #逐帧读取视频
                ret,frame = cap.read()
                if ret == True:
                        # 窗口大小
                        src = cv2.resize(frame,(video_width ,video_height),interpolation=cv2.INTER_CUBIC) 
                        # 显示窗口
                        cv2.imshow('smile',src)
                        #按q 退出
                        if cv2.waitKey(int(1000/fps)) & 0xFF ==ord('q'):
                                break
                else:
                        break
        # 释放资源
        cap.release()
        cv2.destroyAllWindows()
        
def chat():
        thread_aichat = threading.Thread(target = ai_chat())
        thread_playvideo = threading.Thread(target = play_video('video_smile/smile2.mp4'))
        
        # 启动线程
        thread_aichat.start()
        thread_playvideo.start()
        
        # 等待两个线程同时结束
        thread_aichat.join()
        thread_playvideo.join()
        
def turn_on_fan():
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('/home/pi/snowboy/voice_wakeup/txt/turn_on_fan.txt','/home/pi/snowboy/voice_wakeup/wav/turn_on_fan')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/turn_on_fan.wav')
        ##预留打开风扇的代码##
        fan.turn_on_fan()
     
def turn_off_fan():
        ##预留关闭风扇的代码##
        fan.turn_off_fan()
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('/home/pi/snowboy/voice_wakeup/txt/turn_off_fan.txt','/home/pi/snowboy/voice_wakeup/wav/turn_off_fan')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/turn_off_fan.wav')
        
# 选择模式，目前选择聊天和风扇模式
class Choice:
        
    def __init__(self):
        self.interrupted_init = False # 初始运行
        self.interrupted = False
       
    def interrupt_callback_init(self):
       # 初始运行
        return self.interrupted_init
        
    def interrupt_callback(self):
       # global self.interrupted
        return self.interrupted
        
    def signal_handler(self,signal,frame):
       # global self.interrupted
        self.interrupted = True 

    def signal_handler_init(self,signal,frame):
       # 初始运行
        self.interrupted_init = True
         
    def first_reply_loop(self):
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('/home/pi/snowboy/voice_wakeup/txt/first_reply_loop.txt','wav/first_reply_loop')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/first_reply_loop.wav')
        self.choice() 
           
    def choice(self):
        # define models and functions related to them
        models = ['/home/pi/snowboy/voice_wakeup/VoiceModel/dakaifengshan.pmdl',
        '/home/pi/snowboy/voice_wakeup/VoiceModel/guanbifengshan.pmdl',
        '/home/pi/snowboy/voice_wakeup/VoiceModel/xuefen.pmdl',
        '/home/pi/snowboy/voice_wakeup/VoiceModel/liaotianmoshi.pmdl']
        # 两个关闭风扇热词，'/home/pi/snowboy/voice_wakeup/VoiceModel/guanfengshan.pmdl',提高命中率
        callbacks = [lambda:turn_on_fan(),
        lambda:turn_off_fan(),
        lambda:self.first_reply_loop(),
        #lambda:self.turn_off_fan(),
        lambda:ai_chat()] 
        # define detector
        signal.signal(signal.SIGINT,self.signal_handler)
        sensitivity=[0.5]*len(models)
        detector=snowboydecoder.HotwordDetector(models,sensitivity=sensitivity)
        print('Start detect')
        # main loop,detect voice per 0.03s
        detector.start(detected_callback=callbacks,
                       interrupt_check=self.interrupt_callback, #lambda:False,
                       sleep_time=0.03)
        detector.terminate()
        
    def wakeup(self):
        # 初始运行
        # define models and functions related to them
        models_init = ['/home/pi/snowboy/voice_wakeup/VoiceModel/xuefen.pmdl']
        callbacks_init = [lambda:two_choice()]

        # define detector
        signal.signal(signal.SIGINT,self.signal_handler_init)
        sensitivity_init=[0.5]*len(models_init)
        detector_init=snowboydecoder.HotwordDetector(models_init,sensitivity=sensitivity_init)
        print('Start detect(init)')
        
        #main loop,detect voice per 0.03s
        detector_init.start(detected_callback=callbacks_init,
                        interrupt_check=self.interrupt_callback_init, #lambda:False,
                        sleep_time=0.03)
        
        detector_init.terminate()
if __name__=='__main__':
    choice=Choice()
    choice.wakeup()
    

