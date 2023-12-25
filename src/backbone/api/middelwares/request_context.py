from contextvars import ContextVar
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

_request_ctx_var: ContextVar = ContextVar("request", default=None)


def current_request() -> Optional[Request]:
    return _request_ctx_var.get()


class AddRequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        req = _request_ctx_var.set(request)
        response = await call_next(request)
        _request_ctx_var.reset(req)
        return response
