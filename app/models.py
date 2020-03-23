from django.db import models

from app.repositories import RootEntityRepository
from ddd import DDDModel, DDDManager


class RootEntityManager(DDDManager):
    pass


class RootEntity(DDDModel):
    name = models.CharField(max_length=128)

    repository = RootEntityRepository  # have to set it as class attribute, no control when model gets instantiated
    objects = RootEntityManager()
