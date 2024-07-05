import snowboydecoder
import sys
import signal
import temp_reply
import playaudio
from Choice import Choice
interrupted = False

def interrupt_callback():
    global interrupted
    return interrupted
    
def signal_handler(signal, frame):
    global interrupted
    interrupted = True 
def two_choice():
    playaudio.play_audio('wav/ding.wav')
    #初始回复
    #用于生成回复的初始音频文件
    #temp_reply.tts('txt/first_reply.txt','wav/first_reply')
    #生成好之后不用重复生成，直接用音频文件输出即可
    playaudio.play_audio('wav/first_reply.wav')
    choice=Choice() #此处不能与类名相同
    choice.choice()
 
#def signal_handler():
#    print("start")
def wakeup():
    # define models and functions related to them
    models = ['VoiceModle/xuefen.pmdl']# 'VoiceModle/kaifengshan.pmdl','VoiceModle/fengshan.pmdl']#,'VoiceModle/kaifengshan.pmdl']#',
    callbacks = [lambda:two_choice()]

    # define detector
    signal.signal(signal.SIGINT,signal_handler)
    sensitivity=[0.5]*len(models)
    detector=snowboydecoder.HotwordDetector(models,sensitivity=sensitivity)
    print('Start detect')
    
    #main loop,detect voice per 0.03s
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback, #lambda:False,
                   sleep_time=0.03)
    
    detector.terminate()
if __name__=='__main__':
    wakeup()
    
