import traceback
import sys
import time
import requests
import os


class Hawk():

    params = {}

    def __init__(self, settings):
        """
        Init Hawk Catcher class with params.
        Set exceptions hook.

        :param settings String|Dict: init params

        {String} settings = 'eyJhbGciOiJIUz<...>WyQPiqc'
            Pass your project JWT token

        {Dictionary} settings = {
            'token': 'eyJhbGciOiJIUz<...>WyQPiqc',
                Project JWT token from Hawk
            'host': 'hawk.so',
                (optional) Hostname for your Hawk server
            'secure': True
                (optional) https or http
        }
        """

        if type(settings).__name__ == 'str':
            settings = {
                'token': settings
            }

        self.params = {
            'token': settings.get('token', ''),
            'host': settings.get('host', 'hawk.so'),
            'secure': settings.get('secure', True),
        }

        if not self.params['token']:
            print('Token is missed. Check init params.')
            return

        self.params['url'] = 'http{}://{}/'.format('s' if self.params['secure'] else '',
                                                    self.params['host'])

        sys.excepthook = self.handler

    def handler(self, exc_cls, exc, tb):
        """
        Catch, prepare and send error

        :param exc_cls: error class
        :param exc: exception
        :param tb: exception traceback
        """
        ex_message = traceback.format_exception_only(exc_cls, exc)[-1]
        ex_message = ex_message.strip()

        error_frame = tb
        while error_frame.tb_next is not None:
            error_frame = error_frame.tb_next

        file = error_frame.tb_frame.f_code.co_filename
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
            callee['sourceCode'] = self.get_near_filelines(callee['file'], callee['line'])
            backtrace.append(callee)

        # Reverse stack to have the latest call at the top
        backtrace = tuple(reversed(backtrace))

        event = {
            'token': self.params['token'],
            'catcherType': 'errors/python',
            'payload': {
                'title': ex_message,
                'backtrace': backtrace,
                'headers': {},
                'addons': {}
            }
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

    def get_near_filelines(self, filepath, line, margin=5):
        """
        Return part of file near the string with error

        :param filepath: path to file
        :param line: error line
        :param margin: get that number of strings above and below error
        :return trace: tuple
        """
        # Read file and strip right spaces
        with open(filepath, 'r') as file:
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

        # Trace tuple to be returned
        trace = []

        # Cycle index for line number
        index = 1

        # Get cut of original file
        lines = content[start:end]
        for array_line in range(start, end):
            trace.append({
                # +1 because lines in array start from 0
                'line': array_line + 1,
                # Get item from lines array
                'content': lines[array_line - start]
            })

        return trace
