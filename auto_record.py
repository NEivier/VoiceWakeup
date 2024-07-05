import pyaudio,wave
import numpy as np
import playaudio
class auto_record:
    def __init__(self):
        self.flag = False             #开始录音节点
        self.frames = []
        self.audio_max = 20
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        ##RECORD_SECONDS = 2
        self.WAVE_OUTPUT_FILENAME = '/home/pi/snowboy/voice_wakeup/wav/question.wav'
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)
    def listen(self):
        mindb=2500    #最小声音，大于则开始录音，否则结束
        delayTime=1.3  #小声1.3秒后自动终止
        print("开始!计时")
        #指示用户可以开始对话
        playaudio.play_audio('/home/pi/snowboy/voice_wakeup/wav/dong.wav')
      
        stat = True              #判断是否继续录音
        stat2 = False            #判断声音是否小
        tempnum = 0               #tempnum、tempnum2为时间
        tempnum2 = 0
        loop=0
        while stat:
            data = self.stream.read(self.CHUNK,exception_on_overflow = False)
            self.frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.short)
            audio_max = np.max(audio_data)
            if audio_max > mindb and self.flag==False:##声音大于2500分贝且之前没有开始声音节点
                loop=loop+1 #记录大声音节点数
                #self.flag =True
                #print("开始录音")
                tempnum2=tempnum  ##记录当前时间
            if loop>=13 and self.flag==False: #出现13个大声音节点
                self.flag=True
            if self.flag:##开始录音了
                if(audio_max < mindb and stat2==False):##声音变小了但是之前的声音大
                    stat2 = True  ##声音变小
                    tempnum2 = tempnum ##记录时间节点
                    print("声音小，且之前是是大的或刚开始，记录当前点")
                if(audio_max > mindb):
                    stat2 =False  ##声音一直很大
                    tempnum2 = tempnum
                    #刷新
                if(tempnum > tempnum2 + delayTime*15 and stat2==True):
                    print("间隔%.2lfs后开始检测是否还是小声"%delayTime)
                    if(stat2 and audio_max < mindb):
                        stat = False   #还是小声
                        print("小声！")
                    else:
                        stat2 = False
                        print("大声！")
            print(str(audio_max)  +  "      " +  str(tempnum))
            tempnum = tempnum + 1
            if self.flag==False and tempnum > 60:                #超过50且一直没有开始录音就直接退出
                stat = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return self.flag
      
    def record(self):
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
    def sound_flie_path(self):
        return self.WAVE_OUTPUT_FILENAME
if __name__=='__main__':
    micro=auto_record()
    flag=micro.listen()
    if flag:
        print(str(1))
        print(str(flag))
        micro.record()
    micro1=auto_record()
    flag=micro1.listen()
    if flag:
        print(str(2))
        print(str(flag))
        micro1.record()
