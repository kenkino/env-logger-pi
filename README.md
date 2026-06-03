# Environmental Logger for Raspberry Pi

Raspberry Piを使用して環境データ（気温、湿度など）を記録・管理するシステムです。物理ボタンによる操作やWebサーバー機能、Zabbix連携を備えています。

## ハードウェア構成

* **本体**: Raspberry Pi (Zero W, 3B+, 4B等)
* **センサー**: BME280 (I2C接続)
* **ディスプレイ**: I2C接続 16x2 LCD
* **入力デバイス**: プッシュボタン x 2 (Start / Stop)

## セットアップ手順 (Quick Start)

本プロジェクトは、クローン後に簡単なセットアップスクリプトを実行するだけで環境構築が完了します。

### 1. クローンと初期設定

```bash
git clone <新しいリポジトリのURL>
cd <新しいリポジトリ名>

# 実行権限を付与してセットアップスクリプトを実行
chmod +x setup.sh
./setup.sh

```

※ `setup.sh` により、以下の作業が自動で行われます。

* `config.json.example` から `config.json` を作成
* `service/env_logger.service.template` を元にシステム設定ファイルを生成

### 2. 仮想環境の準備とインストール

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 3. サービスとして登録（自動起動設定）

```bash
# 生成された設定ファイルをシステムに配置
sudo cp service/env_logger.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable envlogging
sudo systemctl start envlogging

```

## 設定のカスタマイズ

`config.json` を編集することで、センサーの計測間隔やWebサーバーのポート番号などを自由に変更できます。

```json
{
    "sensor": {
        "bus_number": 1,
        "i2c_address": 118,
        "interval_sec": 60
    },
    "lcd": {
        "enabled": false,
        "bus_number": 1,
        "i2c_address": 62
    },
    "gpio": {
        "start": 22,
        "stop": 23
    },
    "web": {
        "host": "0.0.0.0",
        "port": 5000
    }
}

```

## 開発・テスト

開発環境でロジックを確認する場合は、以下のコマンドを実行してください。

```bash
pytest

```

## プロジェクトの特徴

* **疎結合な設計**: ハードウェア制御とWebインターフェースが分離されています。
* **自動化されたデプロイ**: `setup.sh` により、クローンした環境へ即座に適応可能です。
* **品質保証**: `pytest` による自動テストと `flake8` によるコード品質管理を導入しています。


