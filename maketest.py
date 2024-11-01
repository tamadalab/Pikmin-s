import wave
import time
from datetime import datetime
import pyaudio
import whisper
import numpy as np

FORMAT = pyaudio.paInt16
SAMPLE_RATE = 44100        # サンプリングレート
CHANNELS = 1               # モノラル
INPUT_DEVICE_INDEX = 0     # マイクのチャンネル
THRESHOLD = 100            # 無音の判定基準（音量がこれ以下なら無音とみなす）
SILENCE_DURATION = 1       # 無音とみなす秒数

OUTPUT_TXT_FILE = "./" + datetime.now().strftime('%Y%m%d_%H_%M') + ".txt"

# Whisperモデルをロード
model = whisper.load_model("base")

def look_for_audio_input():
    """
    デバイス上でのオーディオ機器情報を表示する
    """
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        print(pa.get_device_info_by_index(i))
        print()
    pa.terminate()

def detect_silence(data):
    """
    無音を検出する
    """
    audio_data = np.frombuffer(data, dtype=np.int16)
    volume = np.abs(audio_data).mean()
    return volume < THRESHOLD

def transcribe_audio():
    """
    Whisperで音声認識を行い、テキストファイルに追記する
    """
    result = model.transcribe("temp_audio.wav", language="ja")
    with open(OUTPUT_TXT_FILE, 'a') as f:
        f.write("\n" + result['text'])

def realtime_textise():
    """
    リアルタイムで音声を文字起こしする
    """
    with open(OUTPUT_TXT_FILE, 'w') as f:
        DATE = datetime.now().strftime('%Y%m%d_%H:%M:%S')
        f.write("日時 : " + DATE + "\n")

    # Audio インスタンス取得
    audio = pyaudio.PyAudio()

    # ストリームオブジェクトを作成
    stream = audio.open(format=FORMAT,
                        rate=SAMPLE_RATE,
                        channels=CHANNELS,
                        input_device_index=INPUT_DEVICE_INDEX,
                        input=True,
                        frames_per_buffer=int(SAMPLE_RATE * 0.1))  # 0.1秒ごとにデータを取得

    silent_chunks = 0  # 無音が続いたチャンク数
    frames = []  # 音声データを蓄積するためのリスト

    while True:
        data = stream.read(int(SAMPLE_RATE * 0.1), exception_on_overflow=False)  # 0.1秒ごとのデータ
        if detect_silence(data):
            silent_chunks += 1
        else:
            silent_chunks = 0
            frames.append(data)

        # 無音がSILENCE_DURATION秒以上続いた場合、録音を終了して文字起こしを行う
        if silent_chunks >= int(SILENCE_DURATION * 10):  # 0.1秒単位でカウント
            if frames:  # 録音された音声がある場合のみ処理
                with wave.open("temp_audio.wav", 'wb') as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(audio.get_sample_size(FORMAT))
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(b''.join(frames))

                transcribe_audio()
                frames = []  # リストをクリアして新しい録音に備える
            silent_chunks = 0

    stream.stop_stream()
    stream.close()
    audio.terminate()

def main():
    look_for_audio_input()
    realtime_textise()

if __name__ == '__main__':
    main()
