from sqlalchemy import Table, Column, Integer, String, DateTime, func, Text, Uuid

from backbone.infrastructure.postgres_connection import BaseEntity

author_table = Table('authors', BaseEntity.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('uuid', Uuid, unique=True),
                     Column('first_name', String(255)),
                     Column('last_name', String(255)),
                     Column('affiliation', String(255)),
                     Column('authors_id', String(255)),
                     Column('bio', Text),
                     Column('created_at', DateTime, server_default=func.now()),
                     Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                     )
