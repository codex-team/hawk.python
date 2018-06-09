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

        {String} settings = '1234567-abcd-8901-efgh-123456789012'
            Pass your project token

        {Dictionary} settings = {
            'token': '1234567-abcd-8901-efgh-123456789012',
                Project token from Hawk
            'host': 'hawk.so',
                (optional) Hostname for your Hawk server
            'path': 'catcher/python',
                (optional) Route for this catcher
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
            'path': settings.get('path', 'catcher/python'),
        }

        if not self.params['token']:
            print('Token is missed. Check init params.')
            return

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
        ex_message = ex_message.strip()
        print(ex_message)

        error_frame = tb
        while error_frame.tb_next is not None:
            error_frame = error_frame.tb_next

        file = error_frame.tb_frame.f_code.co_filename
        line = error_frame.tb_lineno
        stack = traceback.extract_tb(tb)

        formated_stack = []
        for summary in stack:
            callee = {
                'file': os.path.abspath(summary[0]),
                'line': summary[1],
                'func': summary[2],
                'text': summary[3],
            }

            # Get part of file near string with error
            callee['trace'] = self.get_near_filelines(callee['file'], callee['line'])
            formated_stack.append(callee)

        # Reverse stack to have the latest call at the top
        formated_stack = tuple(reversed(formated_stack))

        event = {
            'token': self.params['token'],
            'message': ex_message,
            'errorLocation': {
                'file': os.path.abspath(file),
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
