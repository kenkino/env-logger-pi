from unittest.mock import patch, MagicMock
from src.sensors import BME280

# 設定データ
dummy_config = {'bus_number': 1, 'i2c_address': 0x76}


@patch('src.sensors.bme280')
@patch('src.sensors.smbus2.SMBus')
def test_read_sensor_data_with_mock(mock_smbus, mock_bme280):
    # 1. bme280ライブラリのサンプリング結果をモック化
    mock_data = MagicMock()
    mock_data.temperature = 27.5
    mock_data.humidity = 60.0
    mock_data.pressure = 1013.25
    mock_bme280.sample.return_value = mock_data

    # 2. 初期化用のキャリブレーションデータもモック化
    mock_bme280.load_calibration_params.return_value = {}

    # 3. インスタンス化
    sensor = BME280(dummy_config)

    # 4. 実行と検証
    data = sensor.read_sensor_data()

    assert data['temp'] == 27.5
    assert data['hum'] == 60.0
    assert 'press' in data
