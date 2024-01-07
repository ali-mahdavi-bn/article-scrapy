from sqlalchemy import Table, Integer, Column, String

from backbone.adapter.abstract_data_model import MAPPER_REGISTRY

language_table = Table('languages', MAPPER_REGISTRY.metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String(50), unique=True, nullable=True)
                       )
