from models import Package, PackageModelForm

from django.contrib import admin

class PackageAdmin(admin.ModelAdmin):
    form = PackageModelForm
    list_display = ('__unicode__', 'commit', 'date', 'url')

admin.site.register(Package, PackageAdmin)
