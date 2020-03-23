from django.db import models


class LegacyEntity(models.Model):
    """
    Since this is an entity of a legacy application, we do not create a fancy repository
    and do not do DDD.
    """

    serial_number = models.TextField()
    legacy_name = models.CharField(max_length=64)