from django.contrib import admin

from denig.admin import FragmentAdmin

from .models import Footnote


class FootnoteAdmin(admin.ModelAdmin):
    list_display = ("source", "footnote_type", "last_modified")


class FootnoteInline(admin.TabularInline):
    model = Footnote
    fields = ("content", "footnote_type", "notes")
    extra = 0


admin.site.register(Footnote, FootnoteAdmin)

FragmentAdmin.inlines = [FootnoteInline]
