from django.contrib import admin

from .models import Footnote


class FootnoteAdmin(admin.ModelAdmin):
    list_display = ("source", "footnote_type", "last_modified")


admin.site.register(Footnote, FootnoteAdmin)
