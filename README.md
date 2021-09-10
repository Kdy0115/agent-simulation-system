thermal agent simulation system
===============================
## System Concept
![system concept](system_concept.png?raw=true "System concept")


エージェントシミュレーションベースの簡易温度環境シミュレータ
- 秒単位での予測
- 単位立方メートルレベルでの局所的な変化の予測
- シミュレーション結果の可視化による温度変化の分析
- 高速計算


実行環境
--------
- Python 3.9.5: https://www.python.org/downloads/release/python-395/
- Vagrant 2.2.18: https://www.vagrantup.com/
- VirtualBox 6.0.24: https://www.virtualbox.org/wiki/Downloads

### python package

- Numpy 1.21.2: https://numpy.org/
- matplotlib 3.4.3: https://matplotlib.org/stable/index.html
- mesa 0.8.9: https://mesa.readthedocs.io/en/doc_builds/index.html

※これ以外のパッケージはpython3.9.5の標準で準備されています。

## 実行環境のセットアップ
#### 1. Vagrantをインストール
https://www.vagrantup.com/

サーバ仮想化のためにVagrantをインストールします。


#### 2. VirtualBoxをインストール
https://www.virtualbox.org/wiki/Downloads

Vagrant実行のためにVirtualBoxが必要です。
VirtualBoxをインストールします。


#### 3. simulationをクローン
```
git clone https://github.com/Kdy0115/agent-simulation-system.git
```

#### 4. vagrantファイルの確認
`Vagrantfile`の設定を確認してください。
基本的にはデフォルト設定で問題ありません。


vagrantのバージョンを指定します。
```
Vagrant.configure("2") do |config|
```
仮想サーバーのOSを指定します。（Ubuntsu 21.04）
```
config.vm.box = "ubuntu/hirsute64"
```
ローカルフォルダと仮想サーバー内のフォルダを同期します。
デフォルトではvagrantファイルと同階層のカレントディレクトリと同期します。
```
config.vm.synced_folder "./", "/var/thermal_simulation"
```
仮想サーバーのその他の設定を行います。
```
config.vm.provider "virtualbox" do |vb|
  vb.gui = false
  # 割り当てるメモリ容量を決定します。
  vb.memory = 4096
  # 割り当てるCPU数を決定します。
  vb.cpus = 6
```
※CPU数は並列処理を利用する場合に数を変更することがあります。

### 5. vagrantの実行
`Vagrantfile`と同階層で以下のコマンドを実行して仮想サーバーを生成してください。
```
vagrant up
```

### 6. 仮想サーバーへ接続
```
vagrant ssh
```
