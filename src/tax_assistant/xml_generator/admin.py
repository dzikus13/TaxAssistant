from django.contrib import admin
from django import forms
# Register your models here.

from .models import TaxForm, TaxFormValidation, TaxFormInstance, ContextDocument


admin.site.register(TaxForm)
admin.site.register(TaxFormValidation)
admin.site.register(TaxFormInstance)
admin.site.register(ContextDocument)