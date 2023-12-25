from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from ieee.domain.entities import IssnEntity


class IssnRepository(AbstractSqlalchemyRepository):
    @property
    def model(self):
        return IssnEntity

    def find_by_file_id(self, file_id):
        return self.query.filter(IssnEntity.file_id == file_id).first()
