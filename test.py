from inference import VITS_TTS_converter
from QAsystem.QAsystem import QAsystem
from whisper_step.whisper_step import trans_audio_sentence
import pyaudio,wave
import numpy as np
import keyboard
import time
from scipy.io.wavfile import write
def float2pcm(sig, dtype='int16'):
    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)

# initialize QAsystem
system = QAsystem()
vits = VITS_TTS_converter(model='ljs', device='cpu')

#%%---------------------DO NOT TOUCH ABOVE---------------------------------
# sentiment = return_predictions(model_path='sentiment_classification/approach-2-model.pth', audio_path='question_covid.wav')

# speech-to-text conversion
sentences = trans_audio_sentence('question_covid.wav')
print(sentences)
query = sentences
# answer question
answer = system.generate_answer(query)
# text-to-speech conversion
audio = vits.infer(sentence=answer, sid=None)
write('answer.wav', 22050, float2pcm(audio))
# print output text
print(answer + '\n')
# play output audio
chunk = 2048

wf = wave.open(r"answer.wav", 'rb')

p = pyaudio.PyAudio()

# 打开声音输出流
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# 写声音输出流进行播放
while True:
    data = wf.readframes(chunk)
    if data == bytes("".encode()): break
    stream.write(data)

stream.close()
p.terminate()
