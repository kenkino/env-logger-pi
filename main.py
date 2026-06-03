from src.web_server import create_app
from src.buttons import ControlButton
from src.zabbix_exporter import ZabbixExporter
from src.logger import CSVLogger
from src.displays import AQM1602
from src.sensors import BME280
from src.utils import load_config
import time
import os
import logging
import threading

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def main():
    config = load_config('config.json')

    # モジュールの初期化
    sensor = BME280(config['sensor'])
    logger = CSVLogger('logs/env_data.csv')
    exporter = ZabbixExporter()
    lcd = AQM1602(config['lcd']) if config['lcd'].get('enabled') else None
    buttons = ControlButton(config['gpio']['start'], config['gpio']['stop'])

    # Webサーバー起動処理
    app = create_app(config['web'])
    threading.Thread(
        target=lambda: app.run(
            host=config['web']['host'],
            port=config['web']['port'],
            threaded=True,
            use_reloader=False
        ),
        daemon=True
    ).start()
    logging.info(f"Webサーバー起動: {config['web']['host']}:{config['web']['port']}")

    is_running = False
    if lcd:
        lcd.display("WellComme !!", "Ready to start", force=True)

    try:
        while True:
            # 1. ボタン操作の判定
            if buttons.is_start_pressed():
                is_running = True
                if lcd:
                    lcd.display("Start monitor!!", "Logging...", force=True)

            action = buttons.get_stop_action()
            if action == 'LONG':
                if lcd:
                    lcd.display("Force Shutdown", "Bye!!", force=True)
                os.system("sudo shutdown -h now")
                break
            elif action == 'DOUBLE':
                if lcd:
                    lcd.display("Shutdown !!", "Shutting down...", force=True)
                os.system("sudo shutdown -h now")
                break
            elif action == 'SINGLE':
                is_running = False
                if lcd:
                    lcd.display("Maintenance !!", "Stopped", force=True)

            # 2. 計測・出力処理
            if is_running:
                try:
                    data = sensor.read_sensor_data()
                    logger.log(data)
                    exporter.export(data)

                    if lcd:
                        lcd.display(f"t {data['temp']:.1f} C", f"h {data['hum']:.1f} %")
                except Exception as e:
                    logging.error(f"計測エラー: {e}")

            time.sleep(1)  # CPU負荷軽減のためのインターバル

    except KeyboardInterrupt:
        logging.info("システム停止")
    finally:
        # クリーンアップ処理
        if lcd:
            lcd.display("System Stop", "Goodbye", force=True)


if __name__ == "__main__":
    main()
