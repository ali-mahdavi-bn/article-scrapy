from inspect import getmembers, isclass

from backbone.infrastructure.postgres_connection import DEFAULT_SESSION_FACTORY
from enumeration import enums
from enumeration.domain.entities.enumeration import Enumeration


def migrate_enumerations(session_maker=DEFAULT_SESSION_FACTORY):
    with session_maker() as session:
        for p, c in getmembers(enums, isclass):
            if hasattr(c, "parent") and hasattr(c, "members"):
                members = c.members()
                for member in members:
                    enum = Enumeration.create(member)

                    session.add(enum)
                    try:
                        session.commit()
                    except:
                        session.rollback()

# def enumeration_factory(enum_id, title, parent_id) -> Enumeration:
#     enumeration = Enumeration()
#     enumeration.id = enum_id
#     enumeration.title = title
#     enumeration.parent_id = parent_id
#     return enumeration



from sqlalchemy import event
from sqlalchemy.orm import Session

@event.listens_for(Session, "do_orm_execute")
def do_orm_execute(orm_execute_state):
   if orm_execute_state.is_insert:
       print("An insert operation has been executed.")