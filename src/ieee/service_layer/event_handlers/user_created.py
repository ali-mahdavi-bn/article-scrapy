from account.domain import events
from backbone.infrastructure.microservices.auth import AuthMicroservice
from organization.domain.entities import OrganizationPersonnel
from unit_of_work import UnitOfWork


def add_user_to_keycloak(message: events.UserCreated, uow: UnitOfWork, auth_servie: AuthMicroservice):
    keycloak_users_id = auth_servie.get_admin_keycloak_openid().create_user({
        "username": message.mobile, "enabled": True}, exist_ok=True)

    with uow:
        user = uow.user.find_by_mobile(message.mobile)
        user.uuid = keycloak_users_id
        person = uow.organization_personnel.query.filter(OrganizationPersonnel.user_id == user.id)
        person.user_uuid = keycloak_users_id
        uow.commit()
