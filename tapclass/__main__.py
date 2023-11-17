from pywebio import start_server
from tapclass.app import tap_catch

if __name__ == '__main__':
    start_server(tap_catch, port=8080)
