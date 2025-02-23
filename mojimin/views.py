from flask import Flask, render_template, request, jsonify, send_file
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
        # transcription.py をバックグラウンドで実行
        process = subprocess.Popen(['python', 'transcription.py'])
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
            return jsonify({"transcription": content}), 200
        else:
            return jsonify({"transcription": ""}), 200
    except Exception as e:
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

@app.route('/run-download-script', methods=['POST'])
def run_download_script():
    try:
        # download.py を実行
        process = subprocess.Popen(
            ['python', 'download.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return jsonify({"message": "Download script executed successfully", "details": stdout.decode()}), 200
        else:
            return jsonify({"error": stderr.decode()}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download-transcription', methods=['GET'])
def download_transcription():
    """
    ファイルをダウンロードする
    """
    try:
        return send_file(output_file, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/execute-post', methods=['POST'])
def execute_post():
    try:
        # post.pyを実行
        result = subprocess.run(['python', 'post.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return {"message": "Post script executed successfully"}, 200
        else:
            return {"error": result.stderr}, 500
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
