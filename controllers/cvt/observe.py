# -*- coding: utf-8 -*-

""" 温度取りローデータ整形モジュール
    評価用の温度取りデータのローデータを整形するプログラム

Todo:
    * ./data/src/に温度取りのローデータを配置する
    * 現状はcsvファイル形式の扱いを前提としているのでcsvファイルとして操作する
"""

# python lib
import pandas as pd
import glob
from datetime import datetime as dt
import sys
import os

sys.path.append(os.getcwd())

# utils
from controllers import error,env,functions


# 読み込むローデータファイルパス
import_dir_path = "data/src/温度取り/温度とり2021年9月/温度とり2021年9月/"
# 出力先ファイルパス
output_dir_path = "data/evaluation/observe/all/"
# 出力用ファイル名
output_file_name = "observe1.csv"

# 時間カラム名
time_colummn_name = "date"

def to_datetime_format(df):
    """ 読み込んだDataFrameの時間型を標準型に変換する関数
        YYYY-MM-DD hh:mm:ssのフォーマットに変換
        
    Args:
        df [DataFrame]: 変換を行ったDataFrame型のデータ
    """ 
    
    if time_colummn_name in df.columns:
        time_arr = []
        for i in range(len(df)):
            # print(df.iloc[i]["date"].replace("/","-").replace("'",":")[:-3])
            time_arr.append(dt.strptime(df.iloc[i][time_colummn_name].replace("/","-").replace("'",":")[:-3], '%Y-%m-%d %H:%M'))
        df[time_colummn_name] = time_arr

        return df
    else:
        sys.exit(error.DATA_CLUMN_NAME_REFFERENCE_ERROR)



def merge_rows(df_arr: list,start: int,end: int):
    """ 同一日時のデータをマージする関数
        設定では温度取りローデータのディレクトリ内には複数のデータに分割されてファイルが配置されている
        同じ日時のデータに合わせるために指定した範囲でデータをまとめる作業を行う
        デフォルトでは4ファイルごと

    Args:
        df_arr [list] : 1ファイルごとのDataFrameが入ったリスト
        start [int]   : 開始時の添字
        end [int]     : 終了時の添字

    Returns:
        result_df_arr [DataFrame]: マージしたDataFrame
    """    
    result_df_arr = pd.merge(df_arr[start],df_arr[start+1],on="date")
    for i in range(start+2,end):
        result_df_arr = pd.merge(result_df_arr,df_arr[i],on="date")
    
    print(result_df_arr.head())
        
    return result_df_arr



def add_rows_data(df,df1):
    """ 2つのDataFrameを縦に結合する関数
        日程ごとに分けられていたデータを全て一つにマージするために使用
        
    Args:
        df [DataFrame] : 結合元のDataFrameのデータ
        df1 [DataFrame]: 結合される側のDataFrameのデータ

    Returns:
        [DataFrame]: 結合したDataFrameのデータ
    """    
    for i in range(len(df)):
        if df1.iloc[0][time_colummn_name] == df.iloc[i][time_colummn_name]:
            
            return pd.concat([df.iloc[:i],df1])
        

df_arr = []
files = glob.glob("{}*.csv".format(import_dir_path))
for i in files:
    df_arr.append(pd.read_csv(i,encoding="shift-jis"))

for i in range(len(df_arr)):
    to_datetime_format(df_arr[i])
    
edit_df_arr = []
for i in range(3):
    edit_df_arr.append(merge_rows(df_arr,4*i,4*(i+1)))
    
for i in range(len(edit_df_arr)):
    if i == 0:
        result_df = add_rows_data(edit_df_arr[0],edit_df_arr[1])
        i += 1
    else:
        result_df = add_rows_data(result_df,edit_df_arr[i])
        
print_message =  """全てのファイルをマージしました。
データカラム
--------------------------------------------------
{0}
--------------------------------------------------
先頭行データ
--------------------------------------------------
{1}
--------------------------------------------------
最後尾データ
--------------------------------------------------
{2}
--------------------------------------------------
""".format(result_df.columns,result_df.head(),result_df.tail())
print(print_message)

new_columns = ["時間"]
for i in result_df.columns:
    if i != "date":
        new_columns.append(i+"_実測値")
result_df.columns = new_columns

functions.create_dir(output_dir_path)
result_df.to_csv(
    (output_dir_path + output_file_name),
    encoding=env.glbal_set_encoding,
    index=None
    )