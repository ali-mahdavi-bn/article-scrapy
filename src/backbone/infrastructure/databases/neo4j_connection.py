import datetime
import inspect
import json
from contextlib import contextmanager
from uuid import UUID

import neo4j
from neo4j import GraphDatabase

from backbone.configs import config
from backbone.helpers.utils import datetime_to_str

NEO4J_DRIVER = GraphDatabase.driver("neo4j://" + config.NEO4J_URL, auth=("neo4j", config.NEO4J_PASSWORD))


@contextmanager
def neo4j_transaction(neo4j_driver=NEO4J_DRIVER):
    with neo4j_driver.session() as session:
        with session.begin_transaction() as tx:
            yield tx


def get_neo4j_driver():
    return NEO4J_DRIVER


def query_create(node_type: str, model: object) -> str:
    query = f"CREATE (n:{node_type}) "
    query = _build_from_object(query, model)
    query += "RETURN n"
    return query


def query_update(node_type: str, identifier: str, model: object) -> str:
    query = f"MATCH (n:{node_type}) WHERE n.uuid = '{identifier}' "
    query = _build_from_object(query, model)
    query += "RETURN n"
    return query


def _build_from_object(query: str, model: object):
    for key in inspect.getmembers(model, lambda a: not (inspect.isroutine(a)))[0][1].keys():
        value = model.__dict__.get(key)
        if value is None:
            continue
        value = f'{datetime_to_str(value)}' if isinstance(value, datetime.datetime) else value
        value = value.__str__() if isinstance(value, neo4j.time.DateTime) else value
        value = json.dumps(value) if isinstance(value, list) else value
        value = value.__str__() if isinstance(value, UUID) else value
        query += f"SET n.{key} = "
        query += f"'{value}'" if isinstance(value, str) else f"{value}"
        query += " \n "

    return query
