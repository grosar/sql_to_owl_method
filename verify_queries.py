import psycopg2 
from test_queries import porbec_parameter_query
from rdb_2_tbox_converter import *
from rdb_2_abox_converter import *
from relational_database import *
from rdflib import Graph
from tqdm import tqdm
from sql_folder import sql_parameter

# THIS FILE IS ONLY FOR AUTOMATICALLY EXECUTING THE QUERY OF THE DATABASE PORBEC LEAVED IN THE REPOSITORY.
# FOR EXECUTING THIS THE DATABASE PORBEC MUST BE LOADED IN A POSTGRES DATABASE AND THE PARAMETERS OF SUCH 
# DATABASE MUST BE CONFIGURED IN THE sql_folder/sql_parameter.py file.
# THEN THE PORBEC ONTOLOGY MUST BE CREATED AND THE FILE EXECUTED WITH THE RIGHT FILENAME. 
# FOR THE SAKE OF SIMPLICITY, THE OWL FILE GENERATED IS ALREADY PRESENT IN THE ontology_folder

con = psycopg2.connect(
database=sql_parameter.DATABASE_NAME,
user=sql_parameter.USER_DATABASE,
password=sql_parameter.PASSWORD,
host=sql_parameter.HOST,
port= sql_parameter.PORT
)

cursor_obj = con.cursor()
dict_combinations_per_parameter_sql = {}

for name, query in porbec_parameter_query.dict_sql_queries_for_parameters.items():
    cursor_obj.execute(query)
    result = cursor_obj.fetchall()
    dict_combinations_per_parameter_sql[name] = result
    if len(dict_combinations_per_parameter_sql[name][0]) == 1:
        dict_combinations_per_parameter_sql[name] = [result[0] for result in dict_combinations_per_parameter_sql[name]]
    else:
        dict_combinations_per_parameter_sql[name] = [[result[0], result[1]] for result in dict_combinations_per_parameter_sql[name]]

    

graph = Graph()
graph.parse(porbec_parameter_query.TEST_OWL_FILE, format="application/rdf+xml")

dict_results = {"spes": [], "collection" : [],
            "card": [], "author": [], "materia": [], "tecnica": [],
            "materia_tecnica": []}

dict_combinations_per_parameter_sparql = dict_combinations_per_parameter_sql
    
count_query = 0
for type_parameter, list_queries in porbec_parameter_query.queries.items():
    list_sql_parameters = dict_combinations_per_parameter_sql[type_parameter]
    list_sparql_parameters = dict_combinations_per_parameter_sparql[type_parameter]
    for query_in_list in list_queries:
        if type_parameter != "materia_tecnica":
            for sql_parameter in tqdm(list_sql_parameters):
                count_query += 1
                cursor_obj.execute(query_in_list["sql_query"].format(sql_parameter.replace("'", "''")))
                result_sql = cursor_obj.fetchall()
                result_sql = [list(row) for row in result_sql]
                result_sparql = []
                for row in (graph.query(query_in_list["sparql_query"].format(sql_parameter))):
                    row_sparql = []
                    for elem in row:
                        if elem is not None:
                            row_sparql.append(str(elem))
                        else:
                            row_sparql.append(elem)
                    result_sparql.append(row_sparql)
                dict_results[type_parameter].append({"name_query": query_in_list["name_query"], 
                "result_sql" : result_sql, "result_sparql" : result_sparql,
                "parameter_sql": sql_parameter})
        else:
            for sql_parameter in tqdm(list_sql_parameters):
                count_query += 1
                materia_parameter = sql_parameter[0]
                tecnica_parameter = sql_parameter[1]
                cursor_obj.execute(query_in_list["sql_query"].format(materia_parameter.replace("'", "''"), tecnica_parameter.replace("'","''")))
                result_sql = cursor_obj.fetchall()
                result_sql = [list(row) for row in result_sql]
                result_sparql = []
                if tecnica_parameter == '':
                    piece_of_query = "FILTER NOT EXISTS {{ ?mattec porbec:tecnica_of_mav_materia_tecnica ?dataprop }}"
                else:
                    piece_of_query = """?mattec porbec:tecnica_of_mav_materia_tecnica "{}"^^xsd:string.""".format(tecnica_parameter)
                
                for row in (graph.query(query_in_list["sparql_query"].format(materia_parameter, piece_of_query))):
                    row_sparql = []
                    for elem in row:
                        if elem is not None:
                            row_sparql.append(str(elem))
                        else:
                            row_sparql.append(elem)
                    result_sparql.append(row_sparql)
                dict_results[type_parameter].append({"name_query": query_in_list["name_query"], 
                "result_sql" : result_sql, "result_sparql" : result_sparql,
                "parameter_sql": sql_parameter})

# #print(dict_results)
    for index, dict in enumerate(dict_results[type_parameter]):
        print("========="  + str(index) + "=============")
        
        print("NAME QUERY: ", dict["name_query"])
        print("PARAMETER_SQL:",dict["parameter_sql"])
        # print("RESULT_SQL: ", dict["result_sql"])
        # print("RESULT_SPARQL: ", dict["result_sparql"])
        if len(dict["result_sql"]) != len(dict["result_sparql"]):
            for row in dict["result_sql"]:
                for elem in row:
                    if elem not in NULL_TYPE_LIST:
                        print("=======LEN SQL:", len(dict["result_sql"]))
                        print("=======LEN SPARQL:", len(dict["result_sparql"]))
                        print("RESULT NOT EQUAL")
                        exit(-1)
            for row in dict["result_sparql"]:
                for elem in row:
                    if elem not in NULL_TYPE_LIST:
                        print("=======LEN SQL: ", len(dict["result_sql"]))
                        print("=======LEN SPARQL:", len(dict["result_sparql"]))
                        print("RESULT NOT EQUAL")
                        exit(-1)
        for row_sql, row_sparql in zip(dict["result_sql"], dict["result_sparql"]):
            for sql_elem, sparql_elem in zip(row_sql, row_sparql):
                if sql_elem not in NULL_TYPE_LIST:
                    if type(sql_elem) is list and type(sparql_elem) is str:
                        if str.lower(str(sql_elem[0])) != str.lower(str(sparql_elem).replace("{\"", "").replace("\"}", "")):
                            print("=======SQL: ", str.lower(str(sql_elem)))
                            print("=======SPARQL:", str.lower(str(sparql_elem)))
                            print("RESULT NOT EQUAL")
                            exit(-1)
                    else:
                        if str.lower(str(sql_elem)) != str.lower(str(sparql_elem)):
                            print("=======SQL: ", str.lower(str(sql_elem)))
                            print("=======SPARQL:", str.lower(str(sparql_elem)))
                            print("RESULT NOT EQUAL")
                            exit(-1)
                else:
                    if sparql_elem not in NULL_TYPE_LIST:
                        print("=======SQL: ", str.lower(str(sql_elem)))
                        print("=======SPARQL:", str.lower(str(sparql_elem)))
                        print("RESULT NOT EQUAL")
                        exit(-1)
print("IT'S ALL OK")
print("TOTAL NUMBER OF QUERY EXECUTED:", count_query) # 32800 query
cursor_obj.close()
con.close()