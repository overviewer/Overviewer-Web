from models import Page, License, File
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

class PageAdmin(MPTTModelAdmin):
    fields = Page.userfields
    list_display = ('title', 'subtitle', 'url')

class FileAdmin(admin.ModelAdmin):
    fields = File.userfields
    list_display = ('name', 'parent', 'size', 'md5')

admin.site.register(Page, PageAdmin)
admin.site.register(License)
admin.site.register(File, FileAdmin)
