"""List devices in a table."""

from collections import namedtuple

import json
from flask import Flask, jsonify, render_template

from fw_apy import (get_components, get_all_queries, get_query,
                    get_query_result, get_columns, get_count)

APP = Flask(__name__)

COMPONENTS = get_components()
OS_INFO = namedtuple(typename='OS_INFO', field_names=['query_id', 'count'])
# Replace the query ID#'s in OS_DICT below with your own
OS_DICT = {'iOS': OS_INFO(45, None),
           'macOS': OS_INFO(1, None),
           'Windows': OS_INFO(3, None),
           'Android': OS_INFO(50, None)}
QUERY_LIST = [('device_details', 'Device Details'),
              ('fileset_info', 'Filesets'),
              ('profile_info', 'Profiles'),
              ('application_info', 'Installed Application')]


def get_platform_counts():
    """Run all platform queries and return a dict of os_data tuples."""
    os_dict = OS_DICT
    for platform, info in os_dict.items():
        os_dict[platform] = info._replace(count=get_count(info.query_id))
    return os_dict


def get_device_query(query):
    """Load json query file and return dict."""
    with open('query_templates/{}_query.json'.format(query)) as query_file:
        return json.load(query_file)


def prepare_device_queries(device_name):
    """Return dict query json objects with device_name in criteria."""
    device_queries = {query[0]: get_device_query(query[0])
                      for query in QUERY_LIST}
    for query in device_queries:
        device_queries[query]['criteria']['qualifier'] = device_name
    return device_queries


@APP.route('/')
@APP.route('/platforms')
def show_in_piechart():
    """Show OS pie chart."""
    os_counts = get_platform_counts()
    return render_template('platform_chart_template', os_dict=os_counts)


# @APP.route('/tree')
# def show_in_treemap():
#     """Show OS treemap."""
#     os_dict = get_platform_counts()
#     return render_template('platform_tree_template', os_dict=os_dict)


@APP.route('/queries')
@APP.route('/query')
def show_all_queries():
    """List all queries from database."""
    return jsonify(get_all_queries())


@APP.route('/query/<int:query_id>')
def show_query(query_id):
    """Display query definition."""
    query = get_query(query_id)
    return jsonify(query)


@APP.route('/query_result/<int:query_id>')
def show_query_result(query_id):
    """Display query result."""
    result = get_query_result(query_id)
    return jsonify(result)


@APP.route('/devices/<string:platform>')
def list_devices(platform):
    """List all devices matching platform."""
    query_id = OS_DICT[platform].query_id
    devices = get_query_result(query_id)['values']
    headers = get_columns(3)
    return render_template('devices_template',
                           devices=devices,
                           headers=headers)


@APP.route('/devices/device_details/<string:device_name>')
def show_device_details(device_name):
    """List results of all DEVICE_QUERIES for device_name."""
    queries = prepare_device_queries(device_name)
    results = {query: get_query_result(data=queries[query], mode='POST')
               for query in queries}
    return render_template('details_template',
                           results=results,
                           queries=queries,
                           order=QUERY_LIST)


if __name__ == "__main__":
    APP.run(host='0.0.0.0')
