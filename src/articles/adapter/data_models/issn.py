from sqlalchemy import Table, Integer, Column, String, DateTime, func, ForeignKey, Uuid

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

issn_table = Table('issn', MAPPER_REGISTRY.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('format', String(50)),
                   Column('value', String(50)),
                   Column('articles_id', Uuid, ForeignKey('articles.uuid')),
                   Column('created_at', DateTime, server_default=func.now()),
                   Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                   )
