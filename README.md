thermal agent simulation system
===============================
## System Concept
![system concept](system_concept.png?raw=true "System concept")


エージェントシミュレーションベースの簡易温度環境シミュレータ
- 秒単位での予測
- 単位立方メートルレベルでの局所的な変化の予測
- シミュレーション結果の可視化による温度変化の分析
- 実世界時間の約3倍の速度


実行環境
--------
- OS: Vagrantで実行するため依存なし
- Python 3.7.12: https://www.python.org/downloads/release/python-3712/
- Vagrant 2.2.18: https://www.vagrantup.com/
- VirtualBox 6.1.26: https://www.virtualbox.org/wiki/Downloads

### python package

- Numpy 1.21.2: https://numpy.org/
- matplotlib 3.4.3: https://matplotlib.org/stable/index.html
- mesa 0.8.9: https://mesa.readthedocs.io/en/doc_builds/index.html

※これ以外のパッケージはpython3.7.12の標準で準備されています。

## Quick Start
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

### 4. vagrantファイルの確認
vagrantファイルの設定を確認してください。
基本的にはデフォルト設定で問題ありません。


vagrantのバージョンを指定します。
```
Vagrant.configure("2") do |config|
```
VirtualBoxに名前をつけます。
```
config.vm.box = "thermal_simulation"
```
仮想サーバーのOSを指定します。（Ubuntsu 16.0.4）
```
config.vm.box_url = "http://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-vagrant.box"
```
仮想サーバーのIPアドレスを割り当てます。
```
config.vm.network "private_network", ip: "172.16.16.1"
```
ローカルフォルダと仮想サーバー内のフォルダを同期します。
```
config.vm.synced_folder "./", "/var/thermal_simulation"
```
仮想サーバーのその他の設定を行います。
```
config.vm.provider "virtualbox" do |vb|
  # GUIは使用しません。
  vb.gui = false
  # 割り当てるメモリ容量を決定します。
  vb.memory = 4096
  # 割り当てるCPU数を決定します。
  vb.cpus = 6
```
※CPU数は並列処理を利用する場合に数を変更することがあります。

### 5. vagrantの実行
`VagrantFile`と同階層で以下のコマンドを実行して仮想サーバーを生成してください。
```
vagrant up
```
