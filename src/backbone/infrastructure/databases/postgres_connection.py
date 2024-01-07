import inspect
import os

from sqlalchemy import create_engine, URL, NullPool, event
from sqlalchemy.orm import sessionmaker

from backbone.configs import config

DEFAULT_URl = URL.create("postgresql+psycopg2", username=config.POSTGRES_USER, password=config.POSTGRES_PASSWORD,
                         host=config.POSTGRES_HOST, port=config.POSTGRES_PORT, database=config.POSTGRES_DATABASE)

DEFAULT_ENGIN = create_engine(
    DEFAULT_URl,
    # poolclass=NullPool,
    isolation_level="REPEATABLE READ",
    # echo=config.DEBUG,
)


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=DEFAULT_ENGIN
)


PROJECT_ROOT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
THIS_FILE_PATH = os.path.abspath(__file__)


def get_file_name_and_line_number():
    stack = inspect.stack()
    found = []
    for frame in stack:
        filename = os.path.abspath(frame[1])
        if (
                filename.startswith(PROJECT_ROOT_DIRECTORY) and
                'abstract' not in filename and
                filename != THIS_FILE_PATH
        ):
            found.append(f"-- {filename}:{frame[2]}")
    return found


# Create an event listener for query execution
@event.listens_for(DEFAULT_ENGIN, 'before_cursor_execute', retval=True)
def add_comment(conn, cursor, statement, parameters, context, executemany):
    current_info = get_file_name_and_line_number()
    if current_info:
        # Add a comment with file name and line number to the beginning of the query
        comment = "\n".join(current_info)
        statement_with_comment = f"{comment}\n{statement}"
        return statement_with_comment, parameters
    return statement, parameters
