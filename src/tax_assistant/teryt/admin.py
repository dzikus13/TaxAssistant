
from django.contrib import admin

# Register your models here.

from .models import RodzajMiejscowosci, Miejscowosc, JednostkaAdministracyjna, Ulica


class MiejscowoscAdmin(admin.ModelAdmin):
    list_display = ["__str__", "rodzaj_miejscowosci"]


class JednostkaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "typ"]


admin.site.register(RodzajMiejscowosci)
admin.site.register(Miejscowosc, MiejscowoscAdmin)
admin.site.register(JednostkaAdministracyjna, JednostkaAdmin)
admin.site.register(Ulica)

