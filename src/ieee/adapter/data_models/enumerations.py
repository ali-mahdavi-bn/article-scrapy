from sqlalchemy import Table, Column, Integer, String, ForeignKey

from backbone.infrastructure.postgres_connection import BaseEntity

enumeration_table = Table('enumerations', BaseEntity.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('title', String(100)),
                          Column('parent_id', Integer, ForeignKey('enumerations.id'))
                          )
