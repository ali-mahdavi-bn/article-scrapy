import json
from uuid import UUID

import requests
from typing import Optional, List
from pydantic import BaseModel
from keycloak import KeycloakOpenID, KeycloakOpenIDConnection, KeycloakAdmin

from backbone.configs import config
from backbone.exception import UnauthorizedException, ForbiddenException
from backbone.infrastructure.discovery.microservices import AUTH_MICROSERVICE
from backbone.service_layer.general_types import Name
from unit_of_work import UnitOfWork


class AuthException(Exception):
    pass


class User(BaseModel):
    id: str
    tenants: Optional[List[str]] = []
    name: Name
    roles: Optional[List[str]] = []


class AuthMicroservice:
    BASE_URL = AUTH_MICROSERVICE

    def __init__(self, realm_name: str = config.KEYCLOAK_REAL_NAME, client_id: str = config.KEYCLOAK_CLIENT_NAME,
                 client_secret_key: str = config.KEYCLOAK_CLIENT_SECRET_KEY):
        self.realm_name = realm_name
        self.client_id = client_id
        self.client_secret_key = client_secret_key

    def perform_healthcheck(self):
        pass

    def openid(self):
        return KeycloakOpenID(server_url=config.KEYCLOAK_SERVER_URL,
                              client_id=self.client_id,
                              realm_name=self.realm_name,
                              client_secret_key=self.client_secret_key)

    def remove_user_credential(self, user_id: UUID | str):
        try:
            credential = self.get_admin_keycloak_openid().get_credentials(user_id=user_id.__str__())
            if len(credential) > 0:
                if credential[0].get('id') is None:
                    raise AuthException("user hasn't any credential.")
                self.get_admin_keycloak_openid().delete_credential(user_id=user_id.__str__(),
                                                                   credential_id=credential[0].get('id'))
        except Exception as e:
            raise AuthException(e)

    def change_user_password(self, user_id: UUID, password: str):
        try:
            self.remove_user_credential(user_id)
            return self.get_admin_keycloak_openid().set_user_password(user_id.__str__(), password, temporary=False)
        except Exception as e:
            raise AuthException(e)

    def get_admin_keycloak_openid(self) -> KeycloakAdmin:
        keycloak_connection = KeycloakOpenIDConnection(
            server_url=config.KEYCLOAK_SERVER_URL,
            username=config.KEYCLOAK_ADMIN_USER,
            password=config.KEYCLOAK_ADMIN_PASSWORD,
            realm_name=self.realm_name,
            client_id=self.client_id,
            client_secret_key=self.client_secret_key,
            verify=True)
        # keycloak_connection.realm_name = self.realm_name
        return KeycloakAdmin(connection=keycloak_connection)

    def authenticate_user(self, token):
        try:
            result = self.openid().introspect(token)
            if not result.get("active"):
                return None
            roles = []
            organization_roles = result.get("resource_access").get("organization")
            auth_roles = result.get("resource_access").get("auth")
            roles.extend(organization_roles.get('roles') if organization_roles else [])
            roles.extend(auth_roles.get('roles') if auth_roles else [])
            user = User(id=result['sub'],
                        name=Name(first_name=result.get('given_name'), last_name=result.get('family_name')),
                        tenants=result.get('tenants'), roles=roles)
            return user
        except Exception as e:
            raise AuthException(e)

    def fake_authenticate_user(self):
        from backbone.configs import config
        if not config.DEBUG:
            raise Exception
        if config.FAKE_EMPLOYEE:
            with UnitOfWork() as uow:
                emp = uow.organization_employee.find_by_uuid(UUID(config.FAKE_EMPLOYEE))
                pres = uow.organization_personnel.find_by_uuid(emp.person_id)
                user_uuid = str(pres.user_uuid)
                name = f"{pres.first_name} {pres.last_name}"
        elif config.FAKE_USER:
            user_uuid = str(config.FAKE_USER)
            name = ""
        else:
            raise Exception

        return User(id=str(user_uuid),
                    name=Name("fake user", name),
                    tenants=None, roles=[])

    def get_users_info(self, user_ids):
        headers = {"Authorization": "Bearer " + self.get_client_token()}
        url = AUTH_MICROSERVICE + f"auth/users_info"
        for i, user_id in enumerate(user_ids):
            url += "?" if i == 0 else "&"
            url += f"user_ids={user_id}"
        result = requests.get(url, headers=headers)
        if result.status_code == 200:
            return json.loads(result.text)
        else:
            return {}

    def has_access_to_resource(self, user_id, resource, scope):
        pass

    def get_client_token(self):
        return self.openid().token(grant_type="client_credentials")['access_token']

    def add_tenant(self, tenant_id, user_id):
        pass

    def has_uma_access(self, token, resource, scope):
        result = self.openid().has_uma_access(token=token, permissions=f"{resource}#{scope}")
        if not result.is_logged_in:
            raise UnauthorizedException()
        if not result.is_authorized:
            permission = '.'.join(''.join(result.missing_permissions).split("#"))
            raise ForbiddenException(f"PermissionDenied.Resource.Scope", resource=resource, scope=scope)
