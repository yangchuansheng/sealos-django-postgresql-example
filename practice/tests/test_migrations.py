from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.test import TestCase

from practice.models import Item


class MigrationContractTests(TestCase):
    def test_initial_migration_is_applied_and_matches_item_schema(self):
        loader = MigrationLoader(connection)
        self.assertIn(('practice', '0001_initial'), loader.graph.nodes)
        self.assertIn(('practice', '0001_initial'), loader.graph.leaf_nodes())
        self.assertIn(Item._meta.db_table, connection.introspection.table_names())
        self.assertEqual(
            [field.name for field in Item._meta.local_fields],
            ['id', 'name', 'created_at'],
        )
        self.assertEqual(Item._meta.get_field('name').max_length, 200)
        self.assertTrue(Item._meta.get_field('created_at').auto_now_add)
