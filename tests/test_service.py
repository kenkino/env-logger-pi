import subprocess
import pytest
import os
import sys

# systemdはLinuxでしか動かないため、Linux以外ならテストを除外する


@pytest.mark.skipif(sys.platform != "linux", reason="systemd-analyze only available on Linux")
def test_systemd_service_syntax():
    """systemd-analyze を使用して service ファイルの文法チェックを行う"""
    service_path = "service/env_logger.service"

    if not os.path.exists(service_path):
        pytest.skip("service file not found")

    result = subprocess.run(
        ['systemd-analyze', 'verify', service_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"systemd service file has errors: {result.stderr}"
