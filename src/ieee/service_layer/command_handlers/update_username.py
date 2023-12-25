from account.domain import commands
from backbone.helpers.utils import remove_none_from_dict
from backbone.infrastructure.microservices.auth import AuthMicroservice
from unit_of_work import UnitOfWork


def update_username(command: commands.UpdateUserName, uow: UnitOfWork, auth_servie: AuthMicroservice):
    with uow:
        payload = command.dict()
        user_id = payload.pop("user_id")
        payload = remove_none_from_dict(payload)

        user = uow.user.find_by_uuid(command.user_id)
        user.mobile = command.username

        uow.session.flush()
        auth_servie.get_admin_keycloak_openid().update_user(user_id=user_id.__str__(), payload=payload)
        uow.commit()

        uow.session.refresh(user)
        return user
