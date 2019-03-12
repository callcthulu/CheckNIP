import xmlschema as x
schema = x.XMLSchema('XSDSchemaNIP.xsd')
print(schema.is_valid('XMLschemaQuestion.xml'))