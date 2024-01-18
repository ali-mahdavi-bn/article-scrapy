from articles.domain.entities.article import Article
from backbone.adapter.abstract_entity import BaseEntity
from unit_of_work import UnitOfWork


def fetch_items(page_size, page_number, entity: BaseEntity, where: str = None) -> BaseEntity:
    offset = (page_number - 1) * page_size
    with (UnitOfWork() as uow):
        item = uow.session.query(entity)
        if where:
            item = item.where(eval(where))
        item = item.order_by(entity.id).limit(page_size) \
            .offset(offset).all()
        return item


def fetch_article_empty_article_text(page_size, page_number):
    return fetch_items(page_size=page_size, page_number=page_number, entity=Article,
                       where="Article.content_of_article == ''")


