======= Description ========

use pip install -r requirements.txt in order to install all the dependencies

In order to translate a Relational Database into an OWL ontology:

    1) create an SQL DDL File with the database schema (this SQL DDL file can be parsed only according to statement supported
                                by the library https://pypi.org/project/simple-ddl-parser/)
    2) create an SQL DML File with all the insert relative to that schema
    3) run main.py -ddl "sql_ddl_filename" -dml "sql_dml_filename" -uri "desired uri" -owl "desired_owl_filename"


the file execute_sql_query.py
    Such file is required to execute a sql query in a postgres database. 
    To do this the parameters for the connection to the postgres database must be setted in the sql_folder\sql_parameter.py.
    The QUERY must be setted in test_queries\sql_query.py

the file execute_sparql_query.py
    Such file is required to execute a sparql on the file with filename TEST_OWL_FILE that can be modified in test_queries\porbec_parameter_query.py. 
    The QUERY must be setted in test_queries\sparql_query.py