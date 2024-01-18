from abc import ABC

from articles.domain.entities import Issn
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository


class AbstractIssRepository(AbstractSqlalchemyRepository, ABC):
    def find_by_file_id(self, file_id):
        self._find_by_file_id(file_id)

    def _find_by_file_id(self, file_id):
        raise NotImplementedError


class SqlalchemyIssnRepository(AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Issn

    def find_by_file_id(self, file_id):
        return self.query.filter(Issn.article_id == file_id).first()
