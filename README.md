# get_bwt901_data
2台のBWT901CLセンサーのデータを同時に読み取るプログラム。(windows) + グラフ化
- 出力データ：加速度, 角速度, 角度
- 出力形式：
  - Time,AccX1,AccY1,AccZ1,AccX2,AccY2,AccZ2,AngVelX1,AngVelY1,AngVelZ1,AngVelX2,AngVelY2,AngVelZ2,AngX1,AngY1,AngZ1,AngX2,AngY2,AngZ2
    - Time：データ取得時刻(hh:mm:ss.fff)
    - Acc：加速度
    - AngVel：角速度
    - Ang：角度

### 参考
- https://qiita.com/Dorebom/items/19b69293b811da2f7851

### 必要モジュール
- pyserial
- pandas
- matplotlib

### 使い方
1. src > main.py > "COM5","COM8"の部分を自身のセンサーのポートに変更
2. "main.py"を実行
3. Ctrl+Cでプログラムを終了
4. YYMMDD_hhmmdd_sensor_data.csvがcsv>YYMMDD>に出力される。

### 出力データのグラフ化
Analyze > 
- filter_by_time.py
  - csvデータの開始時刻と終了時刻を設定（開始～終了時刻外のデータを削除）
    - プログラム内 filter_dict を適宜変更
  - 出力先：time_filtered > YYMMDD > ~_time_filtered.csv
- sensor_data_plotter
  - グラフ化とRMSの計算を行う。
  - save_sensor_graph
    - time_filtered > YYMMDD 内のcsvデータをグラフ化して保存
      - プログラム内の time_filtered//YYMMDD 部分を適宜変更
    - 出力先：sensordataplotter > img > 
  - show_sensor_graph
    - csvデータを指定し、グラフとして表示(保存なし)
