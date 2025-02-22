import os
from transformers import pipeline
from googletrans import Translator

# 出力ファイルのパスを指定
output_file = "output.txt"  # 必要であれば絶対パスを指定してください
summary_file = "summary.txt"

def summarize_text(text, max_length=130, min_length=30):
    """
    テキストを要約する
    :param text: 要約するテキスト
    :param max_length: 要約の最大長
    :param min_length: 要約の最小長
    :return: 要約されたテキスト
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def translate_text(text, dest_language="ja"):
    """
    テキストを翻訳する
    :param text: 翻訳するテキスト
    :param dest_language: 翻訳先の言語
    :return: 翻訳されたテキスト
    """
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

def main():
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        summary = summarize_text(content)
        translated_summary = translate_text(summary)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(translated_summary)
        
        print(f"Summary written to {summary_file}")
    else:
        print(f"{output_file} does not exist.")

if __name__ == "__main__":
    main()