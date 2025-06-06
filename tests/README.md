# Smart Checklist API Tests

This directory contains comprehensive unit tests for the Smart Checklist API endpoints.

## Running the Tests

### Method 1: Direct execution
```bash
cd tests
python test_api.py
```

### Method 2: Using unittest discovery
```bash
# From project root
python -m unittest discover tests -v
```

### Method 3: Using pytest (if installed)
```bash
pip install pytest
pytest tests/ -v
```

## Test Structure

The test file `test_api.py` demonstrates several important testing patterns:

### 1. **Test Isolation**
- Each test uses a temporary SQLite database
- Database is created fresh for each test method
- Clean teardown ensures no test pollution

### 2. **Authentication Testing**
- Tests that API endpoints require authentication
- Tests user isolation (users can't access others' data)
- Demonstrates session-based authentication testing

### 3. **CRUD Operation Testing**
- **Create**: Tests POST endpoints with validation
- **Read**: Tests GET endpoints for lists and individual items
- **Update**: Tests PUT endpoints with partial updates
- **Delete**: Tests DELETE endpoints with cascade behavior

### 4. **Input Validation Testing**
- Tests required field validation
- Tests data type validation
- Tests business rule validation (e.g., URL normalization)

### 5. **Hierarchical Data Testing**
- Tests parent-child relationships between items
- Tests cascade deletion behavior
- Tests proper JSON structure for nested data

### 6. **Error Handling Testing**
- Tests proper HTTP status codes (200, 201, 400, 401, 404)
- Tests meaningful error messages
- Tests edge cases and boundary conditions

## Test Categories

### Authentication Tests
- `test_api_requires_authentication()`: Ensures all endpoints require login
- `test_user_isolation()`: Ensures users can't access others' data

### Checklist CRUD Tests
- `test_create_checklist()`: Creating new checklists
- `test_create_checklist_validation()`: Input validation
- `test_get_checklists()`: Retrieving all user checklists
- `test_get_specific_checklist()`: Retrieving individual checklist with items
- `test_update_checklist()`: Updating checklist properties
- `test_delete_checklist()`: Deleting checklists

### Item CRUD Tests
- `test_create_item()`: Creating items with URLs and status
- `test_create_subitem()`: Creating hierarchical subitems
- `test_item_creation_validation()`: Item validation rules
- `test_get_items()`: Retrieving all items in a checklist
- `test_get_specific_item()`: Retrieving individual items
- `test_update_item()`: Updating item properties
- `test_toggle_item()`: Toggling checked status
- `test_delete_item()`: Deleting items

### Hierarchical Structure Tests
- `test_hierarchical_item_structure()`: Tests proper nesting in responses
- `test_cascade_delete_subitems()`: Tests cascade deletion behavior

## Key Testing Patterns Demonstrated

### 1. Helper Methods
```python
def _api_request(self, method, url, data=None, expected_status=200):
    """Centralized API request handling with status validation"""
```

### 2. Test Data Setup
```python
def setUp(self):
    """Creates isolated test environment with temporary database"""
```

### 3. Authentication Setup
```python
def _create_and_login_user(self):
    """Helper to create authenticated test sessions"""
```

### 4. Assertion Patterns
```python
# Test successful creation
self.assertEqual(response.status_code, 201)
self.assertIn('id', response)

# Test validation errors
self.assertEqual(response.status_code, 400)
self.assertEqual(response['error'], 'Expected error message')
```

## Extending the Tests

When adding new API endpoints, follow these patterns:

1. **Add to the appropriate test section** (Authentication, CRUD, etc.)
2. **Test both success and failure cases**
3. **Validate HTTP status codes**
4. **Test input validation thoroughly**
5. **Test authorization/ownership rules**
6. **Use descriptive test method names**
7. **Add comprehensive docstrings**

## Dependencies

The tests use only Python standard library modules:
- `unittest` - Test framework
- `json` - JSON handling
- `tempfile` - Temporary file creation
- `os` - File system operations

No additional dependencies are required beyond what the main application uses. 