from pynput.mouse import Controller
from configparser import ConfigParser
import tools
import window

mouse = Controller()
ls = []
config = ConfigParser()
config.read('config.ini', encoding='utf-8')
appid = ''
secretKey = ''
if config.has_section('set') and config.has_option('set', 'appid') and config.has_option('set', 'secret_key'):
    appid = config['set']['appid']
    secretKey = config['set']['secret_key']


def start():
    p = tools.translate('apple', appid, secretKey)
    window.keyboard_listener_start()
    t = p.get('error_code', '0')
    if t == '0':
        window.start_translate(appid, secretKey)
    else:
        if t == '52003':
            window.start_settings()
        else:
            print(t)


start()


