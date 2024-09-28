from django.db import models
from django.utils.translation import gettext as _

from assistant.models import Interaction
from .utils import validate


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

    def __str__(self):
        return self.name

    @property
    def schema(self):
        schema_object = self.taxformvalidation_set.filter(
            valid_till__isnull=True).first()
        if not schema_object:
            raise ValueError(_("Tax form is missing current schema"))


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

    valid_till = models.DateField(null=True)

    def __str__(self):
        return f"{self.tax_form.name}-{self.valid_till}"


class TaxFormInstance(models.Model):
    tax_form = models.ForeignKey(TaxForm, on_delete=models.SET_NULL, null=True)
    user_designation = models.CharField(max_length=20, null=True)
    user_id = models.UUIDField(null=True)
    data = models.JSONField()
    xml = models.TextField()
    status = models.CharField(
        max_length=20, choices=[(i[0], i[1]) for i in TAX_FORM_STATUS])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_interaction = models.ForeignKey(
        Interaction, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tax_form.name}-{self.valid_till}"

    def validate(self):
        if not self.xml:
            raise ValueError("XML not created")

        return validate(self.xml, self.tax_form.schema)
