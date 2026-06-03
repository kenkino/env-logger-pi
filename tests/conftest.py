# tests/conftest.py
import sys
from unittest.mock import MagicMock

# src以下のコードが読み込まれるよりも前に、RPi系をダミーで埋める
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
