from class_sensor_data_logger import SensorDataLogger

if __name__ == "__main__":
    logger = SensorDataLogger("COM5", "COM8")  # 適宜変更
    logger.set_output_interval(0.05)  # 20Hzで読み取り,書き出し
    mode = input("-1: テスト, 1: 実行: ")
    if mode == "-1":
        logger.run_test()
    else:
        logger.run()
