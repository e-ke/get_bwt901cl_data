import datetime
import os
from time import sleep, time
import threading

from class_bwt901cl import BWT901CL

class SensorDataLogger:
    def __init__(self, sensor1_port, sensor2_port):
        self.sensor1 = BWT901CL(sensor1_port)
        self.sensor2 = BWT901CL(sensor2_port)
        self.filename = ''
        self.header = ''
        self.output_interval = 0.1  # デフォルトの出力間隔を0.1秒に設定
        
    # 出力間隔を設定するメソッド
    def set_output_interval(self, interval):
        self.output_interval = interval
    
    # CSVファイルの初期化("csv/YYMMDD/"に"YYMMDD_HHMMSS_sensor_raw.csv"を作成)
    def init_csv(self):
        current_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        # folder_path = f'csv/{current_time[:6]}/'
        folder_path = f'../csv/{current_time[:6]}/'
        os.makedirs(folder_path, exist_ok=True)
        self.filename = f'{folder_path}{current_time}_sensor_data.csv'
        self.header = 'Time,AccX1,AccY1,AccZ1,AccX2,AccY2,AccZ2,AngVelX1,AngVelY1,AngVelZ1,AngVelX2,AngVelY2,AngVelZ2,AngX1,AngY1,AngZ1,AngX2,AngY2,AngZ2\n'

    # Ctrl+Cでの終了時処理
    def handle_keyboard_interrupt(self, stop_event, thread1, thread2):
        print("KeyboardInterrupt: stop process")
        stop_event.set()
        thread1.join()
        thread2.join()
        self.sensor1.stop()
        self.sensor2.stop()
        # ファイル名が設定されている場合のみファイルをフラッシュ
        if self.filename:
            with open(self.filename, 'a', buffering=1) as file:
                file.flush()
        print()

    # センサーデータの取得(各スレッドで利用)
    def read_sensor_data(self, sensor, stop_event):
        while not stop_event.is_set():
            sensor._readData()
        print("thread end:", sensor.port)

    # スレッドの準備
    def setup_threads(self, stop_event):
        thread1 = threading.Thread(target=self.read_sensor_data, args=(self.sensor1, stop_event))
        thread2 = threading.Thread(target=self.read_sensor_data, args=(self.sensor2, stop_event))
        thread1.start()
        thread2.start()
        return thread1, thread2

    # 各スレッドから取得して保持しているセンサーデータの取得
    def get_sensor_data(self):
        s1_Acc = self.sensor1.getAccel()
        s2_Acc = self.sensor2.getAccel()
        s1_angVel = self.sensor1.getAngularVelocity()
        s2_angVel = self.sensor2.getAngularVelocity()
        s1_ang = self.sensor1.getAngle()
        s2_ang = self.sensor2.getAngle()
        return s1_Acc, s2_Acc, s1_angVel, s2_angVel, s1_ang, s2_ang

    # 実行用(データの表示(動作確認用)とcsv出力)
    def run(self):
        self.init_csv()

        with open(self.filename, 'w', buffering=1) as file:
            file.write(self.header)

            stop_event = threading.Event()
            thread1, thread2 = self.setup_threads(stop_event)

            last_flush_time = time()
            try:
                while True:
                    s1_Acc, s2_Acc, s1_angVel, s2_angVel, s1_ang, s2_ang = self.get_sensor_data()
                    
                    # センサーデータを表示するためのコードを追加
                    data_format = "{:8.3f}"
                    s1_Acc_str = " ".join(data_format.format(a) for a in s1_Acc)
                    s2_Acc_str = " ".join(data_format.format(a) for a in s2_Acc)
                    s1_angVel_str = " ".join(data_format.format(a) for a in s1_angVel)
                    s2_angVel_str = " ".join(data_format.format(a) for a in s2_angVel)
                    s1_ang_str = " ".join(data_format.format(a) for a in s1_ang)
                    s2_ang_str = " ".join(data_format.format(a) for a in s2_ang)

                    print(f"Acc1:{s1_Acc_str}|Acc2:{s2_Acc_str}", end="||")
                    print(f"AngVel1:{s1_angVel_str}|AngVel2:{s2_angVel_str}", end="||")
                    print(f"Ang1:{s1_ang_str}|Ang2:{s2_ang_str}")
                    
                    time_stamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    file.write(f'{time_stamp},'
                               f'{s1_Acc[0]},{s1_Acc[1]},{s1_Acc[2]},'
                               f'{s2_Acc[0]},{s2_Acc[1]},{s2_Acc[2]},'
                               f'{s1_angVel[0]},{s1_angVel[1]},{s1_angVel[2]},'
                               f'{s2_angVel[0]},{s2_angVel[1]},{s2_angVel[2]},'
                               f'{s1_ang[0]},{s1_ang[1]},{s1_ang[2]},'
                               f'{s2_ang[0]},{s2_ang[1]},{s2_ang[2]}\n')

                    if time() - last_flush_time > 30:
                        file.flush()
                        last_flush_time = time()

                    sleep(self.output_interval) # 出力頻度

            except KeyboardInterrupt:
                self.handle_keyboard_interrupt(stop_event, thread1, thread2)