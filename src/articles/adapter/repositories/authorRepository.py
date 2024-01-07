from articles.domain.entities.author import Author
from backbone.adapter.abstract_sqlalchemy_repository import AbstractSqlalchemyRepository


class AuthorRepository(AbstractSqlalchemyRepository):
    @property
    def model(self):
        return Author

    def find_by_authors_id(self, authors_id):
        return self.query.filter(Author.authors_id == authors_id).first()
