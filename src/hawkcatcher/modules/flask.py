from ..core import Hawk
from typing import Union
from hawkcatcher.modules.types import FlaskSettings
from hawkcatcher.errors import ModuleError

try:
    from flask.signals import got_request_exception
    from flask import Flask, request
except ImportError:
    raise ModuleError("Flask is not installed")

# class for catching errors in flask app
class HawkFlask(Hawk):
    params: FlaskSettings = {}

    def init(self, settings: Union[str, FlaskSettings] = None) -> None:
        self.params = self.get_params(settings)
        got_request_exception.connect(self.handle_request_exception)

    @staticmethod
    def get_params(settings) -> Union[FlaskSettings, None]:
        hawk_params = Hawk.get_params(settings)

        if hawk_params is None:
            return None

        return {
            **hawk_params,
            'set_user': settings.get('set_user'),
            'with_request_data': settings.get('with_request_data', True)
        }

    def handle_request_exception(self, sender: Flask, exception):
        """
        Catch, prepare and send error

        :param sender: flask app
        :param exception: exception
        """
        ctx = {}

        if self.params.get('with_request_data') == True:
            headers = dict(request.headers)
            cookies = dict(request.cookies)
            ctx = {
                'app': sender.name,
                'url': request.url,
                'method': request.method,
                'headers': headers,
                'cookies': cookies,
                'params': request.args,
                'form': request.form,
                'json': request.json
            }

        if self.params.get('set_user') is not None:
            ctx['user'] = self.params['set_user'](request)

        self.send(exception, ctx)
    
