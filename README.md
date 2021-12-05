thermal agent simulation system
===============================
## システムコンセプト
![system concept](system_concept.png?raw=true "System concept")


エージェントシミュレーションベースの簡易温度環境シミュレータ
- 秒単位での予測
- 単位立方メートルレベルでの局所的な変化の予測
- シミュレーション結果の可視化による温度変化の分析
- 高速計算

-------------------------
実行環境
-------------------------
- Python 3.7.6: https://www.python.org/downloads/release/python-376/

### python package

- Numpy 1.21.2: https://numpy.org/
- matplotlib 3.4.3: https://matplotlib.org/stable/index.html
- mesa 0.8.9: https://mesa.readthedocs.io/en/doc_builds/index.html

※これ以外のパッケージはpython3.9.5の標準で準備されています。

## 実行環境のセットアップ
### 1. 実行用のディレクトリを作成
```
$ mkdir simulation
$ cd simulation
```
### 2. ソースコードのclone
 ```
$ git clone https://github.com/Kdy0115/agent-simulation-system.git
```
以下の3.1か4.1の実行環境を選択

### 3. ローカル環境での実行
3.1. 各種ライブラリをインストール（python仮想環境の構築を推奨）
```
$ pip install Numpy==1.21.2
$ pip install matplotlib==3.4.3
$ pip install mesa==0.8.9
```
3.2. main.pyの実行
```
$ python main.py
```

### 4. Dockerコンテナ内での実行
4.1. Dockerのインストール https://www.docker.com/

4.2. 実行環境コンテナimageのbuildと実行
```
$ docker compose up -d --build
```
すでにimageが生成されている場合は以下のコマンド
```
$ docker compose up -d
```

4.3. dockerコンテナ内へログイン
```
$ docker compose exec python3 bash
```

4.4. 実行ファイルがあるディレクトリ内へ移動
```
$ cd opt
```

4.5. シミュレーションの実行
```
$ python main.py
```

4.6. コンテナの停止
```
$ docker compose stop
```