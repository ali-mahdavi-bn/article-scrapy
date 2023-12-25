import requests

from account.domain import commands
from backbone.configs import config
from backbone.exception import ForbiddenException


def remove_active_session(command: commands.RemoveActiveSession):
    try:
        url = f"{config.KEYCLOAK_SERVER_URL}admin/realms/timez/sessions/{command.session_id}"
        header = {
            "Authorization": f"Bearer {command.token}"
        }
        requests.delete(url, headers=header)
        return {"uuid": command.session_id}
    except IndexError as e:
        raise ForbiddenException(detail="you_have_to_permission")
