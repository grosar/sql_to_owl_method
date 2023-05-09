from owlready2 import *
from xsd_datatype import *
from parameters import *
from relational_database import *
from ontology import *

"""
Given an ontology and an dml sql file, fill the triples
"""
class RDB2ABOXConverter():

    def __init__(self):
        """
        """
        pass


    def fill_ontology(self, ontology: Ontology, rdb: RelationalDatabase):
        """
            The methods implements the ABOX algorithm for the conversion of the data inside a database into
            an owl ontology.
            parameters:
                ontology: Ontology object
                rdb: Relational database object

        """
        
        self._create_instances_of_classes(ontology, rdb)
        self._create_instances_of_properties(ontology, rdb)
        self._identify_same_individuals(ontology, rdb)
        return ontology
            

    def _create_instances_of_classes(self, ontology: Ontology, rdb: RelationalDatabase):
        """
            The method takes in input a relational database object which contains all the tables and the rows of such tables
            and iterates over them in order to create each instance and for each instance the necessary data properties.
            parameters:
                ontology: Ontology object
                rdb: Relational database object

        """        
        for table in rdb.get_tables(): ####### iterate over the tables
            for row_id, row__column_dict in table.get_rows_id_and_values(): ### iterate over the table rows id and column_value
                if table.get_table_name() in ontology.get_created_classes():
                    instance_name = table.get_table_name() + "_instance_" + row_id
                    instance = ontology.create_instance(table.get_table_name(), instance_name) 
                    ontology.put_hierarchy_property_instance(table.get_table_name(), row_id, instance) 
                    for column_name, column_value_tuple in row__column_dict.items(): # take column and value
                        data_property_name = column_name + DATA_PROPERTY_CONJUCTION + table.get_table_name()
                        if data_property_name in ontology.get_created_data_property():
                            if column_value_tuple[1] not in NULL_TYPE_LIST: # if there is a value to insert
                                type_col = LOOKUP_TYPE_DICT[column_value_tuple[0].get_type()]
                                ontology.create_data_property_instance(instance, type_col, data_property_name,
                                    instance_name, column_name, column_value_tuple[1])

                    
    def _create_instances_of_properties(self, ontology: Ontology, rdb: RelationalDatabase):
        """
            The method creates for each instances the necessary object property instances if exists.
            parameters:
                ontology: Ontology object
                rdb: Relational database object

        """ 
        for table in rdb.get_tables(): # iterate over the tables
            if table.get_number_of_fk_columns() != 0: # if the tables have more than 0 fks
                if table.get_table_name() in ontology.get_created_classes():
                    for row_id in table.get_rows(): # iterate over the id of the instances

                        domain_instance_name = table.get_table_name() + "_instance_" + row_id 
                        domain_instance = ontology.get_instance_object_by_name(domain_instance_name) # take the domain instance

                        for range_table_name, tuple in table.get_fk_tables_dict().items():
                                name_columns_fk = [column.get_column_name() for column in tuple[1]] # take the referenced columns
                                name_columns_ori = [column.get_column_name() for column in tuple[2]] # take the columns with the reference
                                name_columns_pk = [column_name for column_name in table.get_pk_columns().keys()] # take the primary key columns

                                if table.get_table_name() != range_table_name:
                                    ### use the reference columns name starting from the referenced value of the fks 
                                    primary_string_range = construct_primary_key_string(table, row_id,
                                        name_columns_fk, name_columns_ori)
                                else:
                                    ### use the reference columns name starting from the pk of the tables (because the fks reference to the pk itself)
                                    primary_string_range = construct_primary_key_string(table, row_id,
                                        name_columns_pk, name_columns_ori)

                                if range_table_name in ontology.get_classes_and_properties()[table.get_table_name()]["object_properties"]: # iterate over the object properties
                                    # takes the direct object properties
                                    direct_property = ontology.get_classes_and_properties()[table.get_table_name()]["object_properties"][range_table_name]["direct"]
                                    if primary_string_range is not None:
                                        range_instance_name = range_table_name + "_instance_" + primary_string_range
                                        # get the range instance
                                        range_instance = ontology.get_instance_object_by_name(range_instance_name)
                                        if not ontology.is_in_object_property_instance(domain_instance_name, range_instance_name):
                                            # create the object property using the domain instance, the range instance and the direct property
                                            ontology.create_object_property_instance(domain_instance, range_instance, direct_property)
                                            ontology.set_object_property_instance(domain_instance_name, range_instance_name)
                                            ontology.set_object_property_instance(range_instance_name, domain_instance_name)    

                else: # if the table is a bridge table
                    for row_id in table.get_rows(): #iterates over the id of the table
                        instance_dict = {}
                        table_names = []    
                        # take the instance referenced by each row of the bridge tables          
                        for table_p_name, prop_table_tuple in table.get_fk_tables_dict().items(): 
                            name_columns_fk = [column.get_column_name() for column in prop_table_tuple[1]]
                            name_columns_ori = [column.get_column_name() for column in prop_table_tuple[2]]
                            primary_string_range = construct_primary_key_string(table, row_id ,name_columns_fk, name_columns_ori)
                            instance_dict[table_p_name] = ontology.get_instance_object_by_name(table_p_name + "_instance_" + primary_string_range)
                            table_names.append(table_p_name)
                        domain_instance = instance_dict[table_names[0]]
                        range_instance = instance_dict[table_names[1]]

                        # once the instances are identified, creates the object property instance between them (the object property
                        # is that resulting from the bridge table) 
                        direct_property = ontology.get_classes_and_properties()[table_names[0]]["object_properties"][table_names[1]]["direct"]

                        ontology.create_object_property_instance(domain_instance, range_instance, direct_property)

    def _identify_same_individuals(self, ontology: Ontology, rdb: RelationalDatabase):
        """
        This method identify when two instances of two class-subclass are the same individual
        In this way the ontology create a same individual axioms.
        parameters:
                ontology: Ontology object
                rdb: Relational database object
        """
        for subclass_name, values_subclass in ontology.get_hierarchy_property_instance().items():
            if values_subclass["name_subclass_of"] is not None and values_subclass["name_subclass_of"] != "Thing":
                values_father_class = ontology.get_father_class(values_subclass["name_subclass_of"])
                for row_id_subclass, instance_subclass in values_subclass["instance_map"].items():
                    for row_id_fatherclass, instance_father_class in values_father_class["instance_map"].items():
                        ids_subclass = [id_string for index, id_string in enumerate(row_id_subclass.split(STRING_INSTANCE_SEPARATOR)) if index%2!=0]
                        count = 0
                        for id_subclass in ids_subclass:
                            if id_subclass in row_id_fatherclass:
                                count += 1
                        if count == len(ids_subclass):
                            instance_subclass.equivalent_to.append(instance_father_class)

def construct_primary_key_string(table, name_instance, name_columns_fk, name_columns_ori):
    """Build the string which identify an instance starting from the name of the instance, the referenced columns, the columns which have the reference
    (which also contains) the value
        parameters:
        name_instance: string which is the name of the instance
        name_columns_fk: the referenced columns
        name_columns_ori: the columns which have the reference
    """
    primary_string = ""  
    for column_name_fk, column_name_ori in zip(name_columns_fk, name_columns_ori):
        if column_name_ori not in table.get_rows()[name_instance]:
            return None
        value = table.get_rows()[name_instance][column_name_ori][1]
        if value == "NULL":
            return None
        if primary_string == "":
            primary_string = primary_string + column_name_fk + STRING_INSTANCE_SEPARATOR + str(value)
        else:
            primary_string = primary_string + STRING_INSTANCE_SEPARATOR + column_name_fk + STRING_INSTANCE_SEPARATOR + str(value)

    return primary_string
