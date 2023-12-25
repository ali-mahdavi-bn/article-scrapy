from __future__ import annotations

from backbone.infrastructure.databases.postgres_connection import DEFAULT_SESSION_FACTORY
from backbone.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from ieee.adapter import repositories as ieee_repo


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, postgres_session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = postgres_session_factory

    def __enter__(self):
        self.session = self.session_factory(expire_on_commit=False)  # type: Session
        self.article = ieee_repo.ArticleRepository(self.session)
        self.author = ieee_repo.AuthorRepository(self.session)
        self.issn = ieee_repo.IssnRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        # self.session.expunge_all()
        self.session.close()

    def repositories(self):
        repos = []
        try:
            pass
        except:
            pass
        return repos

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.expunge_all()
        # self.session.rollback()
