from abc import ABC

from articles.domain.entities.article import Article
from backbone.adapter.abstract_repository import AbstractRepository
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository


class AbstractUserRepository(AbstractRepository, ABC):
    def find_by_article_id(self, article_id):
        article = self._find_by_article_id(article_id)
        return article

    def _find_by_article_id(self, article_id):
        raise NotImplementedError


class SqlalchemyArticleRepository(AbstractUserRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Article

    def _find_by_article_id(self, article_id) -> model:
        return self.query.filter(Article.article_id == article_id).first()
