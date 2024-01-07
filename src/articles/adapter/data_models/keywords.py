from sqlalchemy import Table, Integer, Column, String, DateTime, func, ForeignKey, Uuid

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

keyword_table = Table('keywords', MAPPER_REGISTRY.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('type', String(100)),
                      Column('keyword', String(100)),
                      Column('article_id', Uuid, ForeignKey('articles.uuid')),
                      Column('created_at', DateTime, server_default=func.now()),
                      Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                      )
