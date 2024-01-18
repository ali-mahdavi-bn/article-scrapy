from abc import ABC

from articles.domain.entities.author import Author
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository


class AbstractAuthorRepository(AbstractSqlalchemyRepository, ABC):
    def find_by_authors_id(self, authors_id):
        self._find_by_authors_id(authors_id)

    def _find_by_authors_id(self, authors_id):
        raise NotImplementedError


class SqlalchemyAuthorRepository(AbstractAuthorRepository, AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Author

    def _find_by_authors_id(self, authors_id):
        return self.query.filter(Author.authors_id == authors_id).first()
