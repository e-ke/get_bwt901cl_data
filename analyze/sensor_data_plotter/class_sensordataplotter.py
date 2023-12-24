import os
import pandas as pd
import matplotlib.pyplot as plt

class SensorDataPlotter:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
        os.makedirs(self.output_file_path, exist_ok=True)  # imgフォルダを作成
        self.df = self.load_data()

    def load_data(self):
        df = pd.read_csv(self.csv_file_path)
        df['Time'] = pd.to_datetime(df['Time'], format="%H:%M:%S.%f")
        return df

    # グラフ保存
    def save_plot(self, data_type, sensor_id):
        base_name = os.path.basename(self.csv_file_path)
        file_name, _ = os.path.splitext(base_name)
        subfolder_name = '_'.join(file_name.split('_')[:2])
        save_dir = os.path.join(self.output_file_path, subfolder_name)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{file_name}_{data_type}{sensor_id}.png")
        plt.savefig(save_path)

    # グラフ作成
    def create_plot(self, data_columns, title, ylabel, sensor_id, data_type, save=False, display=False):
        plt.figure(figsize=(10, 6))
        colors = ['red', 'green', 'blue']
        rms_values = []

        for col, color in zip(data_columns, colors):
            plt.plot(self.df['Time'], self.df[col], label=col, color=color, linewidth=1)
            rms = (self.df[col]**2).mean()**0.5
            rms_values.append(rms)

        plt.xlabel('Time')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(loc='upper left')
        rms_text = f"RMS: X={rms_values[0]:.2f}, Y={rms_values[1]:.2f}, Z={rms_values[2]:.2f}"
        plt.figtext(0.5, 0.01, rms_text, ha="center", fontsize=9)

        if save:
            self.save_plot(data_type, sensor_id)
        if display:
            plt.show()
            self.print_all_rms()  # RMSを表示
        plt.close()

    def plot_data(self, data_columns, title, ylabel, sensor_id, data_type):
        self.create_plot(data_columns, title, ylabel, sensor_id, data_type, save=True)

    def display_plot(self, data_columns, title, ylabel, sensor_id, data_type):
        self.create_plot(data_columns, title, ylabel, sensor_id, data_type, display=True)

    # RMS計算
    def calculate_rms(self, sensor_id, data_type):
        if data_type == 'acc':
            data_columns = [f'AccX{sensor_id}', f'AccY{sensor_id}', f'AccZ{sensor_id}']
        elif data_type == 'angvel':
            data_columns = [f'AngVelX{sensor_id}', f'AngVelY{sensor_id}', f'AngVelZ{sensor_id}']
        else:
            raise ValueError("Invalid data type. Choose 'acc' for acceleration or 'angvel' for angular velocity.")

        rms_values = []
        for col in data_columns:
            rms = (self.df[col]**2).mean()**0.5
            rms_values.append(rms)

        print(f"Sensor {sensor_id} {data_type.upper()} RMS: {tuple(rms_values)}")

    def print_all_rms(self):
        print(f"Data File: {os.path.basename(self.csv_file_path)}")
        # センサー1
        self.calculate_rms(1, 'acc') 
        self.calculate_rms(1, 'angvel')
        # センサー2
        self.calculate_rms(2, 'acc') 
        self.calculate_rms(2, 'angvel')
        print()
        
        
    # グラフ保存
    def plot_acceleration(self, sensor_id):
        self.plot_data([f'AccX{sensor_id}', f'AccY{sensor_id}', f'AccZ{sensor_id}'],
                       f'Sensor {sensor_id} Acceleration Data', 'Acceleration', sensor_id, 'Acc')
    def plot_angular_velocity(self, sensor_id):
        self.plot_data([f'AngVelX{sensor_id}', f'AngVelY{sensor_id}', f'AngVelZ{sensor_id}'],
                       f'Sensor {sensor_id} Angular Velocity', 'Angular Velocity', sensor_id, 'AngVel')
    def plot_angle(self, sensor_id):
        self.plot_data([f'AngX{sensor_id}', f'AngY{sensor_id}', f'AngZ{sensor_id}'],
                       f'Sensor {sensor_id} Angles', 'Angle', sensor_id, 'Ang')
    # グラフ表示
    def display_acceleration(self, sensor_id):
        self.display_plot([f'AccX{sensor_id}', f'AccY{sensor_id}', f'AccZ{sensor_id}'],
                          f'Sensor {sensor_id} Acceleration Data', 'Acceleration', sensor_id, 'Acc')
    def display_angular_velocity(self, sensor_id):
        self.display_plot([f'AngVelX{sensor_id}', f'AngVelY{sensor_id}', f'AngVelZ{sensor_id}'],
                          f'Sensor {sensor_id} Angular Velocity', 'Angular Velocity', sensor_id, 'AngVel')
    def display_angle(self, sensor_id):
        self.display_plot([f'AngX{sensor_id}', f'AngY{sensor_id}', f'AngZ{sensor_id}'],
                          f'Sensor {sensor_id} Angles', 'Angle', sensor_id, 'Ang')