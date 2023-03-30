from django.db import models


class TrackChangesModel(models.Model):
    """:class:`~django.models.Model` mixin that keeps a copy of initial
    data in order to check if fields have been changed. Change detection
    only works on the current instance of an object."""

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial = self.__dict__.copy()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__initial = self.__dict__.copy()

    def has_changed(self, field):
        return getattr(self, field) != self.__initial[field]

    def initial_value(self, field):
        return self.__initial[field]
