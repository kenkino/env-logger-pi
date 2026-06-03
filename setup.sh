#!/bin/bash

# 現在のパスとユーザー名を取得
PROJECT_ROOT=$(pwd)
USER_NAME=$(whoami)

# 設定ファイルがなければ作成する
if [ ! -f config.json ]; then
    cp config.json.example config.json
    echo "config.json を作成しました。必要に応じて編集してください。"
fi

# 2. サービスファイルの生成
# テンプレートを読み込み、変数を置換して書き出す
sed -e "s|{{PROJECT_ROOT}}|$PROJECT_ROOT|g" \
    -e "s|{{USER_NAME}}|$USER_NAME|g" \
    service/env_logger.service.template > service/env_logger.service

echo "service/env_logger.service を生成しました。"
echo "設定が完了しました。以下でサービスを有効化してください:"
echo "sudo cp service/env_logger.service /etc/systemd/system/"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl restart envlogging"
