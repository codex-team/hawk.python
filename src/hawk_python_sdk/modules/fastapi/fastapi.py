from hawk_python_sdk.types import HawkCatcherSettings
from ...core import Hawk
from hawk_python_sdk.modules.fastapi.types import FastapiSettings, FastapiAddons
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Union
from hawk_python_sdk.errors import ModuleError
import asyncio
from contextvars import ContextVar
from fastapi import Request
import asyncio

# Variable for saving current request, work with async tasks
current_request: ContextVar[Union[Request, None]] = ContextVar("current_request", default=None)


# class for catching errors in fastapi app
class HawkFastapi(Hawk):
    params: FastapiSettings = {}
        
    def init(self, settings: Union[str, FastapiSettings] = None):
        self.params = self.get_params(settings)
    
        if self.params.get('app_instance') is None:
            raise ModuleError('Fastapi app instance not passed to HawkFastapi')

        self.params.get('app_instance').add_middleware(self._get_starlette_middleware())

    def _get_starlette_middleware(self):
        """
        Create middleware for starlette to identify request exception and storing current request for manual sending
        """

        # Create method to use it in middleware class with Hawk class context
        def send_func(err):
            return self.send(err)

        class StarletteMiddleware:
            def __init__(self, app: ASGIApp):
                self.app = app

            async def __call__(self, scope: Scope, receive: Receive, send: Send):
                if scope["type"] == "http":
                    request = Request(scope, receive, send)
                    current_request.set(request)
                    try:
                        await self.app(scope, receive, send)
                    except Exception as err:
                        return send_func(err)
                else:
                    await self.app(scope, receive, send)
                return None

        return StarletteMiddleware

    def send(self, event: Exception = None, context=None, user=None):
        """
        Method for manually send error to Hawk, make it async for starlette
        :param exception: exception
        :param context: additional context to send with error
        :param user: user information who faced with that event
        """

        request = current_request.get()

        if user is None and request is not None:
            user = self._set_user(request)

        return super().send(event, context, user)
    
    def _set_addons(self) -> Union[FastapiAddons, None]:
        request = current_request.get()

        if request is None:
            return None

        return {
            'fastapi': {
                'url': str(request.url),
                'method': request.method,
                'headers': dict(request.headers),
                'cookies': dict(request.cookies),
                'params': dict(request.query_params)
            }
        }
    
    @staticmethod
    def get_params(settings) -> FastapiSettings | None:
        hawk_params = Hawk.get_params(settings)

        if hawk_params is None:
            return None

        return {
            **hawk_params,
            'app_instance': settings.get('app_instance'),
        }