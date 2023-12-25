from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from backbone.configs import config
from backbone.infrastructure.microservices.auth import AuthMicroservice, AuthException


class AuthenticateMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        header = request.headers.get('Authorization')
        request.state.user = None
        request.state.token = None

        if header is None:
            return await call_next(request)
        protocol, _, token = header.partition(" ")

        try:
            if config.DEBUG and request.headers.get('X-Mobile'):
                from backbone.infrastructure.microservices.auth.auth_microservice import User
                from unit_of_work import UnitOfWork
                uow = UnitOfWork()
                with uow:
                    user = uow.user.find_by_mobile(request.headers.get('X-Mobile'))
                    user = User(id=str(user.uuid),
                                name=user.name,
                                tenants=None, roles=[])
            else:
                user = AuthMicroservice().authenticate_user(token)
            if user is None:
                return await call_next(request)
            request.state.user = user
            request.state.token = token

            return await call_next(request)

        except AuthException:
            return await call_next(request)
