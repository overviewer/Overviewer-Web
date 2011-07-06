from models import Page, License
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

class PageAdmin(MPTTModelAdmin):
    fields = Page.userfields
    list_display = ('title', 'subtitle', 'url')

admin.site.register(Page, PageAdmin)
admin.site.register(License)
