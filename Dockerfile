FROM python:3.9

RUN apt-get update
RUN apt-get update && apt-get install -y \
    pulseaudio \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# ダミーサウンドデバイスの設定
# RUN echo "snd-dummy" >> /etc/modules

RUN pip install --upgrade pip
RUN pip install SpeechRecognition
RUN pip install pyaudio
RUN python3 -m pip install numpy
RUN pip install flask
RUN pip install git+https://github.com/openai/whisper.git
RUN python -m pip install jupyterlab

# エントリーポイントを設定
CMD ["python", "server.py"]
