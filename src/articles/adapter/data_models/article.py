from sqlalchemy import Table, Integer, Text, Column, ForeignKey,String, DateTime, func, Uuid

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

article_table = Table('articles', MAPPER_REGISTRY.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('uuid', Uuid, unique=True),
                      Column('link_article', String),
                      Column('content_of_article', Text),
                      Column('language_id', Integer, ForeignKey('languages.id')),
                      Column('title', String(255)),
                      Column('publisher', String(255)),
                      Column('abstract', Text),
                      Column('published_in', String(100)),
                      Column('date_of_conference', String(30)),
                      Column('doi', String(100)),
                      Column('insert_date', String(255)),
                      Column('conf_loc', String(100)),
                      Column('publication_date', String(255)),
                      Column('start_page', Integer),
                      Column('end_page', Integer),
                      Column('article_id', Integer),
                      Column('created_at', DateTime, server_default=func.now()),
                      Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                      )
