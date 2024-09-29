from lxml import etree
from io import BytesIO
from django.template import Template, Context


def validate(xml: str, xsd: str, silent: bool = True) -> bool:
    doc = etree.parse(BytesIO(bytes(xml, encoding="UTF-8")))
    schema_doc = etree.parse(BytesIO(bytes(xsd, encoding="UTF-8")))
    schema = etree.XMLSchema(schema_doc)
    if silent:
        return schema.validate(doc)
    else:
        return schema.assertValid(doc)


def generate_xml(template, context: dict):
    xml_template = Template(template)
    ctx = Context(context)
    xml = xml_template.render(ctx)

    return xml



