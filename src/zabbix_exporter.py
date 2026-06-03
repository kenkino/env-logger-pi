import json
import logging


class ZabbixExporter:
    def __init__(self, file_path='/dev/shm/bme280_latest.json'):
        self.file_path = file_path

    def export(self, data):
        """センサーデータをJSONとして出力する"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"エクスポートエラー: {e}")

    @staticmethod
    def read_latest():
        """Zabbixエージェントが呼び出す用の静的メソッド"""
        try:
            with open('/dev/shm/bme280_latest.json', 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"JSON load error: {e}")
            return {"temp": 0, "hum": 0, "press": 0}
