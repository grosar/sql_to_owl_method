
from test_queries import sparql_query, porbec_parameter_query #substitute in sparql_query.
from rdb_2_tbox_converter import *
from rdb_2_abox_converter import *
from relational_database import *
from rdflib import Graph

graph = Graph()
graph.parse(porbec_parameter_query.TEST_OWL_FILE, format="application/rdf+xml")
result_sparql = []
for row in (graph.query(sparql_query.QUERY)):
    row_sparql = []
    for elem in row:
        if elem is not None:
            row_sparql.append(str(elem))
        else:
            row_sparql.append(elem)
    result_sparql.append(row_sparql)
for index, row in enumerate(result_sparql):
    print("ROW" + str(index+1)+ ": ", row)