from django.db import transaction

from ddd import repository, DDDRepository

from legacy_app.facade import dtos, adapter


@repository
class RootEntityRepository(DDDRepository):
    """
    The repository is a central place to write to the database.
    Some ACL logic can be performed here.
    """

    @transaction.atomic
    def bulk_create(self, objs):
        self.model.objects.bulk_create(objs)

    def get_by_id(self, id):
        aggr = self.model.objects.get(id=id)
        return aggr

    @transaction.atomic
    def create(self, obj):
        obj.save()
        legacy_dto = dtos.LegacyEntityDTO(obj.name[:64], obj.name[64:] + '_serial')

        # instead of a direct call, think about decoupling this using a pub/sub system
        adapter.create_legacy_entity(legacy_dto)

    @transaction.atomic
    def delete(self, obj):
        adapter.delete_legacy_entity_by_name(obj.name)
        obj.delete()

    @transaction.atomic
    def update(self, obj):
        prev_obj = self.get_by_id(obj.id)
        obj.save()

        legacy_dto = dtos.LegacyEntityDTO(obj.name[:64], obj.name[64:] + '_serial')

        # instead of a direct call, think about decoupling this using a pub/sub system
        adapter.update_legacy_entity_by_name(prev_obj.name, legacy_dto)
