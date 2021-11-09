# -*- coding: utf-8 -*-

""" 共通の関数を定義したファイル

    共通関数で定義する理由として他のクラスやファイルからも利用できる依存しないものはこのファイルに定義する
"""

# ライブラリ
import os

def create_dir(path: str) -> None:
    """ ディレクトリ作成関数

    Args:
        path [str]: 作成するディレクトリパスの文字列
    """    
    if not os.path.exists(path):
        os.makedirs(path)
        print("Create {} directory".format(path))
        
        
        
def format_time(str_time: str) -> str:
    """ 渡された時間文字列をYYYY/MM/DD hh:mm:00に変換する関数

    Args:
        str_time [str]: 文字列型の時間　想定フォーマットはYYYY/MM/DD hh:mm:00
        引数の名前 (:obj:`引数の型`, optional): 引数の説明.

        Returns:
        戻り値の型: 戻り値の説明 (例 : True なら成功, False なら失敗.)

    """   
            
    # shift-jisではないフォーマットのとき
    if len(str_time) == 19:
        # shift-jis形式の文字列に変換
        str_time = str_time.replace("-","/")
        return str_time
    # shift-jis形式のときで文字コードの数字に不足があるとき
    else:
        time_str = str_time.split()
        # 文字列を/で分割する（日付部分）
        date_arr = time_str[0].split("/")
        # 年数を取得
        year = date_arr[0]
        # 月を取得（0が無い場合は先頭に付加）
        month = date_arr[1] if len(date_arr[1]) > 1 else "0"+date_arr[1]
        # 日を取得（0が無い場合は先頭に付加）
        day = date_arr[2] if len(date_arr[2]) > 1 else "0"+date_arr[2]

        # 文字列を:で分割する（時間部分）
        time_arr = time_str[1].split(":")
        # 時間を取得（0が無い場合は先頭に付加）
        hour = time_arr[0] if len(time_arr[0]) > 1 else "0"+time_arr[0]
        # 分を取得（0が無い場合は先頭に付加）
        minutes = time_arr[1] if len(time_arr[1]) > 1 else "0"+time_arr[1]

        # YYYY/MM/DD hh:mm:00に変換
        return "{0}/{1}/{2} {3}:{4}:00".format(year,month,day,hour,minutes)