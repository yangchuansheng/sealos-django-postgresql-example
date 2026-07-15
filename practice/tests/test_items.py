import json

from django.test import TestCase

from practice.models import Item


class ItemApiTests(TestCase):
    def test_create_and_read_return_the_same_item_identity(self):
        create_response = self.client.post(
            '/items/',
            data=json.dumps({'name': 'synthetic-item'}),
            content_type='application/json',
        )

        self.assertEqual(create_response.status_code, 201)
        created = create_response.json()
        item_id = created['id']
        self.assertEqual(created['name'], 'synthetic-item')

        read_response = self.client.get(f'/items/{item_id}/')

        self.assertEqual(read_response.status_code, 200)
        self.assertEqual(read_response.json()['id'], item_id)
        self.assertEqual(read_response.json()['name'], 'synthetic-item')
        self.assertEqual(Item.objects.get(pk=item_id).name, 'synthetic-item')

    def test_invalid_json_and_missing_name_are_rejected(self):
        invalid_json = self.client.post(
            '/items/',
            data='{',
            content_type='application/json',
        )
        missing_name = self.client.post(
            '/items/',
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(invalid_json.status_code, 400)
        self.assertEqual(missing_name.status_code, 400)
