from ...core import Hawk
from typing import Union
from hawk_python_sdk.modules.flask.types import FlaskSettings, Addons
from hawk_python_sdk.errors import ModuleError

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
        got_request_exception.connect(self._handle_request_exception)

    @staticmethod
    def get_params(settings) -> Union[FlaskSettings, None]:
        hawk_params = Hawk.get_params(settings)

        if hawk_params is None:
            return None

        return {
            **hawk_params,
            'set_user': settings.get('set_user'),
        }
    
    def send(self, exception, context=None, user=None):
        """
        Method for manually send error to Hawk
        :param exception: exception
        :param context: additional context to send with error
        :param user: user information who faced with that event
        """

        if (user is None) and (request):
            user = self._set_user(request)

        super().send(exception, context, user)

    def _handle_request_exception(self, sender: Flask, exception):
        """
        Catch, prepare and send error

        :param sender: flask app
        :param exception: exception
        """

        user = self._set_user(request)

        ctx = self.params.get('context', None)

        self.send(exception, ctx, user)

    def _set_addons(self) -> Union[Addons, None]:
        """
        Set flask addons to send with error
        """
        addons: Union[Addons, None] = None

        if self.params.get('with_addons') == True:
            headers = dict(request.headers)
            cookies = dict(request.cookies)

            addons = {
                'flask': {
                    'url': request.url,
                    'method': request.method,
                    'headers': headers,
                    'cookies': cookies,
                    'params': request.args,
                    'form': request.form,
                    'json': request.json
                }
            }

        return addons
