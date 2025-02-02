from xsd_datatype import *
from owlready2 import *


FILENAME_FORMAT = "rdfxml"

LIST_OF_OBJECT_PROPERTY_TYPE = ["Nothing", "Func", "Inv", "FuncInv", "Inverse"]

AFFERMATIVE_ANSWERS = ["y", "yes"]
NEGATIVE_ANSWERS = ["n", "no"]



LOOKUP_TYPE_DICT = {"integer":int, "bigint": Long, "long":Long, "int":int, "smallint":int, 
                    "float":float, "real":float, "numeric":Decimal, "decimal":Decimal,
                    "boolean": bool,
                    "char":str, "character":str, "text":str, "character varying":str,"character varying[]":str, "varchar":str,
                    "date": datetime.date, "time": datetime.time, "time without time zone": datetime.time, "timestamp":datetime.datetime,
                    "timestamp without time zone": datetime.datetime, "timestampwithout time zone": datetime.datetime}

TRUE_VALUE_LIST = ["t", "true", "TRUE", "True"]
FALSE_VALUE_LIST = ["f", "false", "FALSE", "False"]

NULL_TYPE_LIST = ["NULL", "", "{}", None, "null", "Null", " ", "{''}", "None", "NONE", "none"]

NUMERIC_TYPE_LIST = [int, Long, float, Decimal]
BOOLEAN_TYPE_LIST = [bool]
STRING_TYPE_LIST = [str]
TIME_TYPE_LIST = [datetime.date, datetime.time, datetime.datetime]


DATA_PROPERTY_SEPARATOR = "__"
DATA_PROPERTY_CONJUCTION = "_of_"
OBJECT_PROPERTY_SEPARATOR = "__"
STRING_INSTANCE_SEPARATOR = "__"

SPACE_REGULAR_EXPRESSION = "\s+"
FIRST_SPACE_REGULAR_EXPRESSION = "^\s+|\s+$"
FIRST_APEX_REGULAR_EXPRESSION = "^'|'$"
FIRST_DOUBLE_APEX_REGULAR_EXPRESSION = "^\"|\"$|(?<!^)\".*?(?<!\")\""
ANGULAR_PARENTESIS_REGULAR_EXPRESSION = "<[^>]*>"
VALUES_TO_INSERT_SPACE_REGULAR_EXPRESSION = "(?<=,)\s+" #finds all occurrences of whitespace following a comma
QUOTES_REGULAR_EXPRESSION = ",(?=(?:[^']*\'[^']*\')*[^']*$)" #finds all commas that are not within a pair of single quotes in the string.
FIRST_SEMICOLON_EXPRESSION = ";(?=[^;]*$)" # finds the semicolon that is not followed by other semicolons in the same string.


