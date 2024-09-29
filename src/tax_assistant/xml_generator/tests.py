from django.test import TestCase
from .models import TaxForm

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


    def test_validator_fail_loud(self):
        from .utils import validate
        import lxml
        with self.assertRaises(lxml.etree.DocumentInvalid):
            validate(self.document_invalid, self.schema, silent=False)



class TestXmlGenerator(TestCase):

    def setUp(self):
        self.document = """
         <Naglowek>
            <KodFormularza kodSystemowy="PCC-3 (6)" kodPodatku="PCC" rodzajZobowiazania="Z" wersjaSchemy="1-0E">PCC-3</KodFormularza>
            <WariantFormularza>6</WariantFormularza>
            <CelZlozenia poz="P_6">1</CelZlozenia>
            <Data poz="P_4">2024-07-29</Data>
            <KodUrzedu>{{KodUrzedu}}</KodUrzedu>
        </Naglowek>
        <Podmiot1 rola="Podatnik">
            {%if PESEL%}
            <OsobaFizyczna>
                <PESEL>{{PESEL}}</PESEL>
                <ImiePierwsze>{{ImiePierwsze}}</ImiePierwsze>
                <Nazwisko>{{Nazwisko}}</Nazwisko>
                <DataUrodzenia>{{DateUrodzenia}}</DataUrodzenia>
            </OsobaFizyczna>
            {%else%}
            {%endif%}
            <AdresZamieszkaniaSiedziby rodzajAdresu="RAD">
                <AdresPol>
                    <KodKraju>{{KodKraju}}</KodKraju>
                    <Wojewodztwo>{{Wojewodztwo}}</Wojewodztwo>
                    <Powiat>{{Powiat}}</Powiat>
                    <Gmina>{{Gmina}}</Gmina>
                    <Ulica>{{Ulica}}</Ulica>
                    <NrDomu>{{NrDomu}}</NrDomu>
                    <NrLokalu>{{NrLokalu}}</NrLokalu>
                    <Miejscowosc>{{Miejscowosc}}</Miejscowosc>
                    <KodPocztowy>{{KodPocztowy}}</KodPocztowy>
                </AdresPol>
            </AdresZamieszkaniaSiedziby>
        </Podmiot1>
        """
        self.context = {
            "PESEL": "1234123455",
            "Nazwisko": "Testowe"
        }


    def test_generator(self):
        from .utils import generate_xml
        result = generate_xml(self.document, self.context)
        self.assertTrue("<PESEL>1234123455</PESEL>" in result)
        self.assertTrue("<Nazwisko>Testowe</Nazwisko>" in result)
        self.assertTrue("<Gmina></Gmina>" in result)


class TestXmlCalculator(TestCase):
    fixtures = ["sample"]

    def test_generator(self):
        tax_form = TaxForm.objects.get(name="PCC-3")
        values = tax_form.calculate_fields({"P26": 1240})
        print(values)
        self.assertTrue("P27" in values)
        self.assertEqual(values["P27"], 25)
        self.assertEqual(values["P46"], 25)

