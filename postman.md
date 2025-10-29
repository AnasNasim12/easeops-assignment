# 🚀 Complete Postman Testing Guide for EaseOps E-Library API

## Prerequisites

1. **Start your FastAPI server**: `uvicorn main:app --reload`
2. **Create sample data**: `python3 create_sample_data.py`
3. **Server running on**: `http://localhost:8000`

## 📋 Testing Workflow Overview

1. **Authentication** → Get JWT Token
2. **User Profile Management**
3. **Library Access & Browsing**
4. **Bookmarks & Notes**
5. **User Interactions**
6. **Notifications**

---

## 🔐 1. AUTHENTICATION TESTING

### 1.1 User Registration

**POST** `http://localhost:8000/api/auth/register`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "testuser@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "password": "password123"
}
```

**Expected Response:** `200 OK`
```json
{
  "id": 1,
  "email": "testuser@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "is_active": true,
  "is_verified": false,
  "dark_mode": false,
  "email_notifications": true,
  "whatsapp_notifications": false,
  "created_at": "2024-01-01T00:00:00"
}
```

### 1.2 User Login

**POST** `http://localhost:8000/api/auth/login`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Expected Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

**💡 Save the `access_token` for authenticated requests!**

### 1.3 Get Current User Info

**GET** `http://localhost:8000/api/auth/me`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Expected Response:** `200 OK` (User profile data)

### 1.4 Test Invalid Login

**POST** `http://localhost:8000/api/auth/login`

**Body (JSON):**
```json
{
  "username": "wronguser",
  "password": "wrongpass"
}
```

**Expected Response:** `401 Unauthorized`

---

## 👤 2. USER PROFILE MANAGEMENT

### 2.1 Get User Profile

**GET** `http://localhost:8000/api/users/profile`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 2.2 Update User Profile

**PUT** `http://localhost:8000/api/users/profile`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "full_name": "Updated Test User",
  "dark_mode": true,
  "email_notifications": false,
  "whatsapp_notifications": false
}
```

### 2.3 Get User Preferences

**GET** `http://localhost:8000/api/users/preferences`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 2.4 Update User Preferences

**PUT** `http://localhost:8000/api/users/preferences`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "dark_mode": true,
  "email_notifications": true,
  "whatsapp_notifications": false
}
```

---

## 📚 3. LIBRARY ACCESS & BROWSING

### 3.1 Get All Books

**GET** `http://localhost:8000/api/library/books`

**Expected Response:** `200 OK` (Array of books)

### 3.2 Get Books with Pagination

**GET** `http://localhost:8000/api/library/books?skip=0&limit=5`

### 3.3 Filter Books by Category

**GET** `http://localhost:8000/api/library/books?category=Fiction`

### 3.4 Search Books

**GET** `http://localhost:8000/api/library/books?search=gatsby`

### 3.5 Filter by Tags

**GET** `http://localhost:8000/api/library/books?tags=classic,american`

### 3.6 Get Specific Book

**GET** `http://localhost:8000/api/library/books/1`

**Expected Response:** `200 OK` (Single book details)

### 3.7 Get All Categories

**GET** `http://localhost:8000/api/library/categories`

**Expected Response:** `200 OK`
```json
["Fiction", "Science Fiction", "Romance", "Programming", "Philosophy"]
```

### 3.8 Get All Tags

**GET** `http://localhost:8000/api/library/tags`

### 3.9 Get Featured Books

**GET** `http://localhost:8000/api/library/featured?limit=3`

### 3.10 Get Popular Books

**GET** `http://localhost:8000/api/library/popular?limit=3`

### 3.11 Test Invalid Book ID

**GET** `http://localhost:8000/api/library/books/99999`

**Expected Response:** `404 Not Found`

---

## 🔖 4. BOOKMARKS & NOTES

### 4.1 Get User's Bookmarks

**GET** `http://localhost:8000/api/bookmarks/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 4.2 Add Bookmark

**POST** `http://localhost:8000/api/bookmarks/1`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Expected Response:** `200 OK`
```json
{
  "message": "Book bookmarked successfully"
}
```

### 4.3 Add Another Bookmark

**POST** `http://localhost:8000/api/bookmarks/2`

### 4.4 Get Bookmarks Again (Verify)

**GET** `http://localhost:8000/api/bookmarks/`

### 4.5 Remove Bookmark

**DELETE** `http://localhost:8000/api/bookmarks/1`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 4.6 Test Adding Duplicate Bookmark

**POST** `http://localhost:8000/api/bookmarks/2`

**Expected Response:** `400 Bad Request`

### 4.7 Get User's Notes

**GET** `http://localhost:8000/api/bookmarks/notes`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 4.8 Get Notes for Specific Book

**GET** `http://localhost:8000/api/bookmarks/notes?book_id=1`

### 4.9 Create Note

**POST** `http://localhost:8000/api/bookmarks/notes`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "book_id": 1,
  "page_number": 10,
  "note_text": "This is an interesting chapter about Gatsby's mysterious past."
}
```

### 4.10 Create Another Note

**POST** `http://localhost:8000/api/bookmarks/notes`

**Body (JSON):**
```json
{
  "book_id": 2,
  "page_number": 25,
  "note_text": "Important character development here."
}
```

### 4.11 Update Note

**PUT** `http://localhost:8000/api/bookmarks/notes/1`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "note_text": "Updated note: This chapter reveals Gatsby's true identity!"
}
```

### 4.12 Delete Note

**DELETE** `http://localhost:8000/api/bookmarks/notes/2`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

---

## 💬 5. USER INTERACTIONS

### 5.1 Submit Feedback

**POST** `http://localhost:8000/api/interactions/feedback`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "feedback_type": "feature_request",
  "subject": "Dark Mode Enhancement",
  "message": "Please add more customization options for dark mode. The current implementation is good but could use more color themes."
}
```

### 5.2 Submit Bug Report

**POST** `http://localhost:8000/api/interactions/feedback`

**Body (JSON):**
```json
{
  "feedback_type": "bug_report",
  "subject": "Search Not Working",
  "message": "The search functionality sometimes returns incorrect results when searching for books with special characters."
}
```

### 5.3 Get User's Feedback

**GET** `http://localhost:8000/api/interactions/feedback`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 5.4 Submit Contact Request

**POST** `http://localhost:8000/api/interactions/contact`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "subject": "Account Issue",
  "message": "I'm having trouble accessing my account. Can you please help me reset my password?"
}
```

### 5.5 Get Active Surveys

**GET** `http://localhost:8000/api/interactions/surveys`

### 5.6 Get Specific Survey

**GET** `http://localhost:8000/api/interactions/surveys/1`

### 5.7 Respond to Survey

**POST** `http://localhost:8000/api/interactions/surveys/1/respond`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "survey_id": 1,
  "responses": {
    "1": "Weekly",
    "2": ["Bookmarks", "Search", "Categories"],
    "3": 4,
    "4": "The app is great! Maybe add more book categories."
  }
}
```

### 5.8 Get FAQs

**GET** `http://localhost:8000/api/interactions/faq`

### 5.9 Share Book

**POST** `http://localhost:8000/api/interactions/share/1`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "platform": "twitter"
}
```

---

## 🔔 6. NOTIFICATIONS

### 6.1 Get User Notifications

**GET** `http://localhost:8000/api/notifications/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 6.2 Subscribe to New Releases

**POST** `http://localhost:8000/api/notifications/subscribe/new-releases`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### 6.3 Send Test Email Notification

**POST** `http://localhost:8000/api/notifications/test`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "notification_type": "email"
}
```

### 6.4 Unsubscribe from New Releases

**POST** `http://localhost:8000/api/notifications/unsubscribe/new-releases`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

---

## 🧪 7. ERROR TESTING

### 7.1 Test Unauthorized Access

**GET** `http://localhost:8000/api/users/profile`

**Expected Response:** `401 Unauthorized`

### 7.2 Test Invalid Token

**GET** `http://localhost:8000/api/users/profile`

**Headers:**
```
Authorization: Bearer invalid_token_here
```

**Expected Response:** `401 Unauthorized`

### 7.3 Test Invalid Bookmark

**POST** `http://localhost:8000/api/bookmarks/99999`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Expected Response:** `404 Not Found`

### 7.4 Test Invalid Note Update

**PUT** `http://localhost:8000/api/bookmarks/notes/99999`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "note_text": "This note doesn't exist"
}
```

**Expected Response:** `404 Not Found`

---

## 📊 8. PERFORMANCE TESTING

### 8.1 Test Pagination Performance

**GET** `http://localhost:8000/api/library/books?skip=0&limit=100`

### 8.2 Test Search Performance

**GET** `http://localhost:8000/api/library/books?search=the`

### 8.3 Test Multiple Concurrent Requests

Run the same request multiple times simultaneously to test concurrency.

---

## 🎯 9. COMPLETE USER JOURNEY TEST

### Step-by-Step Complete Flow:

1. **Register** → Get user account
2. **Login** → Get JWT token
3. **Browse Books** → Explore library
4. **Search Books** → Find specific content
5. **Add Bookmarks** → Save interesting books
6. **Create Notes** → Add reading notes
7. **Update Profile** → Customize preferences
8. **Submit Feedback** → Provide input
9. **Take Survey** → Participate in research
10. **Test Notifications** → Verify email settings

---

## 📝 10. POSTMAN COLLECTION SETUP

### Environment Variables:

Create a Postman environment with:
```
base_url: http://localhost:8000
access_token: (will be set after login)
```

### Pre-request Script (for authenticated endpoints):

```javascript
pm.request.headers.add({
    key: 'Authorization',
    value: 'Bearer ' + pm.environment.get('access_token')
});
```

### Test Script (for login endpoint):

```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set('access_token', response.access_token);
}
```

---

## ✅ Expected Results Summary

- **Authentication**: Secure JWT-based login/logout
- **Profile Management**: Dark mode, notification preferences
- **Library Access**: Browse, search, filter books by category/tags
- **Bookmarks**: Add/remove bookmarks, create/manage notes
- **Interactions**: Submit feedback, contact requests, surveys
- **Notifications**: Email notifications for new releases

This comprehensive testing guide covers all the features you initially requested! 🚀

---

## 🔧 Troubleshooting Common Issues

### Authentication Issues
- **401 Unauthorized**: Check if JWT token is valid and properly formatted
- **Token Expired**: Re-login to get a new token
- **Missing Authorization Header**: Ensure `Authorization: Bearer <token>` is included

### Database Issues
- **500 Internal Server Error**: Check if database is running and accessible
- **Validation Errors**: Verify request body format matches expected schema

### Email Notification Issues
- **SMTP Error**: Configure SMTP settings in `.env` file
- **Test Email Fails**: Use mock email function for testing without SMTP setup

### Route Conflicts
- **422 Unprocessable Entity**: Check if request parameters are in correct format (query vs body)
- **404 Not Found**: Verify endpoint URL and HTTP method

---

## 📋 Sample Test Data

### Default Users (from sample data):
- **johndoe** / password123
- **janesmith** / password123  
- **admin** / admin123

### Sample Books Available:
- The Great Gatsby (Fiction)
- To Kill a Mockingbird (Fiction)
- 1984 (Science Fiction)
- Pride and Prejudice (Romance)
- Python Programming (Programming)
- Clean Code (Programming)
- The Art of War (Philosophy)

---

## 🎉 Success Criteria

Your API testing is successful when:
- ✅ All authentication endpoints work correctly
- ✅ User profile management functions properly
- ✅ Library browsing and search work as expected
- ✅ Bookmarks and notes can be created, updated, and deleted
- ✅ User interactions (feedback, surveys) are functional
- ✅ Notification system responds appropriately
- ✅ Error handling works for invalid requests
- ✅ All endpoints return proper HTTP status codes