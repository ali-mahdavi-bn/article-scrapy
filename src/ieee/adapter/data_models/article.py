from sqlalchemy import Table, Integer, Text, Column, String, DateTime, func, Uuid

from backbone.infrastructure.postgres_connection import BaseEntity

article_table = Table('articles', BaseEntity.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('uuid', Uuid, unique=True),
                      Column('link_article', String, nullable=False),
                      Column('format', String(100)),
                      Column('article_text', Text),
                      Column('displayPublicationTitle', String(255)),
                      Column('abstract', Text),
                      Column('title', String(255)),
                      Column('doi', String(255)),
                      Column('publication_date', String(100)),
                      Column('funding_name', String(100)),
                      Column('conf_loc', String(100)),
                      Column('article_id', Integer),
                      Column('volume', Integer),
                      Column('issue', Integer),
                      Column('publisher', String(255)),
                      Column('insert_date', String(255)),
                      Column('created_at', DateTime, server_default=func.now()),
                      Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
                      )
