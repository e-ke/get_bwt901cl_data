import os
from class_sensordataplotter import SensorDataPlotter

# ベースディレクトリとターゲットディレクトリの設定
base_directory = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))  # analyzeディレクトリ
target_directory = os.path.join(base_directory, "time_filtered")
csv_file_path = os.path.join(target_directory, 
                "231209_104621_sensor_data_timeFiltered.csv")  # ファイル名を指定



plotter = SensorDataPlotter(csv_file_path)

# センサー1の加速度、角速度、角度のグラフの表示
plotter.display_acceleration(1)
plotter.display_angular_velocity(1)
# plotter.display_angle(1)

# センサー2の加速度、角速度、角度のグラフの表示
# plotter.display_acceleration(2)
# plotter.display_angular_velocity(2)
# plotter.display_angle(2)
