import traceback
import sys
import time
import requests

class Hawk:

    __name__ = "Codex Hawk"

    def __init__(self):

        self.token = None
        self.domain = None

        self.host = 'howk.io'
        self.path = 'catcher/python'
        self.url = 'https://' + self.host + '/' + self.path

        sys.excepthook = self.handler

    def config(self, token, domain, host=None, path=None):
        self.token = token
        self.domain = domain
        self.host = host if host else self.host
        self.path = path if path else self.path
        self.url = 'http://' + self.host + '/' + self.path

    def handler(self, exc_cls, exc, tb):

        ex_message = traceback.format_exception_only(exc_cls, exc)[-1]

        error_frame = tb
        while error_frame.tb_next is not None:
            error_frame = error_frame.tb_next

        file = error_frame.tb_frame.f_code.co_filename
        line = error_frame.tb_lineno
        stack = ''.join(traceback.format_exception(exc_cls, exc, tb))

        event = {
            'token': self.token,
            'message': ex_message,
            'errorLocation': {
                'file': file,
                'line': line,
                'full': file + ' -> ' + str(line)
            },
            'stack': stack,
            'time': time.time()
        }
        result = requests.post(self.url, json=event)

    def __call__(self):
        self.handler(*sys.exc_info())

