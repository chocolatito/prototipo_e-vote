from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportMixin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#
from .models import Elector, Padron, PadronElector, Person, Group, Membership

# Register your models here.


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin, ExportMixin, UserAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'date_joined', )
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# _Elector
class ElectorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'dni', 'names', 'surnames', 'user')


admin.site.register(Elector, ElectorAdmin)


# _Padron
class PadronAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'date')
    fields = ('title', 'date')


admin.site.register(Padron, PadronAdmin)


# _Padron
class PadronElectorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'elector', 'padron')


admin.site.register(PadronElector, PadronElectorAdmin)

admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Membership)
