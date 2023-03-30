from django.contrib import admin

from .models import Collection, Document, Fragment, Language

admin.site.register(Collection)
admin.site.register(Language)
admin.site.register(Document)

## Add to the Fragment view a way to see:
## 1. the document that the fragment is from
## 2. the translation of the fragment


class FragmentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "line_number", "document", "last_modified")
    list_filter = ("document", "languages")
    search_fields = ("transcription", "notes")


admin.site.register(Fragment, FragmentAdmin)
