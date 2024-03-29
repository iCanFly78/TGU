import yaml
import socket
import urllib.request
import re
CONFIG_FILE = r'clientconfig.yaml'


class BaseConfig:
    def __init__(self):

        with open(CONFIG_FILE) as fh:
            client_config = yaml.load(fh, yaml.FullLoader)
        for key, value in client_config.items():
            setattr(self, key, value)

    def get_conn(self, key: str):
        return str(getattr(self, key)['host']), int(getattr(self, key)['port'])

    def get_ip(self, iptype: str = 'local'):
        if iptype == 'local':
            ip = socket.gethostbyname(socket.gethostname())
        elif iptype == 'external':
            res = urllib.request.urlopen('http://ya.ru/internet').read()
            ip = re.search(b'\d+\.\d+\.\d+\.\d+', res).group().decode()
        else:
            raise Exception('Unknown ip type')
        return ip


