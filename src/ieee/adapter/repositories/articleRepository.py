from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from ieee.domain.entities import ArticleEntity


class ArticleRepository(AbstractSqlalchemyRepository):
    @property
    def model(self):
        return ArticleEntity

    def find_by_articleId(self, articleId) -> model:
        return self.query.filter(ArticleEntity.articleId == articleId).first()
