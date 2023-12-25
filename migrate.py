from backbone.infrastructure.postgres_connection import BaseEntity, DEFAULT_ENGIN
from migrate_enum import migrate_enumerations

migrate_enumerations()
BaseEntity.metadata.create_all(DEFAULT_ENGIN)


