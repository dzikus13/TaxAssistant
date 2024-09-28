from django.test import TestCase

# Create your tests here.


class TestXmlValidator(TestCase):

    def setUp(self):
        with open("../../examples/pcc_example.xml") as f:
            content = f.read()
            self.document = content

        with open("../../examples/pcc_example_invalid.xml") as f:
            content = f.read()
            self.document_invalid = content

        with open("../../examples/pcc-3.xsd") as f:
            content = f.read()
            self.schema = content

    def test_validator_silent(self):
        from .utils import validate
        self.assertTrue(validate(self.document, self.schema))


    def test_validator_fail_silent(self):
        from .utils import validate
        self.assertFalse(validate(self.document_invalid, self.schema))


    def test_validator_fail_silent(self):
        from .utils import validate
        import lxml
        with self.assertRaises(lxml.etree.DocumentInvalid):
            validate(self.document_invalid, self.schema, silent=False)
