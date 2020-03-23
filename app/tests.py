from django.test import TestCase

from rest_framework.test import APITestCase

from app.models import RootEntity
from legacy_app.models import LegacyEntity


def create_root_entity():
    root_entity = RootEntity(name='my_name')
    RootEntity.get_repository().create(root_entity)
    return root_entity


class DjangoVanillaTests(TestCase):
    """
    Test the repository without calling views.
    """

    def test_create_root_entity(self):
        create_root_entity()
        self.assertEqual(RootEntity.objects.count(), 1)
        self.assertEqual(LegacyEntity.objects.count(), 1)

    def test_bulk_create_root_entity(self):
        roots = [RootEntity(name='one'), RootEntity(name='two')]
        RootEntity.get_manager().bulk_create(roots)
        self.assertEqual(RootEntity.objects.count(), 2)

    def test_delete_root_entity(self):
        root = create_root_entity()
        RootEntity.get_repository().delete(root)
        self.assertEqual(RootEntity.objects.count(), 0)
        self.assertEqual(LegacyEntity.objects.count(), 0)


class DjangoAPITests(APITestCase):
    """
    Test the repository with calling views.
    """

    def test_create_root_entity(self):
        r = self.client.post('/root_entity/', format='json', data={'name': 'fancy_name'})
        self.assertEqual(RootEntity.objects.count(), 1)
        self.assertEqual(LegacyEntity.objects.count(), 1)

    def test_update_root_entity(self):
        root = create_root_entity()
        new_name = 'fancy_name'
        self.client.patch(f'/root_entity/{root.id}', format='json', data={'name': new_name})
        self.assertEqual(RootEntity.objects.count(), 1)
        self.assertEqual(RootEntity.objects.first().name, new_name)
        self.assertEqual(LegacyEntity.objects.first().legacy_name, new_name)
