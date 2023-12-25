from uuid import UUID

import sentry_sdk
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class AdditionalDataMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # body = await request.body()
        # with sentry_sdk.configure_scope() as scope:
        #     scope.set_context("request", {
        #         "headers": dict(request.headers),
        #         "path": request.url.path,
        #         "query_params": dict(request.query_params),
        #         "request_body":  body.decode()
        #     })

        request.state.organization_id = request.headers.get('X-Organization-Id')
        request.state.personnel_id = request.headers.get('X-Personnel-Id')
        request.state.employee_id = request.headers.get('X-Employee-Id')
        request.state.device_id = request.headers.get("X-Device-Id")
        return await call_next(request)
