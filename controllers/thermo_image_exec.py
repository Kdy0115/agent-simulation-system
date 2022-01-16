import cv2
import os
import numpy as np

video_path = "docs/パラメータ同定実験結果/研究室内自然対流/20220103_自然対流同定用動画.MP4"

def m_slice(path):
    movie = cv2.VideoCapture(path)                  # 動画の読み込み
    Fs = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))   # 動画の全フレーム数を計算
    fps = movie.get(cv2.CAP_PROP_FPS)               # フレーム数
    
    out_dir = "data/thermo_img/"                    # 出力先フォルダ
    
    num = 0
    cap_time = 0
    while cap_time < Fs:
        cap_time = num * 10 * fps
        file_path = out_dir + "result_{}.jpg".format(num*10)
        movie.set(cv2.CAP_PROP_POS_FRAMES, cap_time)
        ret, frame = movie.read()
        if ret:
            cv2.imwrite(file_path, frame)
        num += 1
        print(cap_time,Fs)


# 関数実行：引数=（ファイル名のパス、保存先のフォルダパス、ステップ数、静止画拡張子）
#m_slice(video_path)

img = cv2.imread('data/thermo_img/result_0.jpg')
print(img)
print(len(img[0]))
print(len(img))

