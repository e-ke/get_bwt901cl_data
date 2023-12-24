import os 
import pandas as pd


filter_dict = {
    # csvフォルダ内のファイルパス: {開始時刻, 終了時刻}
    "sample\\231213_181935_sensor_data.csv": {"start": "18:19:37.430", "end": "18:19:41.310"},
    "sample\\231213_182054_sensor_data.csv": {"start": "18:20:56.000", "end": "18:21:01.190"},
}


def filter_by_time(csv_filename, st_time, ed_time, output_dir):
    # ファイル名を抽出
    file_name = csv_filename.rsplit('.', 1)[0].rsplit('\\', 1)[-1]
    # YYMMDDのサブディレクトリを生成
    yymmdd = file_name.split('_')[0]
    new_subdir = os.path.join(output_dir, yymmdd)
    os.makedirs(new_subdir, exist_ok=True)

    # CSVファイルを読み込む
    df = pd.read_csv(csv_filename, dtype=object)
    
    # 時間データの形式を変換
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format="%H:%M:%S.%f").dt.time
    
    # 時間の範囲を設定
    st_time = pd.to_datetime(st_time, format="%H:%M:%S.%f").time()
    ed_time = pd.to_datetime(ed_time, format="%H:%M:%S.%f").time()
    
    # 時間でフィルタリング
    filtered_df = df[(df.iloc[:, 0] >= st_time) & (df.iloc[:, 0] <= ed_time)].copy()
    
    # 時間列を文字列に変換
    filtered_df.iloc[:, 0] = filtered_df.iloc[:, 0].apply(lambda x: x.strftime("%H:%M:%S.%f")[:-3])
    
    # 新しいCSVファイル名を生成（新しいサブディレクトリに保存）
    new_csv_filename = os.path.join(new_subdir, file_name + "_timeFiltered.csv")
    
    # CSVファイルとして保存
    filtered_df.to_csv(new_csv_filename, index=False)

    return new_csv_filename


def main():
    # time_filtered ディレクトリを作成
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir_name = "time_filtered"
    output_dir = os.path.join(parent_dir, output_dir_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # CSVファイルのディレクトリを指定
    csv_dir = os.path.join(os.path.dirname(parent_dir), "csv")

    # 時間でフィルタリング
    for filename, time_range in filter_dict.items():
        full_path = os.path.join(csv_dir, filename)
        if os.path.exists(full_path):
            filter_by_time(full_path, time_range["start"], time_range["end"], output_dir)
            print(f"{filename} is filtered")
        else:
            print(f"ファイル {filename} が見つかりませんでした。")


if __name__ == "__main__":
    main()
    input("press Enter to exit")
