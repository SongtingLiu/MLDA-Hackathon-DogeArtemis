import pyaudio,wave
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=2, rate=16000, input=True, frames_per_buffer=2048)
record_buf = []
count = 0
while count < 8*5:
    audio_data = stream.read(2048)      # 读出声卡缓冲区的音频数据
    record_buf.append(audio_data)       # 将读出的音频数据追加到record_buf列表
    count += 1
    print('*')
    wf = wave.open('question_electric.wav', 'wb')          # 创建一个音频文件，名字为“01.wav"
    wf.setnchannels(2)                      # 设置声道数为2
    wf.setsampwidth(2)                      # 设置采样深度为
    wf.setframerate(16000)                  # 设置采样率为16000
    # 将数据写入创建的音频文件
    wf.writeframes("".encode().join(record_buf))
    # 写完后将文件关闭
    wf.close()
# 停止声卡
stream.stop_stream()
# 关闭声卡
stream.close()
# 终止pyaudio
pa.terminate()