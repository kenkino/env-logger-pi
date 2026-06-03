from unittest.mock import patch, MagicMock
from src.sensors import BME280

dummy_config = {'bus_number': 1, 'i2c_address': 0x76}


@patch('src.sensors.bme280')
@patch('src.sensors.smbus2.SMBus')
def test_read_sensor_data(mock_smbus, mock_bme280):
    # 1. モックの設定
    mock_bme280.load_calibration_params.return_value = {}

    # 2. センサーデータのシミュレーション
    mock_data = MagicMock()
    mock_data.temperature = 27.5
    mock_data.humidity = 60.0
    mock_data.pressure = 1013.25
    mock_bme280.sample.return_value = mock_data

    # 3. インスタンス生成
    sensor = BME280(dummy_config)

    # 4. 新しい read_sensor_data メソッドのテスト
    result = sensor.read_sensor_data()

    # 検証
    assert result['temp'] == 27.5
    assert result['hum'] == 60.0
    assert 'press' in result
