from lxml import etree
from io import BytesIO


def validate(xml: str, xsd: str, silent: bool = True) -> bool:
    doc = etree.parse(BytesIO(bytes(xml, encoding="UTF-8")))
    schema_doc = etree.parse(BytesIO(bytes(xsd, encoding="UTF-8")))
    schema = etree.XMLSchema(schema_doc)
    if silent:
        return schema.validate(doc)
    else:
        return schema.assertValid(doc)
