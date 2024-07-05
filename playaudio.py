import pyaudio
import wave
import sys


def play_audio(wav_path):
    CHUNK = 1024

    if len(sys.argv) < 1:
        print('plays a wave file.\n\nUsage:%s filename.wav' % sys.argv[0])
        sys.exit(-1)
    wf = wave.open(wav_path, 'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    ##play audio
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

