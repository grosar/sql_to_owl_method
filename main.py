import argparse
from rdb_2_tbox_converter import *
from rdb_2_abox_converter import *
from relational_database import *
import pickle

if __name__ == '__main__':
    filename = "rdb.pkl"
    
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-ddl", "--ddl_file", type=str, help="the name of the ddl file in input")
    argParser.add_argument("-dml", "--dml_file", type=str, help="the name of the dml file in input")
    argParser.add_argument("-uri", "--uri_owl", type=str, help="the url of the owl file to create")
    argParser.add_argument("-owl", "--owl_filename", type=str, help="the owl filename to create")

    args = argParser.parse_args()
    if not os.path.isfile("rdb.pkl"):
        rdb = RelationalDatabase(args.ddl_file, args.dml_file)
        with open(filename, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(rdb, outp, pickle.HIGHEST_PROTOCOL)
    else:
        with open(filename, 'rb') as inp:  # Overwrites any existing file.
            rdb = pickle.load(inp)

    rdb_2_tbox_converter = RDB2TBOXConverter()

    ontology = rdb_2_tbox_converter.convert_rdb_to_owl(args.uri_owl, rdb)

    rdb_2_abox_converter = RDB2ABOXConverter()

    ontology = rdb_2_abox_converter.fill_ontology(ontology, rdb)

    ontology.write_owl_ontology_file(args.owl_filename, FILENAME_FORMAT)





