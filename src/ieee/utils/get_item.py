from backbone.infrastructure.postgres_connection import BaseEntity
from ieee.domain.entities import ArticleEntity
from unit_of_work import UnitOfWork


def fetch_items(page_size, page_number, entity: BaseEntity) -> BaseEntity:
    offset = (page_number - 1) * page_size
    with (UnitOfWork() as uow):

        item = uow.session.query(entity) \
            .order_by(entity.id).limit(page_size) \
            .offset(offset).all()
        return item


def fetch_article(page_size, page_number):
    return fetch_items(page_size=page_size, page_number=page_number, entity=ArticleEntity)
