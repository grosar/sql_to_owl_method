from owlready2 import *
from xsd_datatype import *
from parameters import *
from relational_database import *
from ontology import *


class RDB2TBOXConverter():

    def __init__(self):
        pass
    
    def convert_rdb_to_owl(self, ontology_name: str, relational_database: RelationalDatabase):
        """
        Method which implements the conversion of the sql into owl.
        """
        ontology = Ontology(ontology_name)
        self._create_classes_and_object_properties(ontology, relational_database)
        self._add_data_properties_to_all_classes(ontology, relational_database)
        self._add_restrictions_to_all_classes(ontology, relational_database)

        return ontology
        
    def _create_classes_and_object_properties(self, ontology: Ontology, relational_database: RelationalDatabase):
        """
        Process the various type of table in order
        """
        tables = relational_database.get_tables_dict()
        for table_name, table in (tables.items()):
            #count_fk = table.get_number_of_fk_columns()
            columns_with_fk_references_table = [column_references_table.get_fk_table_name() for column_references_table in table.get_fk_columns().values()]
            count_fk = len(set(columns_with_fk_references_table))
            if count_fk == 0:
                self._process_no_fk_table(ontology, table)

            if count_fk == 1:
                self._process_1_fk_table(ontology, table)

            if count_fk == 2:
                self._process_2_fk_table(ontology, table)
            
            if count_fk > 2:
                self._process_n_fk_table(ontology, table)


    """
    CREATION OF CLASSES WITHOUT FK
    """
    def _process_no_fk_table(self, ontology: Ontology, table: Table):
        """
        It translates tables without foreign keys (starting from the self._owl_dict) in owl classes creating also
        the dataproperties with the corresponding axioms.
        """
        table_name = table.get_table_name()
        ontology.create_class(table_name, Thing, "Thing")

    
    """             
    CREATION OF CLASSES WITH 1 FK
    """
    def _process_1_fk_table(self, ontology: Ontology, table: Table):
        """
        Creates the owl classes starting from the table with only 1 fk.
        """
        self._verify_and_create_hierarchy(ontology, table)

                               
    """             
    CREATION OF CLASSES WITH 2 FK
    """
    def _process_2_fk_table(self, ontology: Ontology, table: Table):
        """
        Creates the owl classes starting from the table with only 2 fk.
        """
        table_with_fk = table
        
        self._verify_and_create_hierarchy(ontology, table)
        
        columns_with_fk_references_table = [column_references_table.get_fk_table_name() for column_references_table in table.get_fk_columns().values()]
        set_columns_with_fk_references_table = set(columns_with_fk_references_table)
   
        if len(set_columns_with_fk_references_table)!=1:
            """
                Select all the fk columns and the corresponding table of reference 
            """
        
            if len(table_with_fk.get_not_fk_columns().keys()) > 0:
                self._translate_more_than_1_fk_table_not_bridge(ontology, table_with_fk)
            else:
                self._translate_2fk_bridge_table(ontology, table_with_fk)
                        


                          
    def _process_n_fk_table(self, ontology: Ontology, table: Table):
        """
        Creates the owl classes starting from the table with more than 2 fk.
        """
        table_with_fk = table

        self._verify_and_create_hierarchy(ontology, table)

        columns_with_fk_references_table = [column_references_table for column_references_table in table.get_fk_tables_dict().keys()]
        set_columns_with_fk_references_table = set(columns_with_fk_references_table)

        
        if len(set_columns_with_fk_references_table)!=1:
            self._translate_more_than_1_fk_table_not_bridge(ontology, table_with_fk)
    


    def _verify_and_create_hierarchy(self, ontology: Ontology, table: Table):
        """
            It verifies if all the primary key attributes of the table are foreign key and if this foreign key
            points to the corresponding primary key of the reference table. The number of attributes of both the
            primary key must be the same. If these conditions are met than the table the user can decide if there is or not a hierarchy
            relationship.
        """
        table_with_fk = table

        RangeClass = None
        DomainClass = None
        referring_table = None

        notSubClassFlag = True
        #print("caso")
        if table.is_the_fk_columns_relative_to_one_table():
            
            referring_table = list(table.get_fk_tables_dict().values())[0][0]

            column_with_fk_reference_table = referring_table.get_table_name()
            
            if column_with_fk_reference_table not in ontology.get_created_classes():
                RangeClass = ontology.create_class(column_with_fk_reference_table, Thing, "Thing")
            RangeClass = ontology.get_created_classes()[column_with_fk_reference_table]

            """
                If all the fk column are primary key
            """
            fk_is_pk = all(column_with_fk.get_column_name() in table.get_pk_columns().keys() for column_with_fk in table.get_fk_columns().values())

            if fk_is_pk:
                """
                    If all the referenced column by the table with fk are primary key of such table 
                """
                references_is_pk = all(column_with_fk.get_fk_column_ref_name() in referring_table.get_pk_columns().keys() for column_with_fk in table.get_fk_columns().values())

                if references_is_pk and (len(table.get_pk_columns().keys())==len(referring_table.get_pk_columns().keys())):
                    """
                        Then domain class is subclass of range class
                    """

                    if acquire_user_choice(str(table.get_table_name()) + " is subclass of " + str(RangeClass) + "? (y/n)"): 
                        DomainClass = ontology.create_class(table.get_table_name(), RangeClass, column_with_fk_reference_table)
                        notSubClassFlag = False
                    else: 
                        DomainClass = ontology.create_class(table.get_table_name(), Thing, "Thing")


                    # DomainClass = ontology.create_class(table.get_table_name(), Thing, "Thing")


            if notSubClassFlag:
                """
                    Then domain class is not subclass of range class
                """
                
                DomainClass = ontology.create_class(table.get_table_name(), Thing, "Thing")
                for column in table_with_fk.get_columns().values():
                    ontology.add_1_to_many_object_properties_to_class(column, table_with_fk,
                        column_with_fk_reference_table, DomainClass, RangeClass)
        
        return DomainClass, RangeClass, referring_table, notSubClassFlag



    def _translate_more_than_1_fk_table_not_bridge(self, ontology: Ontology, table_with_fk: Table):
        for tuple_references in table_with_fk.get_fk_tables_dict().values():
            reference_column = tuple_references[1][0]
            column = tuple_references[2][0]

            """
                Creates the range class
            """
            if reference_column.get_table_name() not in ontology.get_created_classes():
                RangeClass = ontology.create_class(reference_column.get_table_name(), Thing, "Thing")
            else:
                RangeClass = ontology.get_created_classes()[reference_column.get_table_name()]


            """
                Creates the domain class
            """
            if table_with_fk.get_table_name() not in ontology.get_created_classes():
                DomainClass = ontology.create_class(table_with_fk.get_table_name(), Thing, "Thing")
            else:
                DomainClass = ontology.get_created_classes()[table_with_fk.get_table_name()]

            """
                Create the 1 to many object properties
            """
            ontology.add_1_to_many_object_properties_to_class(column, table_with_fk,
                reference_column.get_table_name(), DomainClass, RangeClass)


    def _translate_2fk_bridge_table(self, ontology: Ontology, table_with_fk: Table):
        Classes = []
        domain_table = None
        """
            Creates the classes to connect with the many to many relationship
        """
        for tuple_references in table_with_fk.get_fk_tables_dict().values():
            
            referenced_table = tuple_references[0]
            reference_column = tuple_references[1][0]

            if referenced_table.get_table_name() not in ontology.get_created_classes():
                RangeClass = ontology.create_class(referenced_table.get_table_name(), Thing, "Thing")
            else:
                RangeClass = ontology.get_created_classes()[referenced_table.get_table_name()]

            Classes.append((reference_column, referenced_table, RangeClass))

        domain_table = Classes[0][1]
        range_table = Classes[1][1]
        
        domain_object = Classes[0][2]
        range_object = Classes[1][2]

        """Creates the many to many association"""

        ontology.add_many_to_many_object_properties_to_class(domain_table, range_table.get_table_name(), domain_object, range_object, table_with_fk.get_table_name())

    def _add_data_properties_to_all_classes(self, ontology: Ontology, relational_database: RelationalDatabase):
        """
            This method iters on all the tables and adds to it the corresponding dataproperties starting
            from its columns.
        """
        DomainClass = None
        tables = relational_database.get_tables_dict()
        for table in tables.values():
            
            if table.get_table_name() in ontology.get_created_classes().keys():
                
                DomainClass = ontology.get_created_classes()[table.get_table_name()]
            else:
                print(table.get_table_name() + " IS A BRIDGE TABLE")

            if table.get_table_name() in ontology.get_classes_and_properties().keys():
                
                if len(ontology.get_classes_and_properties()[table.get_table_name()]["data_properties"]) == 0:
                    ontology.add_data_properties_to_class(table, DomainClass) 


    def _add_restrictions_to_all_classes(self, ontology: Ontology, relational_database: RelationalDatabase):
        """
            Adds all the restriction to all the classes.
        """
        for classes in ontology.get_classes_and_properties().values():
            if len(classes["data_properties"]) > 0:
                """If there are restriction, they are applied"""
                if len(classes["data_properties_restr"] + classes["object_properties_restr"]) >= 1:
                    ontology.add_restriction_to_class(classes["object"], classes["data_properties_restr"],
                        classes["object_properties_restr"]) 