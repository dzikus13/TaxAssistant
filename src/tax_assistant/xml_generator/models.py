from django.db import models
from django.utils.translation import gettext as _

from assistant.models import Session
from .utils import validate, generate_xml
from assistant.utils import get_us_code


# Create your models here.

TAX_FORM_STATUS = {
    "new": _("New"),
    "validated": _("Validated"),
    "posted": _("Posted"),
}


class TaxForm(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    metadata = models.JSONField()
    system_prompt = models.TextField(null=True)
    xml_template = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property
    def schema(self):
        schema_object = self.taxformvalidation_set.filter(
            valid_till__isnull=True).first()
        if not schema_object:
            raise ValueError(_("Tax form is missing current schema"))
        return schema_object

    def is_ready(self, item_list):
        item_dict = item_list
        # print("ITEMs", item_list)
        # for item in item_list:
        #    print("ITEM", item)
        #    for k, v in item.items():
        #        item_dict[k] = v
        for item, data in self.metadata.items():
            if data.get("required", True) and not data.get("calculated", False):
                if not item in item_dict:
                    print("MISSING", item)
                    return False
        return True
    
    def get_missing_fields(self, item_list):
        response = []

        item_dict = item_list
        # print("ITEMs", item_list)
        # for item in item_list:
        #    print("ITEM", item)
        #    for k, v in item.items():
        #        item_dict[k] = v
        for item, data in self.metadata.items():
            if data.get("required", True) and not data.get("calculated", False):
                if not item in item_dict:
                    response.append(item)
        return response

    def create_document(self, session):
        data = session.collect_knowledge()
        data = self.calculate_fields(data)
        doc = TaxFormInstance(
            tax_form=self,
            user_designation=session.user_id,
            user_id=session.user_id,
            data=data,
            source=session
        )
        doc.save()
        doc.xml = doc.generate_xml(data)
        print("XML", doc.xml)
        doc.save()
        if doc.validate():
            doc.status = "validated"
            doc.save()
    
    def calculate_fields(self, values):
        for item, value in self.metadata.items():
            calculation = value.get("calculated", False)
            if calculation:
                values[item] = self.calculate_field(value, values)
        return values
    
    def calculate_field(self, calculation, values):
        calculation_type = calculation.get("type", "multiplicative")
        if calculation_type == "additive":
            total = 0
            for variable_name in calculation["variables"]:
                total += values[variable_name]
            return total
        elif calculation_type == "e-pity":
            return get_us_code(values["P19"])
        else:
            return round(float(values[calculation["variable"]]) * calculation["factor"])
    

class TaxFormInstance(models.Model):
    xml = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=[(name, descr) for name, descr in TAX_FORM_STATUS.items()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True)


class ContextDocument(models.Model):
    tax_form = models.ForeignKey(TaxForm, on_delete=models.CASCADE)
    content = models.TextField()
    valid_till = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tax_form.name}-{self.valid_till}"


class TaxFormValidation(models.Model):
    tax_form = models.ForeignKey(TaxForm, on_delete=models.SET_NULL, null=True)
    xsd = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    valid_till = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tax_form.name}-{self.valid_till}"


class TaxFormInstance(models.Model):
    tax_form = models.ForeignKey(TaxForm, on_delete=models.SET_NULL, null=True)
    user_designation = models.CharField(max_length=100, null=True)
    user_id = models.UUIDField(null=True)
    data = models.JSONField(null=True, blank=True)
    xml = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default="new",
        choices=[(name, descr) for name, descr in TAX_FORM_STATUS.items()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tax_form.name}"

    def validate(self):
        if not self.xml:
            raise ValueError("XML not created")
        return validate(self.xml, self.tax_form.schema.xsd)

    def generate_xml(self, data):
        template_str = self.tax_form.xml_template
        xml = generate_xml(template_str, data)
        return xml