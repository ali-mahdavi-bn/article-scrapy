from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from backbone.configs import config

config_data = {'GOOGLE_CLIENT_ID': config.GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': config.GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

