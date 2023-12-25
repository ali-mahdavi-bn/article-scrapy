from backbone.configs import config

AUTH_MICROSERVICE = "http://localhost:8008/" if config.DEBUG else "https://timez-auth-service.darkube.app/"
KEYCLOAK_SERVER_URL = "https://keyckoak-times.darkube.app/"
PERSONNEL_MICROSERVICE_URL = "http://localhost:8010/" if config.DEBUG else "https://organization.darkube.app/"
