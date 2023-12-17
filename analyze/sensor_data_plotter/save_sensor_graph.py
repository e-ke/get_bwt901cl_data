import os
from class_sensordataplotter import SensorDataPlotter

# ベースディレクトリとターゲットディレクトリの設定
base_directory = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))  # analyzeディレクトリ
target_directory = os.path.join(base_directory, 'time_filtered')

# 指定ディレクトリ内のすべてのcsvファイルをリストアップ
csv_files = [os.path.join(target_directory, f) for f in os.listdir(target_directory) if f.endswith('.csv')]


# 各ファイルに対して処理を行う
for csv_file_path in csv_files:
    plotter = SensorDataPlotter(csv_file_path)
    
    # # センサー1の加速度、角速度、角度のグラフの保存
    plotter.plot_acceleration(1)
    plotter.plot_angular_velocity(1)
    # plotter.plot_angle(1)

    # # センサー2の加速度、角速度、角度のグラフの保存
    plotter.plot_acceleration(2)
    plotter.plot_angular_velocity(2)
    # plotter.plot_angle(2)