from account.domain import commands
from backbone.helpers.utils import remove_none_from_dict
from backbone.infrastructure.microservices.auth import AuthMicroservice
from unit_of_work import UnitOfWork


def update_user_info(command: commands.UpdateUserInfo, uow: UnitOfWork, auth_servie: AuthMicroservice):
    with uow:
        payload = command.dict()
        user_id = payload.pop("user_id")
        payload = remove_none_from_dict(payload)

        user = uow.user.find_by_uuid(command.user_id)
        if command.email:
            user.email = command.email
        if command.lastName:
            user.last_name = command.lastName
        if command.firstName:
            user.first_name = command.firstName

        auth_servie.get_admin_keycloak_openid().update_user(user_id=user_id.__str__(), payload=payload)
        uow.commit()
        uow.session.refresh(user)
        return user