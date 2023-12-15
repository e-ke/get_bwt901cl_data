# get_bwt901_data
2台のBWT901CLセンサーのデータを同時に読み取るプログラム。(windows)
- 出力(表示)データ：加速度, 角速度, 角度
- 出力(表示)形式：
  - Time, AccX1, AccY1, AccZ1, AccX2, AccY2, AccZ2, AngVelX1, AngVelY1, AngVelZ1, AngVelX2, AngVelY2, AngVelZ2, AngX1, AngY1, AngZ1, AngX2, AngY2, AngZ2

### 参考
- https://qiita.com/Dorebom/items/19b69293b811da2f7851

### 使い方
1. srcフォルダをDL
2. main.pyをテキストエディタで開き、"COM5","COM8"の部分を自身のセンサーのポートに変更
4. コマンドプロンプト等で"python main.py"を実行
5. 接続完了後, 指示に従って-1または1を入力
  - -1の場合：取得したデータの表示のみを行う
  - 1の場合：データをcsv出力
6. Ctrl+Cでプログラムを終了

### main.py
- 実行用
- 2台のセンサーのポートを指定
- テスト：データ表示のみ
- 実行：データcsv書き込み
- プログラム停止方法：Ctrl+C

### class_sensor_data_logger.py
- set_output_interval() : 出力頻度を変更
