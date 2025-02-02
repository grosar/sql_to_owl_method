from dateutil import parser
from owlready2 import *
from xsd_datatype import *
from parameters import *
from relational_database import *
from utilities import *

class Ontology():

    def __init__(self, name_ontology):
        """
        Attributes:
            self._onto = Ontology object of OWLReady2
            self._created_classes = dict: {classname: owlready2 class object}
            self._data_properties = dict: {dataproperty_name: owlready2 dataproperty object}
            self._created_object_property = dict: {objectproperty_name:owlready2 objectproperty object}
            self._classes_and_properties = dict:  {"class_name": owlready2 class object, "data_properties": {}, "object_properties": {},
                "object_properties_restr":[], "data_properties_restr":[]}
            self._created_instances = dict: {"instance_name": {"object": instance, "column_name": column_instance...}}
            self._hierarchy_structure_instance = dict: {"class_name": {"instance_map": {"id_name": instance_object} "name_subclass_of": name of the subclass} }
            self._object_property_instance = dict: {domain_instance_name: []}
        """
        self._onto = get_ontology(name_ontology)
        self._created_classes = {}
        self._table_converted_in_properties = {}
        self._created_data_property = {}
        self._created_object_property = {}
        self._classes_and_properties = {}
        self._created_instances = {}
        self._hierarchy_structure_instance = {}
        self._object_property_instance = {}

    def write_owl_ontology_file(self, OWLFilename, format):
        """
        Save an ontology as owl file
            parameters:
                OWLFilename: string which is the filename of the owl to create
                format: format in which the ontology must be saved
        """
        self._onto.save(file=OWLFilename, format=format) 

    def put_hierarchy_property_instance(self, class_name, id, instance):
        """
        Save an instance of a certain class_name with a specific id.
            parameters:
                OWLFilename: string which is the filename of the owl to create
                format: format in which the ontology must be saved
        """
        self._hierarchy_structure_instance[class_name]["instance_map"][id] = instance

    def get_hierarchy_property_instance(self):
        """
        Get the hierarchy dict
        """
        return self._hierarchy_structure_instance

    def get_father_class(self, class_name):
        """
        Get the father class of the class with class_name as name.
            parameters:
                class_name: the name of the class of which we want the father class
        """
        return self.get_hierarchy_property_instance()[class_name] 

    def get_instance_by_class_and_id(self, class_name, id):
        """
        Get the father class of the class with class_name as name.
            parameters:
                class_name: the name of the class of which we want the instance
                id: the id of the instance
        """
        return self._hierarchy_structure_instance[class_name]["instance_map"][id]

    def get_created_classes(self):
        """
        Return the dictionary of the classes {"name_class": object_class}
        """
        return self._created_classes

    def get_table_converted_in_properties(self):
        """
        Return a dictionary with the properties resulting from a bridge table
        """
        return self._table_converted_in_properties
    
    def get_created_data_property(self):
        """
        Return a dictionary with the data properties {"name_data_property": object_data_property}
        """
        return self._created_data_property

    def get_created_object_property(self):
        """
        Return a dictionary with the object properties {"name_object_property": object_object_property}
        """
        return self._created_object_property

    def get_classes_and_properties(self):
        """Return the dictionary  {"class_name": owlready2 class object, "data_properties": {}, "object_properties": {},
                "object_properties_restr":[], "data_properties_restr":[]}"""
        return self._classes_and_properties

    def set_object_property_instance(self, domain_instance_name, range_instance_name):
        """
        Save an instance of object property between two instances
            parameters: 
                domain_instance_name: name of the domain instance
                range_instance_name: name of the range instance
        """
        if domain_instance_name not in self._object_property_instance:
            self._object_property_instance = {domain_instance_name: []}
        else:
            self._object_property_instance[domain_instance_name].append(range_instance_name)

    def is_in_object_property_instance(self, domain_name, range_name):
        """
        Verify if an object property instance has been already created between two object
            parameters:
                domain_name: name of the domain instance
                range_name: name of the range instace
        """
        return ((domain_name in self._object_property_instance) and (range_name in self._object_property_instance[domain_name]))


    def create_class(self, class_name, subclass_of, name_subclass_of):
        """
            Create a class specifing also of which is the subclass.
            parameters:
                table_name: the name of the class to create
                subclass_of: the father class (owlready2)
                name_subclass_of: name of the father class
        """
        with self._onto:
            NewClass = types.new_class(class_name, (subclass_of,))
            if class_name not in self._classes_and_properties:
                self._created_classes[class_name] = NewClass
                self._classes_and_properties[class_name] = {"object": NewClass, "data_properties": {}, "object_properties": {},
                "object_properties_restr":[], "data_properties_restr":[]}
                self._hierarchy_structure_instance[class_name] = {"name_subclass_of": name_subclass_of, "instance_map": {}}
        return NewClass


    def create_data_property(self, table_name, column_name , column_type, DomainClass, not_null = False, unique = False):
        """
            Create a data property and add it to the DomainClass.
            parameters:
                table_name: name of the class
                column_name: name of the column
                column_type: type of the column
                DomainClass: domain class object owlready2
                not_null: not null flag
                unique: unique flag (not used in owl-full)
        """
        with self._onto:
            NewDataProperty = types.new_class((column_name) + DATA_PROPERTY_CONJUCTION + (table_name), 
                (DomainClass >> LOOKUP_TYPE_DICT[str.lower(column_type)], FunctionalProperty))
            Restr = None

            if not_null:
                """If there is the not_null constraint then cardinality = 1"""
                Restr = (NewDataProperty.exactly(1, LOOKUP_TYPE_DICT[str.lower(column_type)]))
            else:
                """If there is not the constraint not_null then max_cardinality = 1"""
                Restr = (NewDataProperty.max(1, LOOKUP_TYPE_DICT[str.lower(column_type)]))

            self._created_data_property[column_name + DATA_PROPERTY_CONJUCTION + table_name] = NewDataProperty
            self._classes_and_properties[table_name]["data_properties"][column_name] = \
            {"property": NewDataProperty, "domain": DomainClass, "range": LOOKUP_TYPE_DICT[str.lower(column_type)]}
            return NewDataProperty, Restr

    def create_object_property(self, domain_table_name, range_table_name, DomainClass, RangeClass, type_prop = "Nothing", 
                                original_property_name = None, bridge_table = None, column = None):
        """
            Create an object property between a DomainClass and RangeClass.
            parameters:
                domain_table_name: domain class name
                range_table_name: range class name
                column_type: type of the column
                DomainClass: domain class object owlready2
                RangeClass: range class object owlready2
                type_prop: type of the property to create (Functional, InverseFunctional)
                original_property_name: property of the original property (in case of inverse)
                bridge_table: flag to assess if the object property has been created from a bridge table
                column: column object
        """
        if type_prop not in LIST_OF_OBJECT_PROPERTY_TYPE:
            return None

        NewObjectProperty = None
        functional_property = False
        inverse_functional_property = False
        name_property = ""
        with self._onto:
            same_range = True
            if domain_table_name == range_table_name and type_prop != "Inverse":
                # print(column._column_name)
                
                if acquire_user_choice(str(column.get_column_name()) + " of " + domain_table_name + " table is Symmetric? (y/n)"): 
                    same_range = False
                    name_property = domain_table_name + "_" + column.get_column_name()
                    NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass, SymmetricProperty))

                if column.on_delete_is_cascade():
                    if acquire_user_choice(str(column.get_column_name()) + " of " + domain_table_name + " table is Transitive? (y/n)"): 
                        same_range = False
                        name_property = domain_table_name + "_" + column.get_column_name()
                        NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass, TransitiveProperty))

            if type_prop == "Nothing" and bridge_table is not None and same_range:
                name_property = bridge_table
                NewObjectProperty = types.new_class(bridge_table, (DomainClass >> RangeClass,)) 

            elif type_prop == "Func" and same_range:
                name_property =  domain_table_name + "_has_a_" + column.get_column_name() + "_of_" + range_table_name
                NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass, FunctionalProperty))
                functional_property = True

            elif type_prop == "Inv" and same_range:
                name_property =  domain_table_name + "_has_a_" + column.get_column_name() + "_of_" + range_table_name
                NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass, InverseFunctionalProperty))
                inverse_functional_property = True

            elif type_prop == "FuncInv" and same_range:
                name_property =  domain_table_name + "_has_a_" + column.get_column_name() + "_of_" + range_table_name
                NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass, FunctionalProperty, InverseFunctionalProperty))
                functional_property = True
                inverse_functional_property = True

            elif type_prop == "Inverse" and domain_table_name == range_table_name:
                name_property =  "INV_" + original_property_name
                NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass,))

            elif type_prop == "Inverse" and original_property_name is not None and bridge_table is None and same_range:
                name_property =  domain_table_name + "_belongs_to_" + column.get_column_name() + "_of_" + range_table_name
                NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass,))

            elif type_prop == "Inverse" and original_property_name is not None and bridge_table is not None and same_range:
                name_property =  "INV_" + original_property_name
                NewObjectProperty = types.new_class(name_property, (DomainClass >> RangeClass,))
        
        """Save the properties that are created in this function"""
        #self._created_object_property[domain_table_name + OBJECT_PROPERTY_SEPARATOR + range_table_name] = NewObjectProperty

        if not bridge_table:

            if range_table_name not in self._classes_and_properties[domain_table_name]["object_properties"]:
                self._classes_and_properties[domain_table_name]["object_properties"][range_table_name] = {}
            if column.get_constraint_name() not in self._classes_and_properties[domain_table_name]["object_properties"][range_table_name]:
                self._classes_and_properties[domain_table_name]["object_properties"][range_table_name][column.get_constraint_name()] = {}
            if column.get_column_name() not in self._classes_and_properties[domain_table_name]["object_properties"][range_table_name][column.get_constraint_name()]:
                self._classes_and_properties[domain_table_name]["object_properties"][range_table_name][column.get_constraint_name()][column.get_column_name()] = {"direct": {"name_property": name_property, "property": NewObjectProperty, "domain":DomainClass, "range": RangeClass,"functional_property": functional_property, "inverse_functional_property": inverse_functional_property}}
            else:
                self._classes_and_properties[domain_table_name]["object_properties"][range_table_name][column.get_constraint_name()][column.get_column_name()]["inverse"] = {"name_property": name_property, "property": NewObjectProperty, "domain":DomainClass, "range": RangeClass,"functional_property": functional_property, "inverse_functional_property": inverse_functional_property}
                    
        else:
            if range_table_name not in self._classes_and_properties[domain_table_name]["object_properties"]:
                self._classes_and_properties[domain_table_name]["object_properties"][range_table_name] = {}
            if bridge_table not in self._classes_and_properties[domain_table_name]["object_properties"][range_table_name]:
                self._classes_and_properties[domain_table_name]["object_properties"][range_table_name][bridge_table] = {"direct": {"name_property": name_property, "property": NewObjectProperty, "domain":DomainClass, "range": RangeClass,"functional_property": functional_property, "inverse_functional_property": inverse_functional_property}}
            else:
                self._classes_and_properties[domain_table_name]["object_properties"][range_table_name][bridge_table]["inverse"] = {"name_property": name_property, "property": NewObjectProperty, "domain":DomainClass, "range": RangeClass,"functional_property": functional_property, "inverse_functional_property": inverse_functional_property}

        return NewObjectProperty

    def create_2_inv_object_property(self, domain_table_name, range_table_name, DomainClass, RangeClass, column, many_to_many = False, bridge_table = None):

        """
            Create 2 inverse object property between a DomainClass and RangeClass.
            parameters:
                domain_table_name: domain class name
                range_table_name: range class name
                column_type: type of the column
                DomainClass: domain class object owlready2
                RangeClass: range class object owlready2
                column: column object
                many_to_many: flag to assess if the relation was many_to_many 
                bridge_table: flag to assess if the object property has been created from a bridge table
                
        """

        """Has a"""
        Restr = None
        HasAObjectProperty = None
        if column is not None:
            not_null = not column.is_nullable()
            unique = column.is_unique()
        else:
            not_null = False
            unique = False
        
        if (not many_to_many) and (not not_null) and (not unique):
            """
            1 to many and null and not unique
            When we talk about a 1 to many relationship the property must be functional because the domain
            can have only an instance of the range.
            """
            HasAObjectProperty = self.create_object_property(domain_table_name,
                range_table_name, DomainClass, RangeClass, "Func", column = column)
        
        elif (many_to_many) and (not not_null) and (not unique):
            """
            many to many and null and not unique.
            When we talk about a many to many relationship the property cannot be functional because
            each instance of the domain can be associated to many instance of the range and viceversa
            """
            HasAObjectProperty = self.create_object_property(domain_table_name,
                range_table_name, DomainClass, RangeClass, "Nothing", None, bridge_table, column = column)

        elif not_null and (not unique):
            """not null and not unique"""

            """The property must be functional with cardinality 1 on the property and the domain class"""
            HasAObjectProperty = self.create_object_property(domain_table_name,
                range_table_name, DomainClass, RangeClass, "Func", column = column)
            Restr = HasAObjectProperty.exactly(1, RangeClass)
        
        elif (not not_null) and unique:
            """null and unique"""

            """The property must be inverse functional"""
            HasAObjectProperty = self.create_object_property(domain_table_name,
                range_table_name, DomainClass, RangeClass, "FuncInv", column = column) # prima era solo inv ma non va bene
                
        elif not_null and unique:
            """not null and unique"""

            """The property must be functional and inverse functional and with cardinality 1 on the property and the domain class"""
            HasAObjectProperty = self.create_object_property(domain_table_name,
                range_table_name, DomainClass, RangeClass, "FuncInv", column = column)
            Restr = HasAObjectProperty.exactly(1, RangeClass)

        """Is a"""
        IsAObjectProperty = None
        IsAObjectProperty = self.create_object_property(range_table_name,
            domain_table_name, RangeClass, DomainClass, "Inverse", str(HasAObjectProperty).split(".")[1], bridge_table, column = column)

        """To create a second property that is inverse of the other"""
        IsAObjectProperty.inverse_property = HasAObjectProperty
        
        
        return HasAObjectProperty, IsAObjectProperty, Restr
    

    def add_data_properties_to_class(self, table: Table, DomainClass):
        """
            This method adds data properties to a given class
            parameters: 
                table: table_object
                DomainClass: domain class object owlready2
        """
        for column_name, column in table.get_columns().items():
            """If the column is not FK""" 

            if not(column.is_pk() is True and "id" in str.lower(column_name)):
                if column.is_fk() is False:
                    NewProperty, Restr = self.create_data_property(table.get_table_name(), column_name, column.get_type(), DomainClass, not column.is_nullable())
                    self._classes_and_properties[table.get_table_name()]["data_properties_restr"].append(Restr)
        
    def add_1_to_many_object_properties_to_class(self, column: Column, table: Table, range_table_name, DomainClass, RangeClass = None):
        """
            This method adds two mutually inverse object properties starting from a 1 to many relationship
            between two class
            parameters: 
                column: a column object referring to the column which will generate the 1_to_many_relationship
                table: table_object from which the 1_to_many_relationship is generated
                range_table_name: name of the range class
                DomainClass: domain class object owlready2
                RangeClass: range class object owlready2
        """
        """If the column is FK"""
        if column.is_fk():
            if (range_table_name is not None) and (RangeClass is not None):
                if column.is_pk() and (len(table.get_pk_columns().keys()) == 1):
                    column.set_nullable(False)
                    column.set_unique(True)

                if (table.get_table_name() + "_" + range_table_name) not in self._created_classes:
                    """Creates 2 object properties which are the one the inverse of the other"""
                    
                    HasAObjectProperty, IsAObjectProperty, Restr = self.create_2_inv_object_property(table.get_table_name(), 
                        range_table_name, DomainClass, RangeClass, column, False)

                    """
                        Adds the restriction
                    """
                    if Restr is not None:
                        self._classes_and_properties[table.get_table_name()]["object_properties_restr"].append(Restr)

    
    def add_many_to_many_object_properties_to_class(self, table, range_table_name, DomainClass, RangeClass = None, bridge_table = None):
        """
            Given a table, the name of the range table a domain and range class it create 2 object properties starting
            from many to many relation.
            parameters: 
                table: table_object from which the many_to_many_relationship is generated
                range_table_name: name of the range class
                DomainClass: domain class object owlready2
                RangeClass: range class object owlready2
                bridge_table: bridge_table_name
        """
        """Creates 2 object properties which are the one the inverse of the other"""
        
        HasAObjectProperty, IsAObjectProperty, _ = self.create_2_inv_object_property(table.get_table_name(), 
            range_table_name, DomainClass, RangeClass, None, True, bridge_table)

        self._table_converted_in_properties[table.get_table_name()] = {"direct": HasAObjectProperty, "inverse": IsAObjectProperty}           


    def add_restriction_to_class(self, class_object, data_properties_restr, object_properties_restr):
        """
        add restrictions to a class.
        parameters: 
                class_object: class object (owlready2) on which the restrictions are defined
                data_properties_restr: data property restrictions
                object_properties_restr: object property restrictions
        """
        with self._onto:
            class_object.is_a.append(And(data_properties_restr + object_properties_restr))

    def create_instance(self, class_name, instance_name):
        """
        create an instance of a class.
        parameters: 
                class_name: name of the class of the instance to create
                instance_name: name of the instance to create
        """
        instance = self.get_created_classes()[class_name](instance_name, namespace = self._onto)
        self._created_instances[instance_name] = {"object": instance}
        return instance

    def create_data_property_instance(self, instance, type_col, data_property_name, instance_name, column_name, value_to_insert):
        """
        create an instance of a data property given an instance of a class.
        parameters: 
                instance: instance of the 
                type_col:
                data_property_name: 
                instance_name: 
                column_name:
                value_to_insert:
        """
        value_string, value = self._parse_value(type_col, value_to_insert)
        string_to_execute = "instance." + data_property_name + value_string
        exec(string_to_execute)
        self._created_instances[instance_name][column_name] = value_to_insert

    def _parse_value(self, type_col, value):
        if type_col in NUMERIC_TYPE_LIST:
            return " = " + value, value
        elif type_col in BOOLEAN_TYPE_LIST:
            if value in FALSE_VALUE_LIST: 
                value = "False"
            elif value in TRUE_VALUE_LIST:
                value = "True" 
            return " = bool(" + value + ")", value
        elif type_col in STRING_TYPE_LIST:
            value = value.replace("\\", "")
            return """ = value""", value
        elif type_col in TIME_TYPE_LIST:
            value = parser.parse(value).date()
            return " = datetime.date(int(value.year), int(value.month), int(value.day))", value
        elif type_col in [datetime.time]:
            value = parser.parse(value).time()
            return " = datetime.time(int(value.hour), int(value.minute), int(value.second))", value
        elif type_col in [datetime.datetime]:
            value = parser.parse(value)
            return " = datetime.datetime(int(value.year), int(value.month), int(value.day), int(value.hour), int(value.minute), int(value.second))", value

    def create_object_property_instance(self, domain_instance, range_instance, direct_property):
        """
        create an instance of an object_property given an instance of a class.
        parameters: 
                domain_instance: domain instance of the object property instance
                range_instance: range instance of the object property instance
                direct_property: object property to instantiate (owlready2)
        """
        if direct_property["functional_property"]:
            direct_string_execute = "domain_instance." + direct_property["property"].__name__ + " = range_instance"
        else:
            direct_string_execute = "domain_instance." + direct_property["property"].__name__ + ".append(range_instance)" 
        
        exec(direct_string_execute)

    def get_instance_object_by_name(self, name_instance):
        return self._created_instances[name_instance]["object"]

# def get_string_instance_to_append(dict):
#     string_instance_to_append = ""
#     for pk_column, pk_value in zip(dict.keys(), dict.values()):
#         string_instance_to_append = string_instance_to_append + STRING_INSTANCE_SEPARATOR + str(pk_column) \
#             + STRING_INSTANCE_SEPARATOR + str(pk_value)
#     return string_instance_to_append