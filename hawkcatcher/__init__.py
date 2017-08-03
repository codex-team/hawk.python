import traceback
import sys
import time
import requests


class __Hawk():

    params = {}

    def __init__(self):
        pass

    def enable(self, settings):
        """
        Init Hawk Catcher class with params.
        Set exceptions hook.

        :param settings String|Dict: init params

        {String} settings = '1234567-abcd-8901-efgh-123456789012'
            Pass your project token

        {Dictionary} settings = {
            'token': '1234567-abcd-8901-efgh-123456789012',
                Project token from Hawk
            'domain': 'myproject.codex',
                Domain name
            'host': 'hawk.so',
                Hostname for your Hawk server
            'path': 'catcher/python',
                Route for this catcher
            'secure': True
                https or http
        }
        """

        if type(settings).__name__ == 'str':
            settings = {
                'token': settings
            }

        self.params = {
            'token': settings.get('token', ''),
            'domain': settings.get('domain', 'guryn.me'),
            'host': settings.get('host', 'hawk.so'),
            'secure': settings.get('secure', True),
            'path': settings.get('path', 'catcher/python'),
        }

        if not self.params['token']:
            print('Token is missed. Check init params.')
            return

        # TODO remove it
        if not self.params['domain']:
            print('Domain is missed. Check init params.')
            return
        ###

        self.params['url'] = 'http{}://{}/{}'.format('s' if self.params['secure'] else '',
                                                    self.params['host'],
                                                    self.params['path'])

        sys.excepthook = self.handler

    def handler(self, exc_cls, exc, tb):
        """
        Catch, prepare and send error

        :param exc_cls: error class
        :param exc: exception
        :param tb: exception traceback
        """

        ex_message = traceback.format_exception_only(exc_cls, exc)[-1]
        print(ex_message)

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
            'token': self.params['token'],
            'domain': self.params['domain'],
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
            r = requests.post(self.params['url'], json=event)
            response = r.content.decode('utf-8')
            print('[Hawk] Response: %s' % response)
        except Exception as e:
            print('[Hawk] Can\'t send error cause of %s' % e)

    def catch(self):
        """
        Exception processor
        """
        self.handler(*sys.exc_info())

hawk = __Hawk()
