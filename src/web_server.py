from flask import Flask, jsonify
import json


def create_app(config):
    app = Flask(__name__)

    @app.route('/data')
    def get_data():
        try:
            with open('/dev/shm/bme280_latest.json', 'r') as f:
                return jsonify(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:  # 具体的なエラーを指定
            return jsonify({"error": f"No data available: {e}"}), 503
    return app
