import traceback
import sys
import time
import requests

class Hawk:

    __name__ = "Codex Hawk"

    def __init__(self):

        self.token = None
        self.domain = None

        self.host = 'hawk.io'
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
        stack = traceback.extract_tb(tb)

        formated_stack = []
        for summary in stack:
            formated_stack.append({
                'file': summary[0],
                'line': summary[1],
                'func': summary[2],
                'text': summary[3]
            })

        event = {
            'token': self.token,
            'domain': self.domain,
            'message': ex_message,
            'errorLocation': {
                'file': file,
                'line': line,
                'full': file + ' -> ' + str(line)
            },
            'stack': formated_stack,
            'time': time.time()
        }

        try:
            requests.post(self.url, json=event)
        except Exception as e:
            print('[Hawk] Cant send error because of', e)

    def __call__(self):
        self.handler(*sys.exc_info())

