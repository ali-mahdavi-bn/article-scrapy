from sqlalchemy import Table, Integer, ForeignKey, Column,Uuid

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

article_author_association_table = Table('article_author_association', MAPPER_REGISTRY.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('article_id', Uuid, ForeignKey('articles.uuid')),
                                   Column('author_id', Uuid, ForeignKey('authors.uuid'))
                                   )
