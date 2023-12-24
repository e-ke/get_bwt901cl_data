import os
import tkinter as tk
from tkinter import filedialog
from class_sensordataplotter import SensorDataPlotter

# analyzeディレクトリ
base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target_directory = os.path.join(base_directory, "time_filtered")

# Tkinterのファイル選択ウィンドウを開く
root = tk.Tk()
root.withdraw()  # Tkウィンドウを表示しない
csv_file_path = filedialog.askopenfilename(initialdir=target_directory,
                                           title="Select file",
                                           filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))

if csv_file_path:
    print(csv_file_path)
    plotter = SensorDataPlotter(csv_file_path)

    # グラフの表示
    plotter.display_acceleration(1)
    plotter.display_angular_velocity(1)
    # plotter.display_angle(1)

    # センサー2のグラフも表示
    # plotter.display_acceleration(2)
    # plotter.display_angular_velocity(2)
    # plotter.display_angle(2)
else:
    print("ファイルが選択されませんでした。")
