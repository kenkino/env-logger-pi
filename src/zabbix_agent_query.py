import sys
from src.zabbix_exporter import ZabbixExporter


def main():
    if len(sys.argv) < 2:
        return
    data = ZabbixExporter.read_latest()
    key = sys.argv[1]
    print(data.get(key, 0))


if __name__ == "__main__":
    main()
