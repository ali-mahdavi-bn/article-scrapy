from account.domain import commands
from account.service_layer.validators.password_validators import PasswordValidator
from backbone.infrastructure.microservices.auth import AuthMicroservice
from unit_of_work import UnitOfWork


def update_user_password(command: commands.UpdateUserPassword, uow: UnitOfWork, auth_servie: AuthMicroservice):
    with uow:
        PasswordValidator("body.password", command.password).validate()
        auth_servie.change_user_password(user_id=command.user_id, password=command.password)
        return {"message": "updated password successfully"}
