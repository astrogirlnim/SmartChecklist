import unittest
import json
import tempfile
import os
import sys
sys.path.append('..')  # Add parent directory to path
from app import create_app, init_db


class APITestCase(unittest.TestCase):
    """
    Comprehensive test suite for the Smart Checklist API
    
    This test class demonstrates proper API testing patterns:
    - Setup/teardown of test database
    - Authentication testing
    - CRUD operations testing
    - Input validation testing
    - Error handling testing
    - Hierarchical data structure testing
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Create app with test configuration
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
            'SECRET_KEY': 'test-secret-key',
            'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
        })
        
        # Initialize the test database
        with self.app.app_context():
            init_db(app_instance=self.app, db_path=self.db_path)
        
        # Create test client
        self.client = self.app.test_client()
        
        # Create test user and login
        self.test_user = self._create_and_login_user()

    def tearDown(self):
        """Clean up after each test method."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _create_and_login_user(self):
        """Helper method to create and login a test user"""
        # Register test user
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Login test user
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        return {'username': 'testuser', 'password': 'testpass123'}

    def _api_request(self, method, url, data=None, expected_status=200):
        """Helper method for making API requests"""
        if method.upper() == 'GET':
            response = self.client.get(url)
        elif method.upper() == 'POST':
            response = self.client.post(url, 
                                      data=json.dumps(data) if data is not None else json.dumps({}),
                                      content_type='application/json')
        elif method.upper() == 'PUT':
            response = self.client.put(url,
                                     data=json.dumps(data) if data is not None else json.dumps({}),
                                     content_type='application/json')
        elif method.upper() == 'DELETE':
            response = self.client.delete(url)
        
        self.assertEqual(response.status_code, expected_status)
        
        # Handle JSON response parsing
        if response.data:
            try:
                return json.loads(response.data)
            except json.JSONDecodeError:
                # If response isn't JSON, return as string
                return {'response': response.data.decode('utf-8')}
        return {}

    # ========================================
    # AUTHENTICATION TESTS
    # ========================================

    def test_api_requires_authentication(self):
        """Test that API endpoints require authentication"""
        # Logout current user
        self.client.get('/logout')
        
        # Test various endpoints without authentication
        endpoints = [
            ('GET', '/api/checklists'),
            ('POST', '/api/checklists'),
            ('GET', '/api/checklists/1'),
            ('PUT', '/api/checklists/1'),
            ('DELETE', '/api/checklists/1'),
            ('GET', '/api/checklists/1/items'),
            ('POST', '/api/checklists/1/items'),
            ('GET', '/api/checklists/1/items/1'),
            ('PUT', '/api/checklists/1/items/1'),
            ('DELETE', '/api/checklists/1/items/1'),
        ]
        
        for method, url in endpoints:
            response = self._api_request(method, url, expected_status=401)
            self.assertEqual(response['error'], 'Authentication required')

    # ========================================
    # CHECKLIST CRUD TESTS
    # ========================================

    def test_create_checklist(self):
        """Test creating a new checklist"""
        data = {'title': 'My Test Checklist'}
        response = self._api_request('POST', '/api/checklists', data, 201)
        
        self.assertIn('id', response)
        self.assertEqual(response['title'], 'My Test Checklist')
        self.assertIn('user_id', response)

    def test_create_checklist_validation(self):
        """Test checklist creation validation"""
        # Test missing title
        response = self._api_request('POST', '/api/checklists', {}, 400)
        self.assertEqual(response['error'], 'Title is required')
        
        # Test empty title
        response = self._api_request('POST', '/api/checklists', {'title': ''}, 400)
        self.assertEqual(response['error'], 'Title cannot be empty')
        
        # Test whitespace-only title
        response = self._api_request('POST', '/api/checklists', {'title': '   '}, 400)
        self.assertEqual(response['error'], 'Title cannot be empty')

    def test_get_checklists(self):
        """Test retrieving all checklists"""
        # Create test checklists
        self._api_request('POST', '/api/checklists', {'title': 'Checklist 1'}, 201)
        self._api_request('POST', '/api/checklists', {'title': 'Checklist 2'}, 201)
        
        # Get all checklists
        response = self._api_request('GET', '/api/checklists')
        
        self.assertIn('checklists', response)
        self.assertEqual(len(response['checklists']), 2)
        self.assertEqual(response['checklists'][0]['title'], 'Checklist 1')
        self.assertEqual(response['checklists'][1]['title'], 'Checklist 2')

    def test_get_specific_checklist(self):
        """Test retrieving a specific checklist with items"""
        # Create checklist
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        # Add items to checklist
        self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                         {'content': 'Item 1'}, 201)
        self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                         {'content': 'Item 2'}, 201)
        
        # Get specific checklist
        response = self._api_request('GET', f'/api/checklists/{checklist_id}')
        
        self.assertEqual(response['title'], 'Test Checklist')
        self.assertEqual(len(response['items']), 2)

    def test_update_checklist(self):
        """Test updating a checklist"""
        # Create checklist
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Original Title'}, 201)
        checklist_id = checklist_response['id']
        
        # Update checklist
        response = self._api_request('PUT', f'/api/checklists/{checklist_id}', 
                                   {'title': 'Updated Title'})
        
        self.assertEqual(response['title'], 'Updated Title')
        self.assertEqual(response['id'], checklist_id)

    def test_delete_checklist(self):
        """Test deleting a checklist"""
        # Create checklist
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'To Delete'}, 201)
        checklist_id = checklist_response['id']
        
        # Delete checklist
        response = self._api_request('DELETE', f'/api/checklists/{checklist_id}')
        self.assertEqual(response['message'], 'Checklist deleted successfully')
        
        # Verify it's deleted
        self._api_request('GET', f'/api/checklists/{checklist_id}', expected_status=404)

    # ========================================
    # ITEM CRUD TESTS
    # ========================================

    def test_create_item(self):
        """Test creating a new item"""
        # Create checklist first
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        # Create item
        item_data = {
            'content': 'Test Item',
            'url': 'example.com',
            'checked': False
        }
        response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', item_data, 201)
        
        self.assertIn('id', response)
        self.assertEqual(response['content'], 'Test Item')
        self.assertEqual(response['url'], 'https://example.com')  # URL should be normalized
        self.assertEqual(response['checked'], False)
        self.assertEqual(response['checklist_id'], checklist_id)

    def test_create_subitem(self):
        """Test creating a subitem (item with parent)"""
        # Create checklist and parent item
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        parent_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                          {'content': 'Parent Item'}, 201)
        parent_id = parent_response['id']
        
        # Create subitem
        subitem_data = {
            'content': 'Sub Item',
            'parent_item_id': parent_id
        }
        response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', subitem_data, 201)
        
        self.assertEqual(response['content'], 'Sub Item')
        self.assertEqual(response['parent_item_id'], parent_id)

    def test_item_creation_validation(self):
        """Test item creation validation"""
        # Create checklist first
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        # Test missing content
        response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', {}, 400)
        self.assertEqual(response['error'], 'Content is required')
        
        # Test empty content
        response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                   {'content': ''}, 400)
        self.assertEqual(response['error'], 'Content cannot be empty')
        
        # Test invalid parent_item_id
        response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                   {'content': 'Test', 'parent_item_id': 'invalid'}, 400)
        self.assertEqual(response['error'], 'Invalid parent_item_id')

    def test_get_items(self):
        """Test retrieving all items in a checklist"""
        # Create checklist and items
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        self._api_request('POST', f'/api/checklists/{checklist_id}/items', {'content': 'Item 1'}, 201)
        self._api_request('POST', f'/api/checklists/{checklist_id}/items', {'content': 'Item 2'}, 201)
        
        # Get items
        response = self._api_request('GET', f'/api/checklists/{checklist_id}/items')
        
        self.assertEqual(response['checklist_id'], checklist_id)
        self.assertEqual(len(response['items']), 2)

    def test_get_specific_item(self):
        """Test retrieving a specific item"""
        # Create checklist and item
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        item_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                        {'content': 'Test Item'}, 201)
        item_id = item_response['id']
        
        # Get specific item
        response = self._api_request('GET', f'/api/checklists/{checklist_id}/items/{item_id}')
        
        self.assertEqual(response['content'], 'Test Item')
        self.assertEqual(response['id'], item_id)

    def test_update_item(self):
        """Test updating an item"""
        # Create checklist and item
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        item_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                        {'content': 'Original Content'}, 201)
        item_id = item_response['id']
        
        # Update item
        update_data = {
            'content': 'Updated Content',
            'url': 'updated-example.com',
            'checked': True
        }
        response = self._api_request('PUT', f'/api/checklists/{checklist_id}/items/{item_id}', update_data)
        
        self.assertEqual(response['content'], 'Updated Content')
        self.assertEqual(response['url'], 'https://updated-example.com')
        self.assertEqual(response['checked'], 1)  # Database stores as integer

    def test_toggle_item(self):
        """Test toggling an item's checked status"""
        # Create checklist and item
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        item_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                        {'content': 'Test Item'}, 201)
        item_id = item_response['id']
        
        # Toggle item (should become checked)
        response = self._api_request('POST', f'/api/checklists/{checklist_id}/items/{item_id}/toggle')
        self.assertEqual(response['checked'], True)
        self.assertIn('checked', response['message'])
        
        # Toggle again (should become unchecked)
        response = self._api_request('POST', f'/api/checklists/{checklist_id}/items/{item_id}/toggle')
        self.assertEqual(response['checked'], False)
        self.assertIn('unchecked', response['message'])

    def test_delete_item(self):
        """Test deleting an item"""
        # Create checklist and item
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Test Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        item_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                        {'content': 'To Delete'}, 201)
        item_id = item_response['id']
        
        # Delete item
        response = self._api_request('DELETE', f'/api/checklists/{checklist_id}/items/{item_id}')
        self.assertEqual(response['message'], 'Item deleted successfully')
        
        # Verify it's deleted
        self._api_request('GET', f'/api/checklists/{checklist_id}/items/{item_id}', expected_status=404)

    # ========================================
    # HIERARCHICAL STRUCTURE TESTS
    # ========================================

    def test_hierarchical_item_structure(self):
        """Test that items with subitems are properly structured"""
        # Create checklist
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Hierarchy Test'}, 201)
        checklist_id = checklist_response['id']
        
        # Create parent item
        parent_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                          {'content': 'Parent Item'}, 201)
        parent_id = parent_response['id']
        
        # Create subitems
        self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                         {'content': 'Subitem 1', 'parent_item_id': parent_id}, 201)
        self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                         {'content': 'Subitem 2', 'parent_item_id': parent_id}, 201)
        
        # Get checklist and verify hierarchical structure
        response = self._api_request('GET', f'/api/checklists/{checklist_id}')
        
        self.assertEqual(len(response['items']), 1)  # Only parent should be at root level
        parent_item = response['items'][0]
        self.assertEqual(parent_item['content'], 'Parent Item')
        self.assertEqual(len(parent_item['subitems']), 2)  # Should have 2 subitems

    def test_cascade_delete_subitems(self):
        """Test that deleting a parent item also deletes its subitems"""
        # Create checklist with parent and subitems
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'Cascade Test'}, 201)
        checklist_id = checklist_response['id']
        
        parent_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                          {'content': 'Parent Item'}, 201)
        parent_id = parent_response['id']
        
        subitem_response = self._api_request('POST', f'/api/checklists/{checklist_id}/items', 
                                           {'content': 'Subitem', 'parent_item_id': parent_id}, 201)
        subitem_id = subitem_response['id']
        
        # Delete parent item
        self._api_request('DELETE', f'/api/checklists/{checklist_id}/items/{parent_id}')
        
        # Verify both parent and subitem are deleted
        self._api_request('GET', f'/api/checklists/{checklist_id}/items/{parent_id}', expected_status=404)
        self._api_request('GET', f'/api/checklists/{checklist_id}/items/{subitem_id}', expected_status=404)

    # ========================================
    # AUTHORIZATION TESTS
    # ========================================

    def test_user_isolation(self):
        """Test that users can only access their own checklists"""
        # Create checklist as first user
        checklist_response = self._api_request('POST', '/api/checklists', {'title': 'User 1 Checklist'}, 201)
        checklist_id = checklist_response['id']
        
        # Logout and create second user
        self.client.get('/logout')
        self.client.post('/register', data={'username': 'user2', 'password': 'pass2'})
        self.client.post('/login', data={'username': 'user2', 'password': 'pass2'})
        
        # Try to access first user's checklist
        self._api_request('GET', f'/api/checklists/{checklist_id}', expected_status=404)
        
        # Try to modify first user's checklist
        self._api_request('PUT', f'/api/checklists/{checklist_id}', {'title': 'Hacked'}, 404)
        self._api_request('DELETE', f'/api/checklists/{checklist_id}', expected_status=404)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 