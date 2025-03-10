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
各プログラムに`persona`という変数があるので，この変数に`benevolent`，`greedy`などのペルソナを入力し，エージェントに反映させることができます．<br>
`iteration`という変数は一回の実験で何体のエージェントで実験を行うかを決めます．<br>
`experiment_set`と言う変数は，実験を区切る数字です．例えば，エージェント100体での実験を3回に分けて行いたい場合は，`iteration=100`とし，`experiment_set`は，1，2，3に分けて実験を行います．

#### 最後通牒ゲーム
`python ultimatum_proposer.py`<br>

`ultimatum_result`というフォルダが生成され，その中に，ペルソナフォルダが生成され，さらにその中に，`ultimatum_{experiment_set}.csv`という実験結果データが生成されます．

#### 独裁者ゲーム
`python dictator_proposer.py`<br>

`dictator_game_result`というフォルダが生成され，その中に，ペルソナフォルダが生成され，その中に，`dictator_{experiment_set}.csv`という実験結果データが生成されます．

#### 匿名独裁者ゲーム

`python dictator_anonymous_proposer.py`<br>

`dictator_game_anonymous_result`というフォルダが生成され，その中に，ペルソナフォルダが生成され，その中に，`dictator_anonymous_{experiment_set}.csv`という実験結果データが生成されます．

#### 提案者が2通りの最後通牒ゲーム
##### 提案者がエージェントの場合

`python unfair_receiver_human.py`<br>

##### 提案者がコンピュータの場合

`python unfair_receiver_program.py`<br>

### 理由の分析
`python text_classification.py`<br>