# Test cases can be run with either of the following:
# python -m unittest discover
# nosetests -v --rednose --nologcapture
# nosetests --verbosity 2 --with-spec --spec-color
# To check coverage:
# coverage run --omit "venv/*" test_wishlists.py
# coverage report -m --include= wishlists.py

import json
import unittest
import logging
import wishlists
from persistence import db, DatabaseEngine
from flask_api import status


class WishlistTestCase(unittest.TestCase):
    def setUp(self):
        wishlists.db.create_wishlist('wl1', 'user1')
        wishlists.db.add_item(1, {'id': 'item1', 'description': 'test item 1'})
        self.db = wishlists.db
        self.app = wishlists.app.test_client()

    def tearDown(self):
        wishlists.db = DatabaseEngine()

    """
        This is a test case to check whether a wishlist is created or not.
        POST verb checked here.
    """

    def test_create_wishlist(self):
        new_wishlist = {'name': 'xynazog', 'user_id': '123'}
        data = json.dumps(new_wishlist)
        resp = self.app.post('/wishlists', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'xynazog')
        respTwo = self.app.get('/wishlists')
        all_wishlists_json = json.loads(respTwo.data)
        self.assertEqual(len(all_wishlists_json), 2)

    """
        This is a test case to check whether an item is added to a wishlist or not.
        POST verb is checked here.
    """

    def test_create_wishlist_item(self):
        new_item = {'id': 'item3', 'description': 'test item 3'}
        data = json.dumps(new_item)
        resp = self.app.post('/wishlists/1/items', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['id'], 'item3')
        # Checking number of items - 2 items 'cause one is created.
        respTwo = self.app.get('/wishlists/1/items')
        dataTwo = json.loads(respTwo.data)
        self.assertEqual(len(dataTwo['1']), 2)

    """
        This is a test case to check whether an item is added to a wishlist out of index.
        POST verb is checked here.
    """

    def test_create_wishlist_item_wishlist_not_found(self):
        new_item = {'id': 'item3', 'description': 'test item 3'}
        data = json.dumps(new_item)
        resp = self.app.post('/wishlists/3/items', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether a wishlist is updated.
        PUT verb checked here.
    """

    def test_update_wishlist(self):
        new_wl = {'name': 'wl2', 'user_id': 'user2'}
        data = json.dumps(new_wl)
        resp = self.app.put('/wishlists/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'wl2')
        self.assertEqual(new_json['user_id'], 'user2')

    """
        This is a test case to check whether an error is returned when no data is sent for a wishlist.
        PUT verb checked here.
    """

    def test_update_wishlist_with_no_data(self):
        resp = self.app.put('/wishlists/1', data=None, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether an error is returned when the incorrect data format is sent for a wishlist.
        PUT verb checked here.
    """

    def test_update_wishlist_with_text_data(self):
        resp = self.app.put('/wishlists/1', data="hello", content_type='text/plain')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether an error is returned when the insufficient data is sent for a wishlist.
        PUT verb checked here.
    """

    def test_update_wishlist_with_no_name(self):
        new_wl = {'user_id': 'user2'}
        data = json.dumps(new_wl)
        resp = self.app.put('/wishlists/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether an error is returned when the insufficient data is sent for a wishlist.
        PUT verb checked here.
    """

    def test_update_wishlist_with_no_user_ID(self):
        new_wl = {'name': 'wl2'}
        data = json.dumps(new_wl)
        resp = self.app.put('/wishlists/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether an error is returned when a nonexistent wishlist is updated.
        PUT verb checked here.
    """

    def test_update_wishlist_not_found(self):
        new_wl = {'name': 'wl2', 'user_id': 'user2'}
        data = json.dumps(new_wl)
        resp = self.app.put('/wishlists/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    """
        This is a test case to check whether an item is updated.
        PUT verb checked here.
    """

    def test_update_item(self):
        new_item = {'description': 'test update'}
        data = json.dumps(new_item)
        resp = self.app.put('/wishlists/1/items/item1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['items']['item1']['description'], 'test update')

    """
        This is a test case to check whether an error is returned when empty data is sent for an item.
        PUT verb checked here.
    """

    def test_update_item_with_no_data(self):
        resp = self.app.put('/wishlists/1/items/item1', data=None, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether an error is returned when the incorrect data format is sent for an item.
        PUT verb checked here.
    """

    def test_update_item_with_text_data(self):
        resp = self.app.put('/wishlists/1/items/item1', data="hello", content_type='text/plain')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether an error is returned when the insufficient data is sent for an item.
        PUT verb checked here.
    """

    def test_update_item_with_no_description(self):
        new_item = {'id': 'item1'}
        data = json.dumps(new_item)
        resp = self.app.put('/wishlists/1/items/item1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    """
        This is a test case to check whether an error is returned when a nonexistent item is updated.
        PUT verb checked here.
    """

    def test_update_item_not_found(self):
        new_item = {'description': 'test update'}
        data = json.dumps(new_item)
        resp = self.app.put('/wishlists/1/items/item2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    """
        This is a test case to check whether an error is returned when an item in a nonexistent wishlist is updated.
        PUT verb checked here.
    """

    def test_update_item_wishlist_not_found(self):
        new_item = {'description': 'test update'}
        data = json.dumps(new_item)
        resp = self.app.put('/wishlists/2/items/item1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    """
        This is a test case to check whether a wishlist is cleared.
        PUT verb checked here.
    """

    def test_clear_wishlist(self):
        resp = self.app.put('/wishlists/1/items/clear', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(len(new_json['items']), 0)

    """
        This is a test case to check whether an error is returned when a nonexistent wishlist is cleared.
        PUT verb checked here.
    """

    def test_clear_wishlist_not_found(self):
        resp = self.app.put('/wishlists/2/items/clear', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    """
        This is a test case to check whether a wishlist is deleted.
        DELETE verb checked here.
    """

    def test_delete_wishlist(self):
        resp = self.app.delete('/wishlists/1', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        respTwo = self.app.get('/wishlists')
        all_wishlists_json = json.loads(respTwo.data)
        self.assertEqual(len(all_wishlists_json), 0)

    """
        This is a test case to check whether a message is response when a nonexistent wishlist is deleted
        DELETE verb checked here.
    """

    def test_delete_wishlist_nonexist(self):
        resp = self.app.delete('/wishlists/5', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        respTwo = self.app.get('/wishlists')
        all_wishlists_json = json.loads(respTwo.data)
        self.assertEqual(len(all_wishlists_json), 1)


if __name__ == '__main__':
    unittest.main()
