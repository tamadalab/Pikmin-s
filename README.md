<h1 align="center"><img src="https://github.com/user-attachments/assets/42cbb20f-106e-4a33-891f-0e4fd71a875f" alt="モジミンアイコン" width="50px">Pikmin-s!<img src="https://github.com/user-attachments/assets/42cbb20f-106e-4a33-891f-0e4fd71a875f" alt="モジミンアイコン" width="50px"></h1>
<div>
  
</div>
<h2>システム名</h2>
もじみん

<h2>機能</h2>
ローカル上でwebアプリを起動し、マイクに向かって話すことでリアルタイムで書き起こしてくれるシステム

<h2>シナリオ</h2>
<ol>
  <li>webブラウザのボタンを押す</li>
  <li>文字起こし開始</li>
  <li>0.5秒無音だった場合、テキスト欄に文字が表示される</li>
  <li>話し始めると文字起こしが行われる。</li>
  <li>停止ボタンを押すと、文字起こしが終了される</li>
</ol>

<h2>ファイル</h2>
<ol>
  <li>maketest.py</li>
   whisperというAIを利用した文字起こしするプログラム
  <li>download.py</li>
   文字起こしした内容をダウンロードするプログラム
  <li>server/py</li>
   Flaskアプリを起動するプログラム
  <li>views.py</li>
   ダウンロードやリセットや録音などのボタンを押した場合に各々のプログラムを実行するプログラム
  <li>index.html</li>
   webデザインを表示させるプログラム
  <li>post.py</li>
   esa.ioに投稿するプログラム
  <li>mojimin.png</li>
   アイコン

</ol>

<h2>使用したライブラリ</h2>
・pyaudio
Pythonでオーディオ操作(マイク)を簡単に利用できます。
　pip install pyaudio
<h2>使用したフレームワーク</h2>
・flask
 pip install flask
Pythonでwebアプリを作成することができます。
<h2>使用したオープンソース</h2>
・whisper
文字起こしに特化したOpenAi
!pip install -q git+https://github.com/openai/whisper.git

<h2>開発環境</h2>
<h3>使用技術・ライブララリ</h3>
<div>
  <img src="https://github.com/user-attachments/assets/ff419d23-41a4-42ea-a53d-d016821f530b" alt="python"> <img src="https://github.com/user-attachments/assets/307a9cc2-347e-4f36-9eab-525bb5ec3380" alt="javascript">
</div>
<table>
  <tr>
    <th>種類</th>
    <th>技術・ライブラリ</th>
    <th>バージョン</th>
    <th>説明</th>
  </tr>
  <tr>
    <td>プログラミング言語</td>
    <td>Python</td>
    <td>3.9以上</td>
    <td>プロジェクト全体で使用する主要な言語</td>
  </tr>
  <tr>
    <td>フロントエンド</td>
    <td>Javascript</td>
    <td>ES6以上</td>
    <td>Webアプリケーションの動的な部分を担当</td>
  </tr>
</table>


