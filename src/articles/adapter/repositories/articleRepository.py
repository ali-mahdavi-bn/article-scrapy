from articles.domain.entities.article import Article
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository


class ArticleRepository(AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Article

    def find_by_article_id(self, article_id) -> model:
        return self.query.filter(Article.article_id == article_id).first()
