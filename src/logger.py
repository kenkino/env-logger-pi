import csv
import os
from datetime import datetime


class CSVLogger:
    def __init__(self, filepath='data/log.csv'):
        self.filepath = filepath
        # ディレクトリがない場合は作成
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # ファイルがない場合はヘッダーを作成
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'temp', 'hum', 'press'])

    def log(self, data):
        """データをCSVに追記する"""
        with open(self.filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                f"{data['temp']:.2f}",
                f"{data['hum']:.2f}",
                f"{data['press']:.2f}"
            ])
