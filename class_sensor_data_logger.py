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

    # CSVファイルの初期化
    def init_csv(self):
        if not os.path.exists('csv'):
            os.makedirs('csv')

        current_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.filename = f'csv/{current_time}_sensor_data.csv'
        self.header = 'Time, AccX1, AccY1, AccZ1, AccX2, AccY2, AccZ2, AngVelX1, AngVelY1, AngVelZ1, AngVelX2, AngVelY2, AngVelZ2, AngX1, AngY1, AngZ1, AngX2, AngY2, AngZ2\n'

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

    # テスト用(データの表示のみ(csv出力なし))
    def run_test(self):
        stop_event = threading.Event()
        thread1, thread2 = self.setup_threads(stop_event)

        try:
            while True:
                s1_Acc, s2_Acc, s1_angVel, s2_angVel, s1_ang, s2_ang = self.get_sensor_data()
                # 各データを整列して表示
                data_format = "{:8.3f}"
                s1_Acc_str = " ".join(data_format.format(a) for a in s1_Acc)
                s2_Acc_str = " ".join(data_format.format(a) for a in s2_Acc)
                s1_angVel_str = " ".join(data_format.format(a) for a in s1_angVel)
                s2_angVel_str = " ".join(data_format.format(a) for a in s2_angVel)
                s1_ang_str = " ".join(data_format.format(a) for a in s1_ang)
                s2_ang_str = " ".join(data_format.format(a) for a in s2_ang)

                print(f"Acc1:{s1_Acc_str}|Acc2:{s2_Acc_str}",end="||")
                print(f"AngVel1:{s1_angVel_str}|AngVel2:{s2_angVel_str}",end="||")
                print(f"Ang1:{s1_ang_str}|Ang2:{s2_ang_str}")

                sleep(0.1) # 出力頻度
        except KeyboardInterrupt:
            self.handle_keyboard_interrupt(stop_event, thread1, thread2)

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
                    print(end=".")  # 動作確認用
                    
                    time_stamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    file.write(f'{time_stamp}, '
                               f'{s1_Acc[0]},{s1_Acc[1]},{s1_Acc[2]},'
                               f'{s2_Acc[0]},{s2_Acc[1]},{s2_Acc[2]},'
                               f'{s1_angVel[0]},{s1_angVel[1]},{s1_angVel[2]},'
                               f'{s2_angVel[0]},{s2_angVel[1]},{s2_angVel[2]},'
                               f'{s1_ang[0]},{s1_ang[1]},{s1_ang[2]},'
                               f'{s2_ang[0]},{s2_ang[1]},{s2_ang[2]}\n')

                    if time() - last_flush_time > 60:
                        file.flush()
                        last_flush_time = time()

                    sleep(0.1) # 出力頻度

            except KeyboardInterrupt:
                self.handle_keyboard_interrupt(stop_event, thread1, thread2)