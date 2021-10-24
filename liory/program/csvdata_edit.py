#!python3.5
# Artisoc, Python, BEMSの3種類の吸い込み温度を比較するプログラム

# ライブラリ
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import os

# Pythonファイルパス
pypath = 'out/result_2021_07_2_fix/cmp/result5.csv'
# Artisocファイルパス
artpath = 'artisoc/07-02/result.xlsx'
# BEMSデータファイルパス

sourcepath = 'data/evaluation/base/2021_7_2/all_bems_data5.csv'

# Pythonファイルをインポート
pydf = pd.read_csv(pypath,encoding="shift-jis")
# Artisocファイルをインポート
artdf = pd.read_excel(artpath,encoding="shift-jis",usecols=[0,4,5,6,7,8,9,10,11,12,13])
# BEMSファイルをインポート
sourcedf = pd.read_csv(sourcepath,encoding="shift-jis")


def adjust_bems_columns(df):
    """ BEMSファイルのカラムを調整する関数
    デフォルトだとPython側のカラム名と被ってしまうため異なる名前を付ける

    Args:
        df ([DataFrame]): BEMSデータを読み込んだDataFrame

    Returns:
        df_source_new_columns: カラムを修正したBEMSデータのDataFrame
    """

    _new_columns = []
    # 吸込温度と時間だけを抽出し配列へ格納
    for column in df.columns:
        if "吸込温度" in column or "時間" in column:
            _new_columns.append(column)

    # 元のデータから時間と吸込温度のみを抽出
    df_source_new_columns = df[_new_columns]
    
    # 時間以外のカラム（吸込温度）に_bemsをつけてrename
    for column in df_source_new_columns:
        if not column == "時間":
            df_source_new_columns = df_source_new_columns.rename(columns={column:column+"_bems"})
        
    return df_source_new_columns


def uniform_time(df_py, df_art, df_bems):
    """ 全てのデータについて一番少ない数のデータに合わせる
    欠損値への対応も含めるためNanが一つでも含まれていればその行は削除

    Args:
        df_py ([DataFrame]): pythonの結果データを読み込んだDataFrame
        df_art ([DataFrame]): Artisocの結果データを読み込んだDataFrame
        df_bems ([DataFrame]): BEMSのデータを読み込んだDataFrame

    Returns:
        df_merge_all [DataFrame]: 全てのデータを統合して時間を統一したプログラム        
    """    
    
    # python,bemsの時間をDate型へ変換（文字列によるバグを検出するため）
    df_py["時間"] = pd.to_datetime(df_py['時間'], format='%Y-%m-%d %H:%M:')
    df_bems["時間"] = pd.to_datetime(df_bems['時間'], format='%Y-%m-%d %H:%M:')

    # pythonの基準日時を取得
    _base_time = df_py.iloc[0]["時間"]
    _base_date = "{0}-{1}-{2} ".format(_base_time.year,_base_time.month,_base_time.day)

    # artisocの時間をdatetime型に変換するために文字列で標準形に変換
    df_art["時間"] =  [_base_date]*len(df_art) + df_art["時間"]
    df_art["時間"] = pd.to_datetime(df_art["時間"],format='%Y-%m-%d %H:%M:')
    
    # Artisocのデータに合わせる場合
    if len(df_art) <= len(df_py) and len(df_art) <= len(df_bems):
        _df_merge_1 = pd.merge(df_art, df_py, how="inner", on="時間")
        df_merge_all = pd.merge(_df_merge_1,df_bems,how="inner", on="時間")
        print('データ数が不足しています。Artisocのデータ数に合わせて出力します。')
    # pythonのデータに合わせる場合
    elif len(df_py) <= len(df_art) and len(df_py) <= len(df_bems):
        _df_merge_1 = pd.merge(df_py,df_art, how="inner", on="時間")
        df_merge_all = pd.merge(_df_merge_1,df_bems,how="inner", on="時間")
        print('データ数が不足しています。Pythonのデータ数に合わせて出力します。')
    # BEMSデータに合わせる場合
    else:
        _df_merge_1 = pd.merge(df_bems,df_art, how="inner", on="時間")
        df_merge_all = pd.merge(_df_merge_1,df_py,how="inner", on="時間")
        print('データ数が不足しています。BEMSのデータ数に合わせて出力します。')
    
    return df_merge_all


def create_graph_data(df) -> (dict, dict):
    """ グラフ描画用データを作成する関数

    Args:
        df ([DataFrame]): python,Artisoc,BEMSデータをインテグレートしたDataFrame

    Returns:
        simple_data [dict]: python,Artisoc,BEMSをそれぞれ時系列で格納した辞書型のデータ
        gap_data    [dict]: (BEMS-python),(BEMS-Artisoc)をそれぞれ時系列で格納した辞書型のデータ
    """    

    # 空調のIDを設定（0～9）
    _id = [i for i in range(10)]
    # 3種類のデータ格納用辞書
    simple_data = {}
    # 比較データ格納用辞書
    gap_data = {}

    # IDを一つずつ取得
    for n in _id:
        simple_data[n] = {
            # 時間
            "timestamp" : df["時間"].values,
            # Artisocデータ（IDが一つずれているため加算）
            "artisoc"   : df["観測温度{}".format(n+1)].values,
            # Pythonデータ
            "python"    : df["5f{}吸込温度".format(n)].values,
            # BEMSデータ
            "bems"      : df["5f{}吸込温度_bems".format(n)].values,
        }

        gap_data[n]    = {
            # 時間
            "timestamp": df["時間"].values,
            # BEMS - Artiscのデータ
            "artisoc"  : (df["5f{}吸込温度_bems".format(n)] - df["観測温度{}".format(n+1)]).values,
            # BEMS - pythonのデータ
            "python"   : (df["5f{}吸込温度_bems".format(n)] - df["5f{}吸込温度".format(n)]).values
        }
    
    return (simple_data, gap_data)

def output_graph(fig,ax_set_list,kind):
    """ 作成したグラフ描画用データを画像として保存する関数

    Args:
        fig ([Figure]): グラフキャンバス定義データ
        ax_set_list ([list]): グラフ描画用データを格納したリスト
        kind ([str]): グラフ種別
    """    

    # 1つずつ（IDずつ）データを取得
    for c,item in enumerate(ax_set_list):
        # 凡例の数を取得（simple_dataの場合は3,gap_dataの場合は2）
        for n in range(len(item[1])):
            item[0].plot(item[2][0],item[2][n+1],label=item[1][n])
        item[0].legend(loc='upper left',fontsize=12)

        # グラフ自体ののタイトルと軸のタイトルを設定
        item[0].set_xlabel("時間[min]",fontsize=14)
        if kind == "simple_data":
            item[0].set_title("比較結果{}".format(c),fontsize=14)
            item[0].set_ylabel("温度[℃]",fontsize=14)
            item[0].set_ylim([18,30])
        else:
            item[0].set_title("差分比較結果{}".format(c),fontsize=14)
            item[0].set_ylabel("実測値-予測値",fontsize=14)
            item[0].set_ylim([-5,5])

    # 位置情報の設定をグラフに反映
    plt.subplots_adjust(wspace=0.2, hspace=0.3)

    # 日時をディレクトリ名に設定
    time = ax_set_list[0][2][0][0].astype('datetime64[D]')
    dir_path = "liory/out/{}/".format(time)
    # ディレクトリがなければ作成
    os.makedirs(dir_path,exist_ok=True)
    # 作成したグラフを保存
    fig.savefig(dir_path + "{}.png".format(kind))

def create_graphs(data):
    """ python版グラフ描画用データを作成する関数

    Args:
        data ([dict]): simple_dataかgap_dataの辞書
    """    

    # グラフのキャンバスの定義
    fig = plt.figure(figsize=(20,20))
    # グラフ描画用データの格納リスト
    ax_set_list = []
    # y座標の位置調整用値
    y_base = 1.0

    # simple_dataの場合の処理
    if len(data[0]) == 4:
        # キーの個数がIDに対応
        for i in data.keys():
            # グラフの凡例用の名前
            l_1 = "artisoc" + str(i)
            l_2 = "python"  + str(i)
            l_3 = "実測値"  + str(i)

            # 10個分のグラフを出力するための位置調整
            x_base = 0.05 if i % 2 == 0 else 0.55
            width = 0.4
            height = 0.12
            y_base -= 0.185 if i % 2 == 0 else 0    
            ax_set = fig.add_axes([x_base,y_base,width,height])

            # 各データの格納
            x  = data[i]["timestamp"]
            y1 = data[i]["artisoc"]
            y2 = data[i]["python"]
            y3 = data[i]["bems"]

            # 格納用リストにデータを入れる
            ax_set_list.append([ax_set,(l_1,l_2,l_3),(x,y1,y2,y3)])

        # グラフ種別を格納
        graph_kind = "simple_data"
    
    # gap_dataの場合
    else:
        for i in data.keys():
            l_1 = "artisoc" + str(i)
            l_2 = "python"  + str(i)

            x_base = 0.05 if i % 2 == 0 else 0.55
            width = 0.4
            height = 0.12
            y_base -= 0.185 if i % 2 == 0 else 0        
            ax_set = fig.add_axes([x_base,y_base,width,height])

            x  = data[i]["timestamp"]
            y1 = data[i]["artisoc"]
            y2 = data[i]["python"]

            ax_set_list.append([ax_set,(l_1,l_2),(x,y1,y2)])
        graph_kind = "gap_data"
        
    # 保存したデータでグラフを描画して画像を保存
    output_graph(fig,ax_set_list,graph_kind)
    

def main(sourcedf,pydf,artdf):
    """ 全体実行用関数
    外部実行を考慮して関数化

    Args:
        sourcedf ([DataFrame]): BEMSデータのDataFrame
        pydf ([DataFrame]): pythonデータのDataFrame
        artdf ([DataFrame]): ArtisocデータのDataFram

    Returns:
        simple_data [dict]: python,Artisoc,BEMSをそれぞれ時系列で格納した辞書型のデータ
        gap_data    [dict]: (BEMS-python),(BEMS-Artisoc)をそれぞれ時系列で格納した辞書型のデータ
    """    

    # BEMSデータのカラムの調整
    df_new_source = adjust_bems_columns(sourcedf)

    # 全データのインテグレート
    df_integrate = uniform_time(pydf,artdf,df_new_source)

    # 時間以外のデータの文字列を浮動小数点に変換
    for column in df_integrate.columns:
        if column != "時間":
            df_integrate[column] = df_integrate[column].astype("float")

    # 変換したデータを返す
    return create_graph_data(df_integrate)

result_data = main(sourcedf,pydf,artdf)

# simple_dataのグラフ出力（python）
create_graphs(result_data[0])
# gap_dataのグラフ出力（python）
create_graphs(result_data[1])