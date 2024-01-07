from uuid import UUID

from backbone.adapter.abstract_entity import BaseEntity


class ArticleAuthorAssociation(BaseEntity):
    id: int
    article_id: UUID
    author_id: UUID

    @classmethod
    def create(self, article_id,author_id):
        article_author = ArticleAuthorAssociation()
        article_author.article_id = article_id
        article_author.author_id = author_id
        return article_author
