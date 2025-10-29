# API Testing Guide

This guide provides comprehensive testing instructions for the EaseOps E-Library User Backend API.

## Prerequisites

1. PostgreSQL database running
2. Python environment with dependencies installed
3. Sample data created (run `python create_sample_data.py`)

## Testing Tools

### Option 1: FastAPI Interactive Docs
- Start the server: `uvicorn main:app --reload`
- Visit: `http://localhost:8000/docs`
- Interactive API documentation with "Try it out" functionality

### Option 2: Postman Collection
Import the following collection for comprehensive testing:

```json
{
  "info": {
    "name": "EaseOps E-Library API",
    "description": "Complete API testing collection"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register User",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"username\": \"testuser\",\n  \"full_name\": \"Test User\",\n  \"password\": \"password123\"\n}"
            },
            "url": "http://localhost:8000/api/auth/register"
          }
        },
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"testuser\",\n  \"password\": \"password123\"\n}"
            },
            "url": "http://localhost:8000/api/auth/login"
          }
        },
        {
          "name": "Get Current User",
          "request": {
            "method": "GET",
            "header": [{"key": "Authorization", "value": "Bearer {{token}}"}],
            "url": "http://localhost:8000/api/auth/me"
          }
        }
      ]
    }
  ]
}
```

### Option 3: cURL Commands

#### 1. User Registration
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "password123"
  }'
```

#### 2. User Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

#### 3. Get Books (No Auth Required)
```bash
curl -X GET "http://localhost:8000/api/library/books"
```

#### 4. Get Books with Filtering
```bash
curl -X GET "http://localhost:8000/api/library/books?category=Fiction&search=gatsby"
```

#### 5. Add Bookmark (Requires Auth)
```bash
curl -X POST "http://localhost:8000/api/bookmarks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### 6. Create Note
```bash
curl -X POST "http://localhost:8000/api/bookmarks/notes" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "page_number": 10,
    "note_text": "This is an interesting chapter about Gatsby"
  }'
```

#### 7. Submit Feedback
```bash
curl -X POST "http://localhost:8000/api/interactions/feedback" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feedback_type": "feature_request",
    "subject": "Dark Mode Enhancement",
    "message": "Please add more customization options for dark mode"
  }'
```

## Test Scenarios

### Authentication Flow
1. Register a new user
2. Login with credentials
3. Use the JWT token for authenticated requests
4. Test token expiration

### Library Access
1. Browse all books
2. Filter by category
3. Search by title/author
4. Get book details
5. Test pagination

### User Preferences
1. Update user profile
2. Toggle dark mode
3. Change notification preferences
4. Verify changes persist

### Bookmarks & Notes
1. Add bookmarks
2. Remove bookmarks
3. Create notes for books
4. Update notes
5. Delete notes
6. View all bookmarks

### User Interactions
1. Submit feedback
2. Submit contact request
3. View active surveys
4. Respond to survey
5. Access FAQs
6. Share books

### Notifications
1. Subscribe to new releases
2. Send test notifications
3. View notification history
4. Mark notifications as read

## Error Testing

### Invalid Credentials
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "wronguser",
    "password": "wrongpass"
  }'
```

### Unauthorized Access
```bash
curl -X GET "http://localhost:8000/api/users/profile"
```

### Invalid Book ID
```bash
curl -X GET "http://localhost:8000/api/library/books/99999"
```

## Performance Testing

### Load Testing with Apache Bench
```bash
# Test book listing endpoint
ab -n 100 -c 10 http://localhost:8000/api/library/books

# Test with authentication
ab -n 50 -c 5 -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/users/profile
```

## Database Testing

### Check Sample Data
```sql
-- Connect to PostgreSQL and run:
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM books;
SELECT COUNT(*) FROM surveys;

-- Check user preferences
SELECT username, dark_mode, email_notifications FROM users;

-- Check book categories
SELECT DISTINCT category FROM books;
```

## Automated Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test Coverage
```bash
pytest --cov=. tests/
```

## Common Issues & Solutions

### 1. Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in config.py
- Verify database exists

### 2. JWT Token Issues
- Check SECRET_KEY in config.py
- Verify token format: `Bearer <token>`
- Check token expiration

### 3. Email Notification Failures
- Configure SMTP settings in .env
- Use app-specific passwords for Gmail
- Check firewall settings

### 4. Import Errors
- Ensure all dependencies are installed
- Check Python path
- Verify __init__.py files exist

## Sample Test Data

The `create_sample_data.py` script creates:
- 3 sample users (johndoe, janesmith, admin)
- 8 sample books across different categories
- 1 sample survey
- All users have password: "password123"

## API Response Examples

### Successful Login Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Book List Response
```json
[
  {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "description": "A classic American novel set in the Jazz Age.",
    "category": "Fiction",
    "tags": ["classic", "american", "literature"],
    "isbn": "9780743273565",
    "language": "English",
    "page_count": 180,
    "is_available": true,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Error Response
```json
{
  "detail": "Book not found"
}
```

## Security Testing

### SQL Injection
Test with malicious input:
```bash
curl -X GET "http://localhost:8000/api/library/books?search='; DROP TABLE books; --"
```

### XSS Prevention
Test with script tags:
```bash
curl -X POST "http://localhost:8000/api/interactions/feedback" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "feedback_type": "general",
    "subject": "<script>alert(\"XSS\")</script>",
    "message": "Test message"
  }'
```

This comprehensive testing guide ensures all API endpoints are thoroughly tested and validated.

