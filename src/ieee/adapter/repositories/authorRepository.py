from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository
from ieee.domain.entities import AuthorEntity


class AuthorRepository(AbstractSqlalchemyRepository):
    @property
    def model(self):
        return AuthorEntity

    def find_by_authorsId(self, authorsId):
        return self.query.filter(AuthorEntity.authorsId == str(authorsId)).first()
