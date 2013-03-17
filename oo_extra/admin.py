from models import Package, PackageModelForm, Build, BuildModelForm

from django.contrib import admin

class PackageAdmin(admin.ModelAdmin):
    form = PackageModelForm
    list_display = ('__unicode__', 'checkout', 'commit', 'date', 'url')

class BuildAdmin(admin.ModelAdmin):
    form = BuildModelForm
    list_display = ('__unicode__', 'branch', 'commit', 'date', 'path', 'downloads')

admin.site.register(Package, PackageAdmin)
admin.site.register(Build, BuildAdmin)
