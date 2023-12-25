from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    DEBUG = True
    FAKE_USER: str = ''
    FAKE_EMPLOYEE: str = ''
    PORT = 8010

    # KEYCLOAK CONFIGS
    KEYCLOAK_SERVER_URL = ""
    KEYCLOAK_CLIENT_NAME = ""
    KEYCLOAK_CLIENT_ID = ""
    KEYCLOAK_REAL_NAME = ""
    KEYCLOAK_CLIENT_SECRET_KEY = ""

    # KEYCLOAK ADMIN CONFIGS
    KEYCLOAK_ADMIN_USER = ""
    KEYCLOAK_ADMIN_PASSWORD = ""
    KEYCLOAK_ADMIN_CLIENT_SECRET_KEY = ""

    # POSTGRES CONFIGS
    POSTGRES_USER = ""
    POSTGRES_PASSWORD = ""
    POSTGRES_DATABASE = ""
    POSTGRES_PORT = ""
    POSTGRES_HOST = ""

    KEYCLOAK_POSTGRES_USER = "keycloak"
    KEYCLOAK_POSTGRES_PASSWORD = ""
    KEYCLOAK_POSTGRES_DATABASE = "keycloak"
    KEYCLOAK_POSTGRES_PORT = "1234"
    KEYCLOAK_POSTGRES_HOST = ""

    # KAFKA CONFIGS
    KAFKA_ADDRESS = ""
    KAFKA_ORGANIZATION_CREATED_EVENT = "Organization.OrganizationCreatedEvent"
    KAFKA_USER_ID_WAS_SET = "Keycloak.UserIdWasSet"
    KAFKA_FORM_SUBMITTED = "form.submitted"
    KAFKA_ATTENDANCE_DAY_CALCULATED = "attendance.day_calculated"
    KAFKA_RULE_ENGINE_FLOW_REACTIVATION = "rule_engine.flow_reactivation"
    KAFKA_TRAFFIC_PAIRED = "time_attendance.traffic_paired"

    # neo4j
    NEO4J_URL = "localhost:7687"
    NEO4J_PASSWORD = "password"

    # MONGODB CONFIGS
    MONGODB_URL = ""
    MONGODB_DATABASE = ""
    MONGODB_USERNAME = ""
    MONGODB_PASSWORD = ""

    # REDIS CONFIGS
    REDIS_HOST = ""
    REDIS_PORT = ""
    REDIS_USER = ""
    REDIS_PASSWORD = ""

    # s3 config
    S3_ENDPOINT = ""
    S3_BUCKET = ""
    S3_ACCESS_KEY = ""
    S3_SECRET_KEY = ""

    GOOGLE_CLIENT_ID = ""
    GOOGLE_CLIENT_SECRET = ""

    BIOVATION_RABBITMQ_HOST = ""
    BIOVATION_RABBITMQ_PORT = ""
    BIOVATION_RABBITMQ_USER = ""
    BIOVATION_RABBITMQ_PASSWORD = ""
    BIOVATION_RABBITMQ_QUEUE = "timez.biovation.logInsertedEvent_queue"
    BIOVATION_RABBITMQ_BULK_QUEUE = "timez.biovation.bulkLogInsertedEvent_queue"

    # kavenegar
    KAVENEGAR_ACCESS_KEY = ""

    class Config:
        case_sensitive = False
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        env_file = (str(BASE_DIR) + "/.env").replace("//", "/")
        env_file_encoding = 'utf-8'


config = Config()


class PasswordConfig:
    MIN_LENGTH = 8
    UPPERCASE_REQUIRED = False
    LOWERCASE_REQUIRED = True
    DIGIT_REQUIRED = True
    SPECIAL_CHARACTERS_REQUIRED = False
    SPECIAL_CHARACTERS = r"[!@#$%^&*()]"
