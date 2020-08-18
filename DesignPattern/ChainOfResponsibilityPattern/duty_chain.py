from __future__ import annotations
import random
import time
import request_
from abc import ABC, abstractmethod
from typing import Any, Optional
from models import Resource

class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """
    _next_handler: Handler = None
    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> object:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class isAuthenticatedHandlers(AbstractHandler):
    def handle(self, request: Any) -> object:
        if request.Meta['is_authenticated']:
            print("Already login!")
            return self._next_handler.handle(request)
        else:
            print("Not login!")
            return 401


class isSuperHandlers(AbstractHandler):
    def handle(self, request: Any) -> object:
        if request.Meta['is_superuser']:
            print("is Super User!")
            return 200
        else:
            print("Not Super User!")
            return self._next_handler.handle(request)


class ResourceExistHandlers(AbstractHandler):
    def handle(self, request: Any) -> object:
        if Resource.has_resource(request.Meta['HTTP_X_ORIGIN_URL'], request.Meta['HTTP_X_ORIGIN_METHOD']):
            print("Resource Exist!")
            return self._next_handler.handle(request)
        else:
            print("Resource Does Not Exist!")
            return 404

class permissionHandlers(AbstractHandler):
    def handle(self, request: Any) -> object:
        if request.Meta['PERMIT']:
            print("has Permission!")
            return 200
        else:
            print("Forbidden!")
            return 403

def get_chain():
    isAuthen = isAuthenticatedHandlers()
    isSuperuser = isSuperHandlers()
    resourceExist = ResourceExistHandlers() 
    permit = permissionHandlers()
    isAuthen.set_next(
        isSuperuser).set_next(
            resourceExist).set_next(
                permit)
    return isAuthen