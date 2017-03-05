from flask import current_app
from google.cloud import datastore

builtin_list = list

def init_app(app):
    pass

def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])

def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity

def list(limit=100, cursor=None):
    ds = get_client()

    query = ds.query(kind='aazz', order=['date'])
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor

def filtered_date_list(filter=filter, limit=100, cursor=None):
    ds = get_client()

    query = ds.query(kind='aazz', order=['date'])
    query.add_filter("date","=", filter)
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor

def filtered_route_list(filter=filter, limit=100, cursor=None):
    ds = get_client()
    query = ds.query(kind='aazz', order=['trainRoute'])
    query.add_filter("trainRoute","=", filter)
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)
    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)
    return entities, next_cursor
