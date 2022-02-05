from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from evangelisation.models import Evangelisation,  Person, Site, Suivi, Image, Participant, Profile




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

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Evangelisation, EvangelisationAdmin)
admin.site.register(Suivi, SuiviAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)




