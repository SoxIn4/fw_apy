"""Python wrapper for FileWave api."""

import json
from collections import namedtuple

import requests  # REQUIRES: pip install requests[security]


API_KEY = 'PASTE_BASE64_ENCODED_API_KEY_HERE'
SERVER_ADDRESS = 'https://url.to.filewave.server:20443'

API_PATH = '/inv/api/v1'
API_URL = SERVER_ADDRESS + API_PATH


def create_api_request(*args, **kwargs):
    """
    Create api request adding each arg as a part of the url.

    ex. call_api('query', '1') will call server_url/query/1
    Return request object and dict of options from kwargs.
    Option dict contains arguments for the request.
    Request will be GET unless POST or PATCH specified with mode KW.
    Use data KW to pass data to be included as json in request body.
    """
    options = {'url': API_URL,
               'headers': {"authorization": API_KEY,
                           "Content-Type": "application/json; charset=utf-8"},
               'verify': False}
    for arg in args:
        options['url'] += '/{}'.format(arg)
    if ('mode' in kwargs and kwargs['mode'] == 'GET') or 'mode' not in kwargs:
        print 'creating request'
        request = requests.get
    elif 'mode' in kwargs and kwargs['mode'] == 'POST':
        if 'data' in kwargs:
            options['data'] = json.dumps(kwargs['data'])
        request = requests.post
    elif 'mode' in kwargs and kwargs['mode'] == 'PATCH':
        if 'data' in kwargs:
            options['data'] = json.dumps(kwargs['data'])
        request = requests.patch
    else:
        request = None
    return request, options


def call_api(*args, **kwargs):
    """
    Send api call adding each arg as a part of the url, and return response.

    ex. call_api('query', '1') will call server_url/query/1
    """
    request, options = create_api_request(*args, **kwargs)
    try:
        print 'sending request'
        response = request(**options)
        print 'response received'
        if 200 <= response.status_code < 300:
            try:
                return json.loads(response.content)
            except ValueError:
                return response.content
        return (options['url'], response)
    except requests.exceptions.RequestException as error:
        print 'HTTP Request failed: ' + options['url'] + '\n' + str(error)


def get_components():
    """Return a list of columns from the fields in components dict."""
    components = call_api('component')
    column = namedtuple(typename='column',
                        field_names=['display_name', 'description', 'type'])

    return {category: {field['column']: column(field.get('display_name', 'NA'),
                                               field.get('description',
                                                         'No Description'),
                                               field['type'])
                       for field in components[category]['fields']}
            for category in components}


def get_columns(query_id):
    """Return a list of columns from the fields in components dict."""
    components = get_components()
    return [components[field['component']][field['column']]
            for field in get_query(query_id)['fields']]


def get_all_queries():
    """Return all queries as a dict."""
    return call_api('query')


def get_query_result(query_id=None, mode='GET', data=None):
    """Return query results as a dict."""
    if mode == 'GET':
        return call_api('query_result', query_id)
    elif mode == 'POST':
        return call_api('query_result/', mode='POST', data=data)


def get_count(query_id):
    """Return the number (int) of items matching a query_id."""
    return get_query_result(query_id)['total_results']


def get_query(query_id):
    """Return query definition as json object."""
    return call_api('query', query_id)


def import_query(query, name=None, favorite=False):
    """Upload new query (dict or json) to server and return result."""
    if isinstance(query, dict):
        if name:
            query['name'] = name
        query['favorite'] = favorite
    return call_api('query/', mode='POST', data=query)


if __name__ == "__main__":
    pass
