from simple_ddl_parser import DDLParser
from owlready2 import *
from xsd_datatype import *
import sqlparse
from parameters import *
import utilities

class RelationalDatabase():

    def __init__(self, DDLFilename, DMLFilename = None):
        owl_dict = self.new_parse_from_file(DDLFilename, False, True)
        owl_dict = self._reorganize_rdb_schema_dict(owl_dict)
        self._schema = owl_dict
        self._dict_tables = {}
        for table in owl_dict["tables"]:
            self._dict_tables[table["table_name"]] = Table(table["table_name"], table["columns"], table["primary_key"])


        for table in self._dict_tables.values():
            for original_column_name, column_reference in table._dict_foreign_keys_ref.items():
                if column_reference["table"] not in table._dict_foreign_keys_tables.keys():
                    table._dict_foreign_keys_tables[column_reference["table"]] = (self._dict_tables[column_reference["table"]],
                        [self._dict_tables[column_reference["table"]]._dict_columns[column_reference["column"]]], 
                        [self._dict_tables[table.get_table_name()]._dict_columns[original_column_name]])
                    table._dict_foreign_keys_columns[original_column_name] = self._dict_tables[column_reference["table"]]._dict_columns[column_reference["column"]]
                else:
                    table._dict_foreign_keys_tables[column_reference["table"]][1].append(
                        self._dict_tables[column_reference["table"]]._dict_columns[column_reference["column"]])
                    table._dict_foreign_keys_tables[column_reference["table"]][2].append(
                        self._dict_tables[table.get_table_name()]._dict_columns[original_column_name])
                    table._dict_foreign_keys_columns[original_column_name] = self._dict_tables[column_reference["table"]]._dict_columns[column_reference["column"]]
            
        if DMLFilename is not None:
            self.insert_data_into_database(DMLFilename)

    def get_dict_schema(self):
        return self._schema

    def get_tables_dict(self):
        return self._dict_tables

    def get_tables_name(self):
        return self._dict_tables.keys()
    
    def get_tables(self):
        return self._dict_tables.values()

    def get_tables_name_and_object(self):
        return self._dict_tables.items()

    def get_number_of_tables(self):
        return len(self._dict_tables)

    def insert_data_into_database(self, DMLFile):
        statements = take_insert_statements(DMLFilename=DMLFile)
        i = 0
        for statement in statements:
            table_name_into_insert, columns_to_substitute, list_values_to_insert = self.get_table_columns_and_values_of_an_insert(statement)
            for values_to_insert in list_values_to_insert:
                columns_dict = self.obtain_columns_dict(columns_to_substitute, values_to_insert)
                table = self.get_table_by_tablename(table_name_into_insert)
                table.insert_row(columns_dict)
            

    def get_table_by_tablename(self, table_name):
        return self._dict_tables[table_name]

    def get_primary_key_columns(self, table, all_columns_dict):
        primary_key_indices = []

        for primary_key in table["primary_key"]:
            for index_column_to_substitute, column_to_substitute in enumerate(all_columns_dict.keys()):
                if column_to_substitute == primary_key:
                    primary_key_indices.append(index_column_to_substitute)
        
        primary_key_columns_to_substitute = [re.sub("\s+", "", list(all_columns_dict.keys())[primary_key_index])  for primary_key_index in primary_key_indices]
        primary_key_values_to_insert = [re.sub("\s+", "", list(all_columns_dict.values())[primary_key_index]) for primary_key_index in primary_key_indices]
        
        return self.obtain_columns_dict(primary_key_columns_to_substitute, primary_key_values_to_insert)

    def get_table_columns_and_values_of_an_insert(self, statement):
        insert_statement_splitted = statement.split("VALUES")
        insert_table_plus_columns = insert_statement_splitted[0].split("INTO")[1]
        if "." in insert_table_plus_columns:
            insert_table_plus_columns = insert_table_plus_columns.split(".")[1]
        insert_table_plus_columns = insert_table_plus_columns.replace("\"", "").replace("\n", "")


        columns_to_substitute = []
        insert_table_name = None

        """Considering the format of the insert statement, the column of the class are detected."""
        if "(" not in insert_table_plus_columns:
            insert_table_name = re.sub(SPACE_REGULAR_EXPRESSION, "", insert_table_plus_columns) 
            columns_to_substitute = self._find_all_columns_to_substitute(insert_table_name, columns_to_substitute)
        else:
            insert_table_name = insert_table_plus_columns.split("(")[0]
            insert_table_name = re.sub(SPACE_REGULAR_EXPRESSION, "", insert_table_name) 
            columns_to_substitute = insert_table_plus_columns.split("(")[1].replace(")", "").split(",")

            columns_to_substitute_temp = []
            for column_to_substitute in columns_to_substitute:
                columns_to_substitute_temp.append(re.sub(FIRST_SPACE_REGULAR_EXPRESSION, "", column_to_substitute))

            columns_to_substitute = columns_to_substitute_temp

        insert_table_name = re.sub(SPACE_REGULAR_EXPRESSION, "", insert_table_name) 

        string_values_to_insert = re.sub(FIRST_SEMICOLON_EXPRESSION, "", insert_statement_splitted[1])
        list_values_to_insert = utilities.list_elements_inside_string(string_values_to_insert)
        list_values_to_insert_corr = []
        
        for values_to_insert in list_values_to_insert:
            values_to_insert = re.split(QUOTES_REGULAR_EXPRESSION, values_to_insert)
            values_to_insert_temp = []
            for value_to_insert in values_to_insert:
                values_to_insert_temp.append(re.sub(FIRST_SPACE_REGULAR_EXPRESSION, "", value_to_insert))
            
            values_to_insert = values_to_insert_temp
            
            values_to_insert = [re.sub(FIRST_APEX_REGULAR_EXPRESSION, "", value_to_insert).replace("''", "'") for value_to_insert in values_to_insert]
           
            list_values_to_insert_corr.append(values_to_insert)
        list_values_to_insert = list_values_to_insert_corr
        return insert_table_name, columns_to_substitute, list_values_to_insert

    def get_columns_without_fk(self, statement):
        insert_statement_splitted = statement.split("VALUES")
        insert_table_plus_columns = insert_statement_splitted[0].split("INTO")[1]
        if "." in insert_table_plus_columns:
            insert_table_plus_columns = insert_table_plus_columns.split(".")[1]
        insert_table_plus_columns = insert_table_plus_columns.replace("\"", "").replace("\n", "")

        columns_to_substitute = []

        if "(" not in insert_table_plus_columns:
            columns_without_fk = None
        else:
            columns_to_substitute = insert_table_plus_columns.split("(")[1].replace(")", "").split(",")
            columns_to_substitute_temp = []
            for column_to_substitute in columns_to_substitute:
                columns_to_substitute_temp.append(re.sub(FIRST_SPACE_REGULAR_EXPRESSION, "", column_to_substitute))

            columns_to_substitute = columns_to_substitute_temp
            columns_without_fk = columns_to_substitute
            

        return columns_without_fk

    def _find_all_columns_to_substitute(self, table_name, columns_to_substitute):
        table = self.get_table_by_tablename(table_name)
        for column_name in table.get_columns().keys():
            columns_to_substitute.append(column_name)

        return columns_to_substitute
    
    def find_fk_columns(self, table_name, columns_without_fk = None):
        columns_and_index_with_fk = []
        table = self.get_table_by_tablename(table_name)
        if columns_without_fk is None:
            for column_index, column in enumerate(table["columns"]):
                if ("references" in column) and (column["references"] is not None):
                    columns_and_index_with_fk.append((column_index, column))
                    
        else:
            for column_index, column in enumerate(table["columns"]):
                for column_without_fk in columns_without_fk:
                    if (column["name"] == column_without_fk) and ("references" in column) and (column["references"] is not None):
                        columns_and_index_with_fk.append((column_index, column))
        columns_with_fk = [column_and_index_with_fk[1] for column_and_index_with_fk in columns_and_index_with_fk]

            
        return columns_with_fk, columns_and_index_with_fk


    def obtain_columns_dict(self, columns, values):
        columns_dict = {}
        for column, value in zip(columns, values):
            columns_dict[column] = value

        return columns_dict

    def obtain_complete_columns_dict(self, columns, values):
        columns_dict = {}
        for column, value in zip(columns, values):
            columns_dict[column["name"]] = (column, value)

        return columns_dict

    def find_fk_table_and_columns(self, columns_with_fk_dict):
        table_and_columns_dict = {}
        
        for _, value in columns_with_fk_dict.items():
            column, value = value[0], value[1]
            table_and_columns_dict[column["references"]["table"]] = {}
            table_and_columns_dict[column["references"]["table"]][column["references"]["column"]] = value
        
        return table_and_columns_dict

    def new_parse_from_file(self, file_path: str, json_dump = False, group_by_type = False):
        """get useful data from ddl"""
        with open(file_path, "r",encoding="utf-8") as df:
            return DDLParser(df.read()).run(file_path=file_path, json_dump=json_dump, group_by_type=group_by_type)


    def _reorganize_rdb_schema_dict(self, original_dict):
        new_dict = {}

        new_dict["ddl_properties"] = original_dict["ddl_properties"]
        new_dict["domains"] = original_dict["domains"]
        new_dict["schemas"] = original_dict["schemas"]
        new_dict["sequences"] = original_dict["sequences"]

        new_dict["tables"] = []

        old_tables = original_dict["tables"]

        for table_index, table in enumerate(old_tables):
            new_dict["tables"].append({})

            new_dict["tables"][table_index]["checks"] = table["checks"]
            new_dict["tables"][table_index]["columns"] = table["columns"]

            new_dict["tables"][table_index]["index"] = table["index"]
            new_dict["tables"][table_index]["partitioned_by"] = table["partitioned_by"]
            new_dict["tables"][table_index]["primary_key"] = table["primary_key"]
            new_dict["tables"][table_index]["schema"] = table["schema"]
            new_dict["tables"][table_index]["table_name"] = table["table_name"]
            new_dict["tables"][table_index]["tablespace"] = table["tablespace"]

            old_alters = table["alter"]

            if old_alters.get("columns") is not None:
                for alter_column in old_alters["columns"]:
                    
                    """
                    Sostituisce le alter su FK con FK normali 
                    """
                    for new_column in new_dict["tables"][table_index]["columns"]:
                        if alter_column["name"] == new_column["name"]:
                            new_column["references"] = alter_column["references"]

            if old_alters.get("primary_keys") is not None:
                new_dict["tables"][table_index]["primary_key"] = old_alters["primary_keys"][0]["columns"]

            if old_alters.get("uniques") is not None:
                for unique in old_alters["uniques"]:
                    if new_dict["tables"][table_index].get("column") is not None:
                        for column in new_dict["tables"][table_index]["column"]:
                            if column["name"] == unique["columns"]:
                                column["unique"] = True
                        
        return new_dict        

def take_insert_statements(DMLFilename):
    with open(DMLFilename, "r", encoding="utf8") as file1:
        read_content = file1.read()
    statements = sqlparse.split(read_content)
    new_statements = []
    for statement in statements:
        new_statements.append(sqlparse.format(statement, strip_comments=True).strip())
    statements = new_statements

    return statements

class Table():
    def __init__(self, table_name = None, list_column = None, primary_keys = None):
        self._table_name = table_name
        self._dict_columns, self._dict_primary_keys, self._dict_foreign_keys_ref = self.fill_columns(table_name, list_column, primary_keys)
        self._dict_columns_with_fk, self._dict_columns_without_fk = self.takes_fk_and_not_fk_columns()
        self._dict_foreign_keys_tables = {}
        self._dict_foreign_keys_columns = {}
        self._rows = {}
    

    def set_table(self, table_name, list_column, primary_keys):
        self._dict_columns, self._dict_primary_keys, self._dict_foreign_keys_ref = self.fill_columns(table_name, list_column, primary_keys)

    def get_table_name(self):
        return self._table_name

    def get_pk_columns(self):
        return self._dict_primary_keys

    def get_columns(self):
        return self._dict_columns

    def get_fk_columns(self):
        return self._dict_columns_with_fk

    def get_not_fk_columns(self):
        return self._dict_columns_without_fk

    def get_fk_tables_dict(self):
        return self._dict_foreign_keys_tables

    def get_dict_fk_columns(self):
        return self._dict_foreign_keys_columns
    
    def get_number_of_columns(self):
        return len(self._dict_columns.keys())

    def get_number_of_fk_columns(self):
        return len(self._dict_foreign_keys_columns.keys())

    def get_number_of_n_fk_columns(self):
        return (len(self._dict_columns.keys()) - len(self._dict_foreign_keys_columns.keys()))

    def get_column_by_name(self, column_name):
        return self._dict_columns[column_name]

    def get_rows(self):
        return self._rows

    def get_rows_id(self):
        return self._rows.keys()

    def get_rows_id_and_values(self):
        return self._rows.items()

    def get_rows_columns_and_values_by_row_id(self, row_id):
        return self._rows[row_id]

    def is_the_fk_columns_relative_to_one_table(self):
        column_fk_table_name = []
        for column_fk in self._dict_columns_with_fk.values():
            column_fk_table_name.append(column_fk._fk_table_name)
        return (len(set(column_fk_table_name)) == 1)

    def takes_fk_and_not_fk_columns(self):
        columns_with_fk = {}
        columns_without_fk = {}
        for column in self.get_columns().values():
            if column.is_fk():
                columns_with_fk[column.get_column_name()] = column
            else:
                columns_without_fk[column.get_column_name()] = column

        return columns_with_fk, columns_without_fk

    def fill_columns(self, table_name, list_column, primary_keys):
        dict_columns = {}
        dict_primary_keys = {}
        dict_foreign_keys_ref = {}
        for column in list_column:
            
            fk = False
            if column["references"] is not None:
                fk = True

            pk = False
            if column["name"] in primary_keys:
                pk = True
                
            if fk:
                column_object = Column(table_name, column["name"], column["check"], column["default"], column["nullable"], pk,
                                                        fk, column["references"]["table"], column["references"]["column"], column["size"], column["type"], column["unique"], column["references"]["on_delete"])
            else:
                column_object = Column(table_name, column["name"], column["check"], column["default"], column["nullable"], pk,
                                                        fk, None, None, column["size"], column["type"], column["unique"], None)

            dict_columns[column["name"]] = column_object

            if pk:
                dict_primary_keys[column["name"]] = column_object
            
            if fk:
                dict_foreign_keys_ref[column["name"]] = column["references"]
            
        return dict_columns, dict_primary_keys, dict_foreign_keys_ref

    def insert_row(self, columns_dict):
        primary_string = ""
        for column_name, value in columns_dict.items():
            if column_name in self._dict_primary_keys.keys():
                if primary_string == "":
                    primary_string = primary_string + column_name + STRING_INSTANCE_SEPARATOR + str(value)
                else:
                    primary_string = primary_string + STRING_INSTANCE_SEPARATOR + column_name + STRING_INSTANCE_SEPARATOR + str(value)
        self._rows[primary_string] = {}
        
        for column_name, value in columns_dict.items():
            column = self._dict_columns[column_name]
            self._rows[primary_string][column_name] = (column, value)

        return self._rows[primary_string]


class Column():
    def __init__(self, table_name, column_name, check, default, nullable, pk, fk, fk_table_name, fk_column_name_ref, size, type, unique, on_delete):
        self._table_name = table_name
        self._column_name = column_name
        self._check = check
        self._default = default
        self._nullable = nullable
        self._pk = pk
        self._fk = fk
        self._fk_table_name = fk_table_name
        self._fk_column_name_ref = fk_column_name_ref
        self._size = size
        self._type = type
        self._unique = unique
        self._on_delete = on_delete

    def get_table_name(self):
        return self._table_name

    def set_table_name(self, table_name):
        self._table_name = table_name

    def get_column_name(self):
        return self._column_name

    def set_column_name(self, column_name):
        self._column_name = column_name

    def get_check(self):
        return self._check

    def set_check(self, check):
        self._check = check

    def get_default(self):
        return self._default

    def set_default(self, default):
        self._default = default

    def is_nullable(self):
        return self._nullable

    def set_nullable(self, nullable):
        self._nullable = nullable

    def is_pk(self):
        return self._pk

    def set_pk(self, pk):
        self._pk = pk

    def is_fk(self):
        return self._fk

    def set_fk(self, fk):
        self._fk = fk

    def get_fk_table_name(self):
        return self._fk_table_name

    def set_fk_table_name(self, fk_table_name):
        self._fk_table_name = fk_table_name
    
    def get_fk_column_ref_name(self):
        return self._fk_column_name_ref

    def set_fk_column_ref_name(self, fk_column_name_ref):
        self._fk_column_name_ref = fk_column_name_ref

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._type = type

    def is_unique(self):
        return self._unique

    def set_unique(self, unique):
        self._unique = unique

    def on_delete_is_cascade(self):
        return str.lower(self._on_delete) == "cascade"



