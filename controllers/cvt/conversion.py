# -*- coding: utf-8 -*-

""" シミュレーション実行データ整形モジュール

Todo:
    * /Thermal Agent Simulation/config/config.iniにシミュレーション設定ファイルを記載しないと実行されない
"""

# ライブラリ
import pandas as pd
import json
import csv
import datetime
import glob
from controllers.cvt.inc.cons import FLOOR5_COLUMN_NAME
import copy
from controllers import functions

class DataSet():
    """ データ整形を扱うモジュールとデータを持つデータセットクラス

    Attributes:
        bems_file_path           [str]  : 設定ファイルから読み込んだBems初期データのファイルパス
        control_data_folder_path [str]  : 設定ファイルから読み込んだ空調制御データのフォルダパス（フロア分読み込まれる）
        simulation_step          [int]  : 設定ファイルから読み込んだシミュレーション回数
        simulation_start_time    [date] : 設定ファイルから読み込んだシミュレーション開始時間
        simulation_end_time      [date] : 設定ファイルから読み込んだシミュレーション終了時間
        layout_file_path         [str]  : 設定ファイルから読み込んだ室内レイアウト情報を記載したファイルパス
        heat_source_file_path    [str]  : 設定ファイルから読み込んだ室内の熱源情報を記載したファイルパス
        skeleton_file_path       [str]  : 設定ファイルから読み込んだスケルトンファイルパス
        output_folder            [str]  : 設定ファイルから読み込んだ実行結果を格納する格納先フォルダパス
        mp_flag                  [bool] : 設定ファイルから読み込んだマルチプロセス計算を行うかのフラグ
        floors                   [array]: シミュレーションを行うフロア階数を配列形式で格納したリスト
        init_bems_data           [array]: Bems初期データの整形結果を保持する配列
        control_data             [array]: 空調制御計画データの整形結果を保持する配列
        layout_data              [array]: レイアウトデータの整形結果を保持する配列
        post_data                [array]: 最終的にシミュレーションモジュールに送るデータ全体格納した配列
        encoding                 [str]  : 文字コード
    """

    def __init__(self, config_bems: str, config_control: str, config_layout: str, config_simulation: str, mp: str, encoding: str) -> None:

        # 設定ファイルの内容を読み込む
        self.bems_file_path           = config_bems["BEMS_file_path"]
        
        self.control_data_folder_path = config_control["Control_file_path"]
        
        self.simulation_step          = config_simulation["Simulation_time"]
        self.simulation_start_time    = config_simulation["start_time"]
        self.simulation_end_time      = config_simulation["end_time"]
        self.output_folder            = config_simulation["Output_folder_path"]
        
        self.laytout_file_path        = config_layout["Lyaout_floor_file_path"]
        self.heat_source_file_path    = config_layout["Heat_source_file_path"]
        self.skeleton_file_path       = config_layout["skeleton_file_path"]
        
        self.mp_flag                  = True if mp["multiprocess"] == "True" else False
        
        # 文字コードの設定
        self.encoding                 = encoding
        
        # シミュレーションを行うフロアの選択
        # self.floors = [3,4,5]
        # self.floors = [3,4]
        self.floors                   = [5]
        
        # 整形データを格納する変数
        self.init_bems_data           = []
        self.control_data             = []
        self.layout_data              = []

        # 出力先フォルダの作成
        functions.create_dir(self.output_folder + "cmp/")



    def import_all_control_data(self):
        """ 空調制御計画データを読み込む
        """       

        # 制御計画データの読み込み
        files = glob.glob("{}*.csv".format(self.control_data_folder_path))
        # ファイルと階数で回す
        for item, floor in zip(files,self.floors):
            # 1フロア分の制御計画データを設定
            control_data_dic = {}
            f = open(item,'r',encoding=self.encoding)
            data_list = []
            # イテレータで読み込む（エージェントシミュレーションの仕様に合わせる）
            data = csv.DictReader(f)
            while True:
                try:
                    data_list.append(next(data))
                except StopIteration:
                    f.close()
                    break
            control_data_dic["floor"] = floor
            control_data_dic["control_data"]  = iter(data_list)

            self.control_data.append(control_data_dic)



    def import_all_layout_data(self):
        """ レイアウトデータをインポートするモジュール
        """
        
        # レイアウトデータのオープン（Jsonで取得）
        f = open(self.laytout_file_path)
        self.layout_data = json.load(f)
        f.close()



    def import_heat_source_data(self):
        """ 熱源データをインポートするモジュール
        """
        
        # 熱源データのオープン（Jsonで取得）
        f = open(self.heat_source_file_path)
        self.source_data = json.load(f)
        f.close()


    def _import_bems_data(self) -> None:
        """ 初期値BEMSデータをインポートしてデータを整形するモジュール
        """

        # BEMSのファイルデータをインポート（エンコーディングを指定）
        df = pd.read_csv(self.bems_file_path,encoding=self.encoding)
        # 先頭の時間を取得（フォーマットを揃えるため）
        self.start_time = df["時間"][0]
        # 時間以外のデータは数値なのでfloat型に変換
        df_format = df[df.columns[df.columns != '時間']].astype("float")
        # 時間変換後のデータを格納するための配列
        time_arr = []
        for i in df["時間"].values:
            time_arr.append(functions.format_time(i))
        # 変換した時間を格納し直す
        df_format["時間"] = time_arr

        # 階数ごとにBEMSデータを整形する
        for floor in self.floors:
            # 1フロア分のデータ
            init_bems_data = {}
            # 使用するデータのみ抽出
            df_a_f = df_format.filter(regex='({}f|外気温|時間)'.format(floor),axis=1)
            # フロア全体のデータを格納するデータ
            dfs_dict_arr = []
            for row in range(len(df_a_f)):
                dfs_dict_arr.append(dict(df_a_f.loc[row]))
            # フロアを格納
            init_bems_data["floor"] = floor
            # bems_dataを追加
            init_bems_data["bems_data"] = dfs_dict_arr
            # クラス内変数に作成したデータを格納
            self.init_bems_data.append(init_bems_data)



    def _sync_control_data(self):
        """ 制御計画データをBEMSデータに同期させる関数
        """        
        
        # if "-" in self.start_time:
        # tdatetime = datetime.datetime.strptime(self.start_time.replace("/","-"),'%Y-%m-%d %H:%M')
        # start_time = tdatetime
        # sync_time = str(start_time)
        
        # シミュレーション開始時間を基準時間に設定しフォーマットをYYYY/MM/DD hh:mm:00に設定
        if "/" in self.start_time:
            sync_time = str(datetime.datetime.strptime(self.start_time.replace("/","-"),'%Y-%m-%d %H:%M'))
        else:
            sync_time = self.start_time
        # else:
        #     tdatetime = datetime.datetime.strptime(self.start_time.replace("/","-"), '%Y-%m-%d %H:%M')
        #     start_time = tdatetime
        #     if start_time.hour < 10:
        #         hour = "0{}".format(start_time.hour)
        #     else:
        #         hour = str(start_time.hour)

        #     if start_time.minute < 10:
        #         minute = "0{}".format(start_time.minute)
        #     else:
        #         minute = str(start_time.minute)
        
        #     sync_time = "{0}:{1}".format(hour, minute)
        
        # 制御計画データをフロアごとに調べる
        for control_data in self.control_data:
            cnt = 0
            # 制御計画データのイテレータを取得して変数を新しくコピー
            iter_control_data = copy.deepcopy(iter(control_data["control_data"]))
            # BEMSデータと同じ時間になるまでループ
            while True:
                one_data_time = next(iter_control_data)
                cnt += 1
                if sync_time == one_data_time["時間"]:
                    break
            if cnt > 1:
                # 元の制御計画データを指定した時間まで動かす
                for i in range(cnt-1):
                    next(control_data["control_data"])



    def integrate_files(self) -> dict:
        """ 読み込み設定データ全体のインテグレートを行う関数
        
            Returns:
            post_data [dict]: 全てのシミュレーション用データを格納した整形後データの辞書
        """

        # 最終的にシミュレーション実行ファイルへ返す全てのデータを格納した変数
        post_data = {
            "simulation_step" :self.simulation_step,
            "simulation_data" :[],
            "output_folder"   :self.output_folder,
        }

        # 初期値BEMSデータの読み込み
        self._import_bems_data()
        # 空調制御計画データの読み込み
        self.import_all_control_data()
        # 制御計画データとBEMSデータの同期
        self._sync_control_data()
        # フロアレイアウトデータの読み込み
        self.import_all_layout_data()
        # フロア内熱源データの読み込み
        self.import_heat_source_data()

        # 制御計画データのフロアごとのデータを確認
        for control in self.control_data:
            # レイアウトデータのフロアごとのデータを確認
            for layout in self.layout_data:
                # 初期BEMSデータのフロアごとのデータを確認
                for init_bems in self.init_bems_data:
                    # フロア内の熱源データの確認
                    for source in self.source_data:
                        # 各フロアの階層が一致していればシミュレーション実行可能としてシミュレーション実行用設定データを作成
                        if (control["floor"] == layout["floor"]) and (layout["floor"] == init_bems["floor"]) and (init_bems["floor"] == source["floor"]):
                            # 1フロア分のデータをまとめる
                            one_post_data = {
                                "floor"         : control["floor"],
                                "init_bems_data": init_bems,
                                "control_data"  : control["control_data"],
                                "layout_data"   : layout,
                                "source_data"   : source,
                            }
                            # 1フロアデータを配列へ追加
                            post_data["simulation_data"].append(one_post_data)

        return post_data



    def output_data(self,data: dict):
        """

        Args:
             data [array]: シミュレーションから返された結果を格納したデータ
        """        
        
        def _output_json(key: int,data: dict):
            """ key（ディレクトリ）とdataを受け取ってJsonファイルを出力するモジュール

            Args:
                key  [Int]  : ファイル名識別用の文字列でフロアが入る
                data [array]: シミュレーション結果の辞書
            """            
            
            f_json = open('{0}/result{1}.json'.format(self.output_folder,key),'w')
            json.dump(data,f_json,indent=4)
            
            

        def _output_complement_data(key,data: dict):
            """ BEMSに合わせた保管用データを作成するモジュール

            Args:
                key  [Int]  : ファイル名識別用の文字列でフロアが入る
                data [array]: シミュレーション結果の辞書
            """            
            
            # result_arr = sorted(data, key=lambda x: x['ac_id'])
            columns = ["時間"]
            values = []
            # シミュレーション結果全体から必要なデータのみを抽出する
            for value in data:
                per_value = {}
                per_value["時間"] = value["timestamp"]
                for i in value["agent_list"]:
                    # 空調のデータのみ抽出
                    if "ac_id" in i:
                        # 吸込温度を取り出す
                        if not i["ac_id"]+"吸込温度" in columns:
                            columns.append(i["ac_id"]+"吸込温度")
                        per_value[i["ac_id"]+"吸込温度"] = i["observe_temp"]
                values.append(per_value)
            
            # 整形した保管用データを指定先ディレクトリに書き出す
            with open('{0}cmp/result{1}.csv'.format(self.output_folder,key), 'w',encoding=self.encoding,newline="") as csv_file:
                fieldnames = columns
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in values:
                    writer.writerow(row)
                    
          
                    
        # シミュレーションデータのフロアと結果データを渡す
        for result in data:
            _output_json(result[0],result[1])
            _output_complement_data(result[0],result[1])

