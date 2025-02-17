import wave
import time
import pyaudio
import whisper
import numpy as np
import os

# 定数
FORMAT = pyaudio.paInt16
SAMPLE_RATE = 44100        # サンプリングレート
CHANNELS = 1               # モノラル
INPUT_DEVICE_INDEX = 0     # マイクのデバイスインデックス
THRESHOLD = 100            # 無音の判定基準 振幅が平均100未満の場合出力する
SILENCE_DURATION = 0.5       # 無音とみなす秒数

# 出力ファイルのパスを指定
output_file = os.path.join(os.path.dirname(__file__), "output.txt")

# Whisperモデルのロード
model = whisper.load_model("base")

def detect_silence(data):
    """
    無音を検出する
    """
    audio_data = np.frombuffer(data, dtype=np.int16)
    volume = np.abs(audio_data).mean()
    return volume < THRESHOLD

def transcribe_audio():
    """
    Whisperで音声認識を行い、文字起こし結果をoutput.txtに追記
    """
    try:
        # temp_audio.wav を文字起こし
        result = model.transcribe("temp_audio.wav", language="ja")
        # output.txt に文字起こし結果を追記
        with open(output_file, 'a', encoding='utf-8') as f:  # 'a' モードで追記
            f.write(f"{result['text']}\n")
            f.flush()  # 書き込みを即座に反映
    except Exception as e:
        pass  # エラー時も何も表示しない

def realtime_textise():
    """
    リアルタイムで音声を録音し、文字起こしする
    """
    # ファイルは追記モードを使うので、初期化は不要

    audio = pyaudio.PyAudio()

    # ストリームを開始
    stream = audio.open(format=FORMAT,
                        rate=SAMPLE_RATE,
                        channels=CHANNELS,
                        input_device_index=INPUT_DEVICE_INDEX,
                        input=True,
                        frames_per_buffer=int(SAMPLE_RATE * 0.1))  # 0.1秒ごとにデータを取得

    silent_chunks = 0  # 無音が続いたチャンク数
    frames = []        # 録音データを蓄積

    try:
        while True:
            data = stream.read(int(SAMPLE_RATE * 0.1), exception_on_overflow=False)
            if detect_silence(data):
                silent_chunks += 1
            else:
                silent_chunks = 0
                frames.append(data)

            # 無音が一定時間続いたら文字起こしを実行
            if silent_chunks >= int(SILENCE_DURATION * 10):  # 0.1秒単位でカウント
                if frames:  # データが存在する場合のみ処理
                    # temp_audio.wav に録音データを書き込み
                    with wave.open("temp_audio.wav", 'wb') as wf:
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(audio.get_sample_size(FORMAT))
                        wf.setframerate(SAMPLE_RATE)
                        wf.writeframes(b''.join(frames))
                    # 録音データを文字起こし
                    transcribe_audio()
                    frames = []  # 録音データをクリアして次のセッションへ
                silent_chunks = 0
    except KeyboardInterrupt:
        pass  # 録音停止時のメッセージを非表示
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def main():
    """
    プログラムのエントリポイント
    """
    realtime_textise()

if __name__ == '__main__':
    main()
