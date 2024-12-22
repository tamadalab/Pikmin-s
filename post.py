import re
import requests

FILE_PATH = "output.txt"  # 読み取るファイルのパス
ESA_ACCESS_TOKEN = "個人のAPIが必要"  # ESA API トークン
ESA_TEAM = "tamadalab"          # チーム名

def main():
    # ファイルを読み込み、全行を取得
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 投稿内容をまとめるための変数
    post_title = ""
    post_body = ""
    category_year = ""

    for line in lines:
        match = re.match(r"\[(\d{4})-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}\] (.+)", line)
        if match:
            year, month, day, content = match.groups()
            category_year = f"文字起こし{year}"  # 年をカテゴリに使用
            if not post_title:
                # 最初の行の日付を利用して投稿タイトルを生成
                post_title = f"{year}-{month}-{day}"
            post_body += f"- [{year}-{month}-{day}] {content}\n"

    # 投稿処理
    if post_title and post_body:
        post_to_esa(post_title, post_body, category_year)
    else:
        print("投稿内容がありません。")
    print(f"投稿準備: タイトル=文字起こし{post_title}, カテゴリ={category_year}")

def post_to_esa(title, body, category):
    url = f"https://api.esa.io/v1/teams/{ESA_TEAM}/posts"
    headers = {"Authorization": f"Bearer {ESA_ACCESS_TOKEN}"}
    data = {
        "post": {
            "name": title,
            "body_md": body,
            "category": category,
            "wip": True,
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("投稿が成功しました！")
    else:
        print(f"投稿に失敗しました: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()
