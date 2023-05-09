from owlready2 import *
import decimal
import json

class Decimal(object):
    def __init__(self, value):
        self.value = value
    
    def parser(s):
        return Decimal(decimal.Decimal(s))

    def unparser(x):
        return json.dumps(x)

declare_datatype(Decimal, "http://www.w3.org/2001/XMLSchema#decimal", Decimal.parser, Decimal.unparser)

class Long(object):
    def __init__(self, value):
        self.value = value
    
    def parser(s):
        return Long(int(s,64))

    def unparser(x):
        return json.dumps(x)

declare_datatype(Long, "http://www.w3.org/2001/XMLSchema#long", Long.parser, Long.unparser)
