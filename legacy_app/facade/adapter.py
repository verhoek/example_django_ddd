from legacy_app.facade.dtos import LegacyEntityDTO
from legacy_app.models import LegacyEntity


def create_legacy_entity(legacy_dto: LegacyEntityDTO):
    LegacyEntity.objects.create(legacy_name=legacy_dto.name, serial_number=legacy_dto.serial)


def delete_legacy_entity_by_name(name):
    LegacyEntity.objects.get(legacy_name=name).delete()


def update_legacy_entity_by_name(name, legacy_dto: LegacyEntityDTO):
    legacy = LegacyEntity.objects.get(legacy_name=name)
    legacy.legacy_name = legacy_dto.name
    legacy.serial_number = legacy_dto.serial
    legacy.save()
