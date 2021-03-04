from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Urna, Voto
# Register your models here.


class VotoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'candidato', 'urna')
    fields = ['candidato', 'urna']


admin.site.register(Voto, VotoAdmin)


class UrnaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'eleccion', 'urna_status')
    fields = ['eleccion', 'urna_status']


admin.site.register(Urna, UrnaAdmin)
