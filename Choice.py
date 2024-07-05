import snowboydecoder
import sys
import signal
import temp_reply
import playaudio
from ai_robot import ai_robot
#import voice_wakeup
# 控制模式，目前只有控制风扇的开关模式
class Choice:
    def __init__(self):
        self.interrupted = False
        
    def interrupt_callback(self):
       # global self.interrupted
        return self.interrupted
        
    def signal_handler(self,signal,frame):
       # global self.interrupted
        self.interrupted = True 
    
    def turn_on_fan(self):
        playaudio.play_audio('wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('txt/turn_on_fan.txt','wav/turn_on_fan')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('wav/turn_on_fan.wav')
        ##预留打开风扇的代码##
     
    def turn_off_fan(self):
        playaudio.play_audio('wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('txt/turn_off_fan.txt','wav/turn_off_fan')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('wav/turn_off_fan.wav')
        ##预留关闭风扇的代码##
        
    def ai_chat(self):
        playaudio.play_audio('wav/ding.wav')
        #初始回复
        #用于生成回复的初始音频文件
        #temp_reply.tts('txt/chat.txt','wav/chat')
        #生成好之后不用重复生成，直接用音频文件输出即可
        playaudio.play_audio('wav/chat.wav')
        AI = ai_robot()
        AI.start_chat()
        
    #def init(slef):
    # voice_wakeup.wakeup() #迭代循环
        
    def choice(self):
        # define models and functions related to them
        self.models = ['VoiceModle/liaotian.pmdl','VoiceModle/kaifengshan.pmdl','VoiceModle/guanfengshan.pmdl','VoiceModle/guanbifengshan.pmdl']#'VoiceModle/xuefen.pmdl']# 两个关闭风扇热词，提高命中率
        self.callbacks = [lambda:self.ai_chat(),
        lambda:self.turn_on_fan(),
        lambda:self.turn_off_fan(),
        lambda:self.turn_off_fan()]
        #lambda:self.init()] 
        # define detector
        signal.signal(signal.SIGINT,self.signal_handler)
        self.sensitivity=[0.5]*len(self.models)
        self.detector=snowboydecoder.HotwordDetector(self.models,sensitivity=self.sensitivity)
        print('Start detect')
        
        #main loop,detect voice per 0.03s
        self.detector.start(detected_callback=self.callbacks,
                       interrupt_check=self.interrupt_callback, #lambda:False,
                       sleep_time=0.03)
        
        self.detector.terminate()
if __name__=='__main__':
	Choice=Choice()
	Choice.choice()
    

