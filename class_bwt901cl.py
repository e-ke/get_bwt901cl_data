# 参考: https://qiita.com/Dorebom/items/19b69293b811da2f7851

import serial
from time import sleep


class BWT901CL(serial.Serial):
    def __init__(self, Port, max_retries=5):
        for attempt in range(max_retries):
            try:
                super().__init__(Port, baudrate=9600, timeout=1)
                # センサーの初期化処理
                self._initialize_sensor_attributes()
                # UARTのスタートBITを探索
                self._synchronize_UART()
                break  # 初期化に成功した場合、ループを抜ける
            except serial.SerialException as e:
                print(f"{e}")
                if attempt < max_retries - 1:
                    print(f"再接続中... ({attempt + 1}/{max_retries})")
                    sleep(3)  # 再接続前の待機時間
                else:
                    print("再接続に失敗しました。プログラムを終了します。")
                    raise  # 再接続の試行が上限に達した場合、例外を再発生させる

    def _initialize_sensor_attributes(self):
        # 属性をループで初期化
        attrs = ['angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z', 
                 'angle_x', 'angle_y', 'angle_z', 
                 'accel_x', 'accel_y', 'accel_z', 
                 'Temp', 
                 'magnetic_x', 'magnetic_y', 'magnetic_z', 
                 'quaternion_x', 'quaternion_y', 'quaternion_z', 
                 'YY', 'MM', 'DD', 'hh', 'mm', 'ss', 'ms', 
                 'D0', 'D1', 'D2', 'D3']
        for attr in attrs:
            setattr(self, attr, 0.0)
        self.quaternion_w = 1.0

    def _synchronize_UART(self):
        while True:
            data = self.read(size=1)
            if data == b'\x55':  # UARTのスタートBITを探索
                self.read(size=10)  # 次のデータブロックを読み込む
                print("UART synchronization successful.")
                break
            print("Trying to synchronize UART: ", data)


    def _readData(self):
        for i in range(6):
            data = super(BWT901CL, self).read(size=11)

            if not len(data) == 11:
                print('byte error:', len(data))
                break
            if not data[0] == 0x55: # スタートBITに異常がある場合読み込み中止
                print('UART sync error:', bytes(data))
                break
            #Time
            if data[1] == 0x50:
                self.YY = data[2]
                self.MM = data[3]
                self.DD = data[4]
                self.hh = data[5]
                self.mm = data[6]
                self.ss = data[7]
                self.ms = int.from_bytes(data[8:10], byteorder='little')

            #Acceleration
            elif data[1] == 0x51:
                # signed=Trueオプションを忘れると，符号なしで認識されてバグることがある．
                self.accel_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768.0*16.0*9.8
                self.accel_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768.0*16.0*9.8
                self.accel_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768.0*16.0*9.8
                self.Temp = int.from_bytes(data[8:10], byteorder='little', signed=True)/340.0+36.25

            #Angular velocity
            elif data[1] == 0x52:
                self.angular_velocity_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768*2000.0
                self.angular_velocity_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768*2000.0
                self.angular_velocity_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768*2000.0
                self.Temp = int.from_bytes(data[8:10], byteorder='little')/340.0+36.25

            #Angle
            elif data[1] == 0x53:
                self.angle_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768*180
                self.angle_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768*180
                self.angle_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768*180

            #Magnetic
            elif data[1] == 0x54:
                self.magnetic_x = int.from_bytes(data[2:4], byteorder='little', signed=True)
                self.magnetic_y = int.from_bytes(data[4:6], byteorder='little', signed=True)
                self.magnetic_z = int.from_bytes(data[6:8], byteorder='little', signed=True)

            #Quatrernion
            elif data[1] == 0x59:
                self.quaternion_x = int.from_bytes(data[2:4], byteorder='little', signed=True)/32768
                self.quaternion_y = int.from_bytes(data[4:6], byteorder='little', signed=True)/32768
                self.quaternion_z = int.from_bytes(data[6:8], byteorder='little', signed=True)/32768
                self.quaternion_w = int.from_bytes(data[8:10], byteorder='little', signed=True)/32768

            #Data output port status
            elif data[1] == 0x55:
                self.D0 = int.from_bytes(data[2:4], byteorder='little',signed=True)
                self.D1 = int.from_bytes(data[4:6], byteorder='little',signed=True)
                self.D2 = int.from_bytes(data[6:8], byteorder='little',signed=True)
                self.D3 = int.from_bytes(data[8:10], byteorder='little',signed=True)

    def stop(self):
        super(BWT901CL, self).close()

    def getData(self):
        super(BWT901CL, self).reset_input_buffer()
        is_not_sync = True
        while is_not_sync:
            data = super(BWT901CL, self).read(size=1)
            # print("is_not_sync:",data)
            if data == b'\x55': # UARTの同期エラーをリカバリ
                print("is_not_sync_if:",data)
                data = super(BWT901CL, self).read(size=10)
                is_not_sync = False
                break

        self._readData()
        return  (self.angle_x, self.angle_y, self.angle_z), \
                (self.angular_velocity_x, self.angular_velocity_y, self.angular_velocity_z), \
                (self.accel_x, self.accel_y, self.accel_z), \
                self.Temp, \
                (self.magnetic_x, self.magnetic_y, self.magnetic_z), \
                (self.quaternion_x, self.quaternion_y, self.quaternion_z, self.quaternion_w), \
                (self.MM, self.DD, self.hh, self.mm, self.ss, self.ms)
    
    # Field Getters
    def getAccel(self):
        return (self.accel_x, self.accel_y, self.accel_z)
    
    def getAngularVelocity(self):
        return (self.angular_velocity_x, self.angular_velocity_y, self.angular_velocity_z)
    
    def getAngle(self):
        return (self.angle_x, self.angle_y, self.angle_z)

    def getTemperature(self):
        return self.Temp