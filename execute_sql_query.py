import psycopg2 
from test_queries import sql_query #substitute here the sql query to execute.
from rdb_2_tbox_converter import *
from rdb_2_abox_converter import *
from relational_database import *
from sql_folder import sql_parameter

con = psycopg2.connect(
    database=sql_parameter.DATABASE_NAME,
    user=sql_parameter.USER_DATABASE,
    password=sql_parameter.PASSWORD,
    host=sql_parameter.HOST,
    port= sql_parameter.PORT
)

cursor_obj = con.cursor()

cursor_obj.execute(sql_query.QUERY)
result_sql = cursor_obj.fetchall()
result_sql = [list(row) for row in result_sql]

for index, row in enumerate(result_sql):
    print("ROW" + str(index+1)+ ": ", row)