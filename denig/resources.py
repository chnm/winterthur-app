from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Document, Fragment


class DocumentResource(resources.ModelResource):
    class Meta:
        model = Document
        exclude = (
            "created",
            "last_modified",
        )


class FragmentResource(resources.ModelResource):
    document = fields.Field(
        column_name="item_image_name",
        attribute="item_image_name",
        widget=ForeignKeyWidget(Document, "item_image_name"),
    )

    class Meta:
        model = Fragment
