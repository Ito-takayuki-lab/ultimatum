# ultimatum

2024年度B4村重がLLMによる被験者実験で用いた環境です．<br>
<https://microsoft.github.io/autogen/0.2/>を実験環境として用いました．0.2と0.4がありますが，0.2の方を用いました．


## 環境構築の手順
#### anacondaでpythonの仮想環境を作成します．pythonバージョンは3.10を用います． <br>

`conda create -n (環境名) python=3.10`<br>

#### 環境をアクティブにします<br>

`conda activate (環境名)`<br>

#### 関連ライブラリなどを全てインストールします

`pip install -r requirements.txt`<br>

#### .envを作成しAPIキーを登録します

`OPENAI_API_KEY = APIキー`


## プログラムの実行
### 被験者実験
#### 最後通牒ゲーム
`python ultimatum_proposer.py`<br>

#### 独裁者ゲーム
`python dictator_proposer.py`<br>

#### 匿名独裁者ゲーム

`python dictator_anonymous_proposer.py`<br>

#### 提案者が2通りの最後通牒ゲーム
##### 提案者がエージェントの場合

`python unfair_receiver_human.py`<br>

##### 提案者がコンピュータの場合

`python unfair_receiver_program.py`<br>

### 理由の分析
`python text_classification.py`<br>