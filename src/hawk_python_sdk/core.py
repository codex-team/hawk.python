import os
import sys
import traceback
from typing import Union

import requests
from base64 import b64decode
import json

import hawk_python_sdk
from hawk_python_sdk.errors import InvalidHawkToken
from hawk_python_sdk.types import HawkCatcherSettings, Addons, User


class Hawk:
    params: HawkCatcherSettings = {}

    def __init__(self, settings: Union[str, HawkCatcherSettings] = None):
        """
        Init Hawk Catcher class with params.
        Set exceptions hook.

        :param settings String|Dict: init params
        """
        if settings is not None:
            self.init(settings)

    def init(self, settings: Union[str, HawkCatcherSettings] = None):
        self.params = self.get_params(settings)

        sys.excepthook = self.handler

    @staticmethod
    def get_params(settings) -> Union[HawkCatcherSettings, None]:
        if settings is None:
            return None

        settings = {'token': settings} if isinstance(settings, str) else settings

        if not settings['token']:
            return None

        return {
            'token': settings.get('token'),
            'collector_endpoint': settings.get('collector_endpoint') or Hawk.get_collector_endpoint(
                settings.get('token')),
            'release': settings.get('release'),
            'before_send': settings.get('before_send'),
            'context': settings.get('context', None)
        }

    def handler(self, exc_cls: type, exc: Exception, tb: traceback, context=None, user=None):
        """
        Catch, prepare and send error

        :param exc_cls: error class
        :param exc: exception
        :param tb: exception traceback
        :param context: additional context to be send with event
        :param user: user information who faced with that event
        """

        if not self.params:
            return
        
        # in case passed context is empty set default from config
        if context is None:
            context = self.params.get('context')

        ex_message = traceback.format_exception_only(exc_cls, exc)[-1]
        ex_message = ex_message.strip()
        backtrace = tb and Hawk.parse_traceback(tb)
        addons = self._set_addons()

        if not (type(context) is dict):
            context = {
                'value': context
            }

        if addons is None:
            addons = {}

        event = {
            'token': self.params['token'],
            'catcherType': 'errors/python',
            'payload': {
                'title': ex_message,
                'type': exc_cls.__name__,
                'backtrace': backtrace,
                'release': self.params['release'],
                'context': context,
                'catcherVersion': hawk_python_sdk.__version__,
                'user': user,
                'addons': addons
            }
        }

        if self.params['before_send'] is not None:
            self.params['before_send'](event)

        self.send_to_collector(event)

    def send_to_collector(self, event):
        try:
            url = f'{self.params["collector_endpoint"]}'
            r = requests.post(url, json=event)
            response = r.content.decode('utf-8')
            print('[Hawk] Response: %s' % response)
        except Exception as e:
            print('[Hawk] Can\'t send error cause of %s' % e)

    def send(self, event: Exception = None, context=None, user=None):
        """
        Method for manually send error to Hawk
        :param event: event to send
        :param context: additional context to send with error
        :param user: user information who faced with that event
        """

        exc_cls, exc, tb = sys.exc_info()

        if event is not None:
            self.handler(type(event), event, tb, context, user)
        else:
            self.handler(exc_cls, exc, tb, context, user)

    def _set_addons(self) -> Union[Addons, None]:
        """
        Set framework addons to send with error
        """
        return None
    
    def _set_user(self, request) -> Union[User, None]:
        """
        Set user information by set_user callback
        """
        user = None

        if self.params.get('set_user') is not None:
            user = self.params['set_user'](request)

        return user
    

    @staticmethod
    def parse_traceback(tb):
        error_frame = tb
        while error_frame.tb_next is not None:
            error_frame = error_frame.tb_next

        # todo: what for?
        # noinspection PyUnusedLocal
        file = error_frame.tb_frame.f_code.co_filename
        # noinspection PyUnusedLocal
        line = error_frame.tb_lineno

        stack = traceback.extract_tb(tb)

        backtrace = []

        # summary - https://docs.python.org/3/library/traceback.html#traceback.FrameSummary
        for summary in stack:
            callee = {
                'file': os.path.abspath(summary.filename),
                'line': summary.lineno,
                'function': summary.name,
            }

            # Get part of file near string with error
            callee['sourceCode'] = Hawk.get_near_filelines(callee['file'], callee['line'])
            backtrace.append(callee)

        # Reverse stack to have the latest call at the top
        backtrace = tuple(reversed(backtrace))

        return backtrace

    @staticmethod
    def get_collector_endpoint(token):
        try:
            decoded_string = b64decode(token)
            token_data = json.loads(decoded_string)
            integration_id = token_data.get('integrationId')

            if integration_id is None:
                raise InvalidHawkToken()
        except Exception:
            raise InvalidHawkToken()

        return f'https://{integration_id}.k1.hawk.so'

    @staticmethod
    def get_near_filelines(filepath, line, margin=10):
        """
        Return part of file near the string with error

        :param filepath: path to file
        :param line: error line
        :param margin: get that number of strings above and below error
        :return trace: tuple
        """
        # Read file and strip right spaces
        with open(filepath) as file:
            content = file.readlines()
            content = [x.rstrip() for x in content]

        # Calculate upper and lower strings for code fragment

        # Error in 7th line in file <=> 6th element in array
        error_line_in_array = line - 1

        # Start and end are being counted for lines array
        # Start from 0 or error_line_in_array - margin
        start = max(0, error_line_in_array - margin)

        #  file | array
        #  line | key
        #     1 |  0
        # /¯¯ 2 |  1 ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ # start from 1
        # |   3 |  2                   |
        # |   4 |  3                   |
        # |   5 |  4                   |
        # |   6 |  5                   |
        # | [ 7 |  6  raise Error()  ] |
        # |   8 |  7                   |
        # |   9 |  8                   |
        # |  10 |  9                   |
        # |  11 | 10                   |
        # \_ 12 | 11 __________________/ # end is 12 because python doesn't get element on the right side of range
        #    13 | 12
        #    14 | 13
        #
        # End is the last line of code fragment in array plus 1
        # or the number of code lines in file
        end = min(len(content), error_line_in_array + margin + 1)

        # todo: what for?
        # Cycle index for line number
        # noinspection PyUnusedLocal
        index = 1

        # Get cut of original file
        lines = content[start:end]

        return [
            {
                # +1 because lines in array start from 0
                'line': array_line + 1,
                # Get item from lines array
                'content': lines[array_line - start]
            } for array_line in range(start, end)
        ]
