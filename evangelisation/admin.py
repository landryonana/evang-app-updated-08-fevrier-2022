from django.contrib import admin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from evangelisation.models import Evangelisation,  Person, Site, Suivi, Image, Participant, Profile


class Userresource(resources.ModelResource):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 
				'date_joined', 'is_active', 'is_staff', 
				'is_superuser', 'last_login', 'password')

class UserAdmin(ImportExportModelAdmin):
	list_display = ('id', 'username', 'first_name', 'email')
	resource_class = Userresource

class SiteAdmin(ImportExportModelAdmin):
	pass

class ParticipantAdmin(ImportExportModelAdmin):
	pass


class PersonAdmin(ImportExportModelAdmin):
	pass


class EvangelisationAdmin(ImportExportModelAdmin):
	pass


class SuiviAdmin(ImportExportModelAdmin):
	pass


class ProfileAdmin(ImportExportModelAdmin):
	pass


class ImageAdmin(ImportExportModelAdmin):
	pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Evangelisation, EvangelisationAdmin)
admin.site.register(Suivi, SuiviAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)





