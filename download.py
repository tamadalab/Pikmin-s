import shutil
import os
import tkinter as tk
from tkinter import filedialog

def download_file(source_path):
    # ファイル保存ダイアログを表示
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示

    destination_path = filedialog.asksaveasfilename(
        title="保存先を選択",  # タイトル
        initialfile=os.path.basename(source_path),  # デフォルトのファイル名
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]  # ファイルタイプのフィルタ
    )
    
    if destination_path:
        try:
            # ファイルをコピー
            shutil.copy(source_path, destination_path)
            print(f"File downloaded to: {destination_path}")
        except FileNotFoundError:
            print("Source file not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No destination selected. Operation canceled.")

# メイン処理
if __name__ == "__main__":
    source_file = "output.txt"  # コピー元のファイル

    # コピー元ファイルの存在確認
    if not os.path.exists(source_file):
        print(f"Source file '{source_file}' not found.")
    else:
        download_file(source_file)
