from flask import Flask, render_template, request, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

# 実行中のプロセスIDを保持する変数
process = None

# 出力ファイルのパスを指定
output_file = "output.txt"  # 必要であれば絶対パスを指定してください

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-recording', methods=['POST'])
def start_recording():
    global process
    try:
        # maketest.py をバックグラウンドで実行
        process = subprocess.Popen(['python', 'maketest.py'])
        return jsonify({"message": "Recording started successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    global process
    try:
        if process and process.poll() is None:  # プロセスが実行中であれば
            if os.name == 'nt':  # Windowsの場合
                process.terminate()
            else:  # UNIX系の場合
                os.kill(process.pid, signal.SIGTERM)
            process = None  # プロセスをリセット
            return jsonify({"message": "Recording stopped successfully"}), 200
        else:
            return jsonify({"message": "No recording process found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-transcription', methods=['GET'])
def get_transcription():
    try:
        if os.path.exists(output_file):  # ファイルが存在する場合
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"DEBUG: File content read: {content}")  # デバッグ用
            return jsonify({"transcription": content}), 200
        else:
            print("DEBUG: File does not exist")
            return jsonify({"transcription": ""}), 200
    except Exception as e:
        print(f"DEBUG: Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
        
@app.route('/delete-transcription', methods=['POST'])
def delete_transcription():
    """
    output.txtを削除する
    """
    try:
        if os.path.exists(output_file):
            os.remove(output_file)
            return jsonify({"message": "output.txt deleted successfully"}), 200
        else:
            return jsonify({"message": "output.txt does not exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
