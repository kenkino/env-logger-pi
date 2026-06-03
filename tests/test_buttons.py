from unittest.mock import MagicMock, patch
from src.buttons import ControlButton


def test_is_start_pressed():
    mock_gpio = MagicMock()
    mock_gpio.LOW = 0
    mock_gpio.input.return_value = 0  # LOWを返す

    btn = ControlButton(17, 27, gpio=mock_gpio)
    assert btn.is_start_pressed() is True


def test_get_stop_action_long():
    with patch('time.time') as mock_time:
        mock_gpio = MagicMock()
        mock_gpio.LOW = 0
        mock_gpio.input.return_value = 0
        mock_time.side_effect = [0.0, 3.5]

        btn = ControlButton(17, 27, gpio=mock_gpio)
        assert btn.get_stop_action() == 'LONG'
