from functools import wraps
from uuid import UUID

from backbone.exception import UnauthorizedException, ForbiddenException
from backbone.infrastructure.microservices.auth import AuthMicroservice
from backbone.api.middelwares.request_context import current_request


def organization_validation():
    def inner(func):
        @wraps(func)
        def view_method(*args, **kwargs):
            user = kwargs.get('user')
            if user is None:
                raise UnauthorizedException()
            tenants = user.tenants
            if tenants is None or len(tenants) == 0:
                raise ForbiddenException("you are not in any organization")
            if kwargs.get("organization_id") is None:
                raise Exception("organization_id needed in parameter")
            organization_id = kwargs.get("organization_id")
            organization_id = organization_id.__str__() if isinstance(organization_id, UUID) else organization_id
            if organization_id not in tenants:
                raise ForbiddenException("you are not in this organization")
            return func(*args, **kwargs)

        return view_method

    return inner


def has_access(resource: str, scope: str):
    def inner(func):
        @wraps(func)
        def view_method(*args, **kwargs):
            AuthMicroservice().has_uma_access(token=current_request().state.token, resource=resource, scope=scope)
            return func(*args, **kwargs)

        return view_method

    return inner


def access_on_client_only():
    def inner(func):
        @wraps(func)
        def view_method(*args, **kwargs):
            client_id = AuthMicroservice().openid().introspect(token=current_request().state.token).get("clientId")
            if not client_id:
                raise ForbiddenException(detail="PermissionDenied.only_client_has_access")
            return func(*args, **kwargs)

        return view_method

    return inner
