from sqlalchemy import Table, Integer, Column, String, DateTime, func, Uuid, ForeignKey

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

file_table = Table('files', MAPPER_REGISTRY.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('uuid', Uuid, unique=True),
                   Column('source', Uuid, ForeignKey('articles.uuid'), nullable=True),
                   Column('path', String),
                   Column("format", String(100)),
                   Column('created_at', DateTime, server_default=func.now()),
                   Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                   )
