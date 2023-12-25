from account.domain import commands
from account.domain.entities.user import User
from unit_of_work import UnitOfWork


def update_wo_factor_authentication(command: commands.UpdateUserTwoFactorAuth, uow: UnitOfWork):
    with uow:
        user: User = uow.user.find_by_uuid(command.user_id)
        user.two_factor_authentication = command.enable
        uow.commit()
        uow.session.refresh(user)
        return user
