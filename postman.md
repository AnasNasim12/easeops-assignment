🚀 Complete Postman Testing Guide for EaseOps E-Library API
Prerequisites
Start your FastAPI server: uvicorn main:app --reload
Create sample data: python3 create_sample_data.py
Server running on: http://localhost:8000
📋 Testing Workflow Overview
Authentication → Get JWT Token
User Profile Management
Library Access & Browsing
Bookmarks & Notes
User Interactions
Notifications
🔐 1. AUTHENTICATION TESTING
1.1 User Registration
POST http://localhost:8000/api/auth/register
Headers:
Body (JSON):
Expected Response: 200 OK
1.2 User Login
POST http://localhost:8000/api/auth/login
Headers:
Body (JSON):
Expected Response: 200 OK
💡 Save the access_token for authenticated requests!
1.3 Get Current User Info
GET http://localhost:8000/api/auth/me
Headers:
YOUR_ACCESS_TOKEN_HERE
Expected Response: 200 OK (User profile data)
1.4 Test Invalid Login
POST http://localhost:8000/api/auth/login
Body (JSON):
Expected Response: 401 Unauthorized
👤 2. USER PROFILE MANAGEMENT
2.1 Get User Profile
GET http://localhost:8000/api/users/profile
Headers:
2.2 Update User Profile
PUT http://localhost:8000/api/users/profile
Headers:
Body (JSON):
2.3 Get User Preferences
GET http://localhost:8000/api/users/preferences
Headers:
2.4 Update User Preferences
PUT http://localhost:8000/api/users/preferences
Headers:
Body (JSON):
📚 3. LIBRARY ACCESS & BROWSING
3.1 Get All Books
GET http://localhost:8000/api/library/books
Expected Response: 200 OK (Array of books)
3.2 Get Books with Pagination
GET http://localhost:8000/api/library/books?skip=0&limit=5
3.3 Filter Books by Category
GET http://localhost:8000/api/library/books?category=Fiction
3.4 Search Books
GET http://localhost:8000/api/library/books?search=gatsby
3.5 Filter by Tags
GET http://localhost:8000/api/library/books?tags=classic,american
3.6 Get Specific Book
GET http://localhost:8000/api/library/books/1
Expected Response: 200 OK (Single book details)
3.7 Get All Categories
GET http://localhost:8000/api/library/categories
Expected Response: 200 OK
3.8 Get All Tags
GET http://localhost:8000/api/library/tags
3.9 Get Featured Books
GET http://localhost:8000/api/library/featured?limit=3
3.10 Get Popular Books
GET http://localhost:8000/api/library/popular?limit=3
3.11 Test Invalid Book ID
GET http://localhost:8000/api/library/books/99999
Expected Response: 404 Not Found
🔖 4. BOOKMARKS & NOTES
4.1 Get User's Bookmarks
GET http://localhost:8000/api/bookmarks/
Headers:
4.2 Add Bookmark
POST http://localhost:8000/api/bookmarks/1
Headers:
YOUR_ACCESS_TOKEN_HERE
Expected Response: 200 OK
4.3 Add Another Bookmark
POST http://localhost:8000/api/bookmarks/2
4.4 Get Bookmarks Again (Verify)
GET http://localhost:8000/api/bookmarks/
4.5 Remove Bookmark
DELETE http://localhost:8000/api/bookmarks/1
Headers:
4.6 Test Adding Duplicate Bookmark
POST http://localhost:8000/api/bookmarks/2
Expected Response: 400 Bad Request
4.7 Get User's Notes
GET http://localhost:8000/api/bookmarks/notes
Headers:
4.8 Get Notes for Specific Book
GET http://localhost:8000/api/bookmarks/notes?book_id=1
4.9 Create Note
POST http://localhost:8000/api/bookmarks/notes
Headers:
Body (JSON):
4.10 Create Another Note
POST http://localhost:8000/api/bookmarks/notes
Body (JSON):
4.11 Update Note
PUT http://localhost:8000/api/bookmarks/notes/1
Headers:
Body (JSON):
4.12 Delete Note
DELETE http://localhost:8000/api/bookmarks/notes/2
Headers:
💬 5. USER INTERACTIONS
5.1 Submit Feedback
POST http://localhost:8000/api/interactions/feedback
Headers:
Body (JSON):
5.2 Submit Bug Report
POST http://localhost:8000/api/interactions/feedback
Body (JSON):
5.3 Get User's Feedback
GET http://localhost:8000/api/interactions/feedback
Headers:
5.4 Submit Contact Request
POST http://localhost:8000/api/interactions/contact
Headers:
json
Body (JSON):
5.5 Get Active Surveys
GET http://localhost:8000/api/interactions/surveys
5.6 Get Specific Survey
GET http://localhost:8000/api/interactions/surveys/1
5.7 Respond to Survey
POST http://localhost:8000/api/interactions/surveys/1/respond
Headers:
Body (JSON):
5.8 Get FAQs
GET http://localhost:8000/api/interactions/faq
5.9 Share Book
POST http://localhost:8000/api/interactions/share/1
Headers:
Body (JSON):
🔔 6. NOTIFICATIONS
6.1 Get User Notifications
GET http://localhost:8000/api/notifications/
Headers:
6.2 Subscribe to New Releases
POST http://localhost:8000/api/notifications/subscribe/new-releases
Headers:
6.3 Send Test Email Notification
POST http://localhost:8000/api/notifications/test
Headers:
Body (JSON):
6.4 Unsubscribe from New Releases
POST http://localhost:8000/api/notifications/unsubscribe/new-releases
Headers:
YOUR_ACCESS_TOKEN_HERE
🧪 7. ERROR TESTING
7.1 Test Unauthorized Access
GET http://localhost:8000/api/users/profile
Expected Response: 401 Unauthorized
7.2 Test Invalid Token
GET http://localhost:8000/api/users/profile
Headers:
Expected Response: 401 Unauthorized
7.3 Test Invalid Bookmark
POST http://localhost:8000/api/bookmarks/99999
Headers:
Expected Response: 404 Not Found
7.4 Test Invalid Note Update
PUT http://localhost:8000/api/bookmarks/notes/99999
Headers:
Body (JSON):
Expected Response: 404 Not Found
📊 8. PERFORMANCE TESTING
8.1 Test Pagination Performance
GET http://localhost:8000/api/library/books?skip=0&limit=100
8.2 Test Search Performance
GET http://localhost:8000/api/library/books?search=the
8.3 Test Multiple Concurrent Requests
Run the same request multiple times simultaneously to test concurrency.
🎯 9. COMPLETE USER JOURNEY TEST
Step-by-Step Complete Flow:
Register → Get user account
Login → Get JWT token
Browse Books → Explore library
Search Books → Find specific content
Add Bookmarks → Save interesting books
Create Notes → Add reading notes
Update Profile → Customize preferences
Submit Feedback → Provide input
Take Survey → Participate in research
Test Notifications → Verify email settings
📝 10. POSTMAN COLLECTION SETUP
Environment Variables:
Create a Postman environment with:
Pre-request Script (for authenticated endpoints):
Test Script (for login endpoint):
✅ Expected Results Summary
Authentication: Secure JWT-based login/logout
Profile Management: Dark mode, notification preferences
Library Access: Browse, search, filter books by category/tags
Bookmarks: Add/remove bookmarks, create/manage notes
Interactions: Submit feedback, contact requests, surveys
Notifications: Email notifications for new releases
This comprehensive testing guide covers all the features you initially requested! 🚀
