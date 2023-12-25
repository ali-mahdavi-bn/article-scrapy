from sqlalchemy import Table, Column, Integer, String, DateTime, func, Uuid, ForeignKey

from backbone.infrastructure.postgres_connection import BaseEntity

issn_table = Table('issn', BaseEntity.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('format', String(50)),
                   Column('value', String(50)),
                   Column('articles_id', Uuid, ForeignKey('articles.uuid')),
                   Column('created_at', DateTime, server_default=func.now()),
                   Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                   )
