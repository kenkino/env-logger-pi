import smbus2
import bme280
import logging


class BME280:
    def __init__(self, config):
        self.bus_number = config['bus_number']
        self.i2c_address = config['i2c_address']
        self.bus = smbus2.SMBus(self.bus_number)

        # センサーのキャリブレーション値を読み込んでおく
        try:
            self.calibration_params = bme280.load_calibration_params(
                self.bus, self.i2c_address
            )
            logging.info("BME280: ライブラリ初期化完了")
        except AttributeError:
            logging.error("ライブラリのメソッド名が異なります")
            raise

    def read_sensor_data(self):
        """センサーから補正済みのデータを取得"""
        try:
            # ライブラリが補正計算まで自動で行う
            data = bme280.sample(self.bus, self.i2c_address, self.calibration_params)
            return {
                "temp": data.temperature,
                "hum": data.humidity,
                "press": data.pressure
            }
        except Exception as e:
            logging.error(f"BME280: データ読み取りエラー - {e}")
            return {"temp": 0.0, "hum": 0.0, "press": 0.0}
