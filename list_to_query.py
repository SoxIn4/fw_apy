"""Create and upload a query from a list of criteria."""

import json

import fw_apy

query_field = 'device_product_name'
query_list = 'model_list.txt'
match_logic = 'one'

criteria_expressions = []

with open(query_list) as criteria_keys:
    key_list = [line.rstrip().replace("'", '') for
                line in criteria_keys.readlines()]

for item in key_list:
    expression = {'column': query_field,
                  'component': 'Client',
                  'operator': 'is',
                  'qualifier': item}
    criteria_expressions.append(expression)

query_criteria = {'expressions': criteria_expressions,
                  'logic': match_logic}
new_query = {'criteria': query_criteria,
             'fields': [{'column': 'device_name',
                         'component': 'Client',
                         'display_name': 'Device Name'}],
             'main_component': 'Client',
             'name': 'Query From List'}

# Uncomment next line to print query details as a json string
# print json.dumps(new_query)

# Uncomment next 2 lines to upload query and print result of import
# result = fw_apy.import_query(new_query)
# print result

# Next 2 lines get results of query without importing and print raw response
query_result = fw_apy.get_query_result(mode='POST', data=new_query)
print query_result

# Uncomment next 2 lines to print just the reult values one by one
# for item in query_result['values']:
#     print item
