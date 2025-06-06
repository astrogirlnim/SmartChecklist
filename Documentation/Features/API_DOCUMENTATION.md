# Smart Checklist API Documentation

This document describes the REST API endpoints for the Smart Checklist application. The API supports full CRUD operations for checklists and items, including hierarchical subitems.

## Base URL
All API endpoints are prefixed with `/api`

## Authentication
All API endpoints require user authentication via session cookies. Users must first login through the web interface:

```bash
# Login via web interface
POST /login
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

## Response Format
All API responses are in JSON format. Successful responses include relevant data, while error responses include an `error` field with a descriptive message.

## HTTP Status Codes
- `200 OK` - Request successful
- `201 Created` - Resource successfully created
- `400 Bad Request` - Invalid input or missing required fields
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found

---

## Checklist Endpoints

### Get All Checklists
Retrieve all checklists for the authenticated user.

**Request:**
```
GET /api/checklists
```

**Response:**
```json
{
  "checklists": [
    {
      "id": 1,
      "title": "My Shopping List"
    },
    {
      "id": 2,
      "title": "Project Tasks"
    }
  ]
}
```

### Create Checklist
Create a new checklist.

**Request:**
```
POST /api/checklists
Content-Type: application/json

{
  "title": "New Checklist"
}
```

**Response:**
```json
{
  "id": 3,
  "title": "New Checklist",
  "user_id": 1
}
```

**Validation:**
- `title` is required and cannot be empty

### Get Specific Checklist
Retrieve a specific checklist with all its items (hierarchically organized).

**Request:**
```
GET /api/checklists/1
```

**Response:**
```json
{
  "id": 1,
  "title": "My Shopping List",
  "user_id": 1,
  "items": [
    {
      "id": 1,
      "checklist_id": 1,
      "parent_item_id": null,
      "content": "Groceries",
      "url": null,
      "checked": 0,
      "subitems": [
        {
          "id": 2,
          "checklist_id": 1,
          "parent_item_id": 1,
          "content": "Milk",
          "url": null,
          "checked": 1,
          "subitems": []
        }
      ]
    }
  ]
}
```

### Update Checklist
Update a checklist's properties.

**Request:**
```
PUT /api/checklists/1
Content-Type: application/json

{
  "title": "Updated Checklist Title"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Checklist Title"
}
```

### Delete Checklist
Delete a checklist and all its items.

**Request:**
```
DELETE /api/checklists/1
```

**Response:**
```json
{
  "message": "Checklist deleted successfully"
}
```

---

## Item Endpoints

### Get All Items in Checklist
Retrieve all items in a specific checklist (hierarchically organized).

**Request:**
```
GET /api/checklists/1/items
```

**Response:**
```json
{
  "checklist_id": 1,
  "items": [
    {
      "id": 1,
      "checklist_id": 1,
      "parent_item_id": null,
      "content": "Main Task",
      "url": "https://example.com",
      "checked": 0,
      "subitems": [
        {
          "id": 2,
          "checklist_id": 1,
          "parent_item_id": 1,
          "content": "Subtask",
          "url": null,
          "checked": 1,
          "subitems": []
        }
      ]
    }
  ]
}
```

### Create Item
Create a new item in a checklist.

**Request:**
```
POST /api/checklists/1/items
Content-Type: application/json

{
  "content": "New Task",
  "url": "example.com",
  "checked": false,
  "parent_item_id": null
}
```

**Response:**
```json
{
  "id": 3,
  "checklist_id": 1,
  "parent_item_id": null,
  "content": "New Task",
  "url": "https://example.com",
  "checked": false
}
```

**Validation:**
- `content` is required and cannot be empty
- `url` is optional; if provided without protocol, "https://" is prepended
- `checked` is optional; defaults to false
- `parent_item_id` is optional; if provided, creates a subitem

### Create Subitem
Create a subitem by specifying a `parent_item_id`.

**Request:**
```
POST /api/checklists/1/items
Content-Type: application/json

{
  "content": "Subitem",
  "parent_item_id": 1
}
```

**Response:**
```json
{
  "id": 4,
  "checklist_id": 1,
  "parent_item_id": 1,
  "content": "Subitem",
  "url": null,
  "checked": false
}
```

### Get Specific Item
Retrieve a specific item with its subitems.

**Request:**
```
GET /api/checklists/1/items/1
```

**Response:**
```json
{
  "id": 1,
  "checklist_id": 1,
  "parent_item_id": null,
  "content": "Main Task",
  "url": "https://example.com",
  "checked": 0,
  "subitems": [
    {
      "id": 2,
      "checklist_id": 1,
      "parent_item_id": 1,
      "content": "Subtask",
      "url": null,
      "checked": 1,
      "subitems": []
    }
  ]
}
```

### Update Item
Update an item's properties. Only provided fields will be updated.

**Request:**
```
PUT /api/checklists/1/items/1
Content-Type: application/json

{
  "content": "Updated Task",
  "url": "new-example.com",
  "checked": true
}
```

**Response:**
```json
{
  "id": 1,
  "checklist_id": 1,
  "parent_item_id": null,
  "content": "Updated Task",
  "url": "https://new-example.com",
  "checked": 1
}
```

**Validation:**
- `content` cannot be empty if provided
- `url` will be normalized with "https://" if needed
- `checked` will be converted to boolean

### Toggle Item Status
Toggle an item's checked status (checked ↔ unchecked).

**Request:**
```
POST /api/checklists/1/items/1/toggle
```

**Response:**
```json
{
  "id": 1,
  "checked": true,
  "message": "Item checked"
}
```

### Delete Item
Delete an item and all its subitems (cascade deletion).

**Request:**
```
DELETE /api/checklists/1/items/1
```

**Response:**
```json
{
  "message": "Item deleted successfully"
}
```

**Note:** Deleting a parent item will automatically delete all its subitems.

---

## Example Usage

### cURL Examples

**Create a checklist:**
```bash
curl -X POST http://localhost:5000/api/checklists \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title": "My API Checklist"}'
```

**Add an item:**
```bash
curl -X POST http://localhost:5000/api/checklists/1/items \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"content": "Test API item", "url": "github.com"}'
```

**Get checklist with items:**
```bash
curl -X GET http://localhost:5000/api/checklists/1 \
  -b cookies.txt
```

### JavaScript/Fetch Example

```javascript
// Create checklist
const response = await fetch('/api/checklists', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include', // Include session cookies
  body: JSON.stringify({
    title: 'My JavaScript Checklist'
  })
});

const checklist = await response.json();
console.log('Created checklist:', checklist);

// Add item to checklist
const itemResponse = await fetch(`/api/checklists/${checklist.id}/items`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    content: 'JavaScript API item',
    url: 'developer.mozilla.org',
    checked: false
  })
});

const item = await itemResponse.json();
console.log('Created item:', item);
```

---

## Error Handling

All error responses follow this format:

```json
{
  "error": "Descriptive error message"
}
```

**Common Errors:**
- `401 Unauthorized`: "Authentication required"
- `400 Bad Request`: "Title is required", "Content cannot be empty", etc.
- `404 Not Found`: "Checklist not found", "Item not found"

---

## Data Model

### Checklist Object
```json
{
  "id": 1,
  "title": "string",
  "user_id": 1
}
```

### Item Object
```json
{
  "id": 1,
  "checklist_id": 1,
  "parent_item_id": null,
  "content": "string",
  "url": "string or null",
  "checked": 0 or 1,
  "subitems": []
}
```

### Hierarchical Structure
Items are organized hierarchically where:
- Root items have `parent_item_id = null`
- Subitems reference their parent via `parent_item_id`
- Each item includes a `subitems` array in API responses
- Deleting a parent item cascades to all subitems

---

## Implementation Notes

1. **Authentication**: Uses Flask-Login session-based authentication
2. **URL Normalization**: URLs without protocol automatically get "https://" prepended
3. **Hierarchical Organization**: Items are automatically organized into parent-child relationships
4. **Cascade Deletion**: Deleting parents automatically deletes all children
5. **Data Validation**: Comprehensive input validation with meaningful error messages
6. **User Isolation**: Users can only access their own checklists and items 