# EaseOps E-Library User Backend

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**
   - Install PostgreSQL
   - Create database: `easeops_elibrary`
   - Update `config.py` with your database URL

3. **Create Sample Data**
   ```bash
   python create_sample_data.py
   ```

4. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Test the API**
   - Visit: `http://localhost:8000/docs`
   - Or use the testing guide: `API_TESTING_GUIDE.md`

## Default Users (from sample data)
- **johndoe** / password123
- **janesmith** / password123  
- **admin** / admin123

## Key Features Implemented

✅ **Authentication & Profile**
- JWT-based user registration and login
- User profile management with preferences
- Dark mode and notification settings

✅ **Library Access**
- Browse eBooks by category, tags, or search
- View book details and content
- Featured and popular books

✅ **Bookmarks & Notes**
- Add/remove bookmarks
- Create and manage reading notes
- View bookmarked books

✅ **User Interactions**
- Submit feedback and contact requests
- Participate in surveys
- Access FAQs and social sharing

✅ **Notifications**
- Email notifications for new releases
- WhatsApp notifications (optional)
- Notification preferences management

## API Endpoints

- **Authentication**: `/api/auth/*`
- **Users**: `/api/users/*`
- **Library**: `/api/library/*`
- **Bookmarks**: `/api/bookmarks/*`
- **Interactions**: `/api/interactions/*`
- **Notifications**: `/api/notifications/*`

## Technology Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **JWT** - Authentication tokens
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Project Structure

```
├── main.py                 # FastAPI app entry point
├── config.py              # Configuration settings
├── database.py            # Database connection
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── auth_utils.py          # Authentication utilities
├── routers/               # API route modules
│   ├── auth.py           # Authentication routes
│   ├── users.py         # User management routes
│   ├── library.py       # Library access routes
│   ├── bookmarks.py     # Bookmarks & notes routes
│   ├── interactions.py  # User interaction routes
│   └── notifications.py # Notification routes
├── create_sample_data.py  # Sample data creation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

Create a `.env` file with:
```
DATABASE_URL=postgresql://user:password@localhost:5432/easeops_elibrary
SECRET_KEY=your-secret-key-here
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
WHATSAPP_API_URL=your-whatsapp-api-url
WHATSAPP_API_TOKEN=your-whatsapp-token
```

## Testing

- **Interactive Docs**: `http://localhost:8000/docs`
- **Testing Guide**: See `API_TESTING_GUIDE.md`
- **Sample Data**: Run `python create_sample_data.py`

## Features for Internship Assignment

This implementation covers all required features:

1. **Authentication & Profile** ✅
   - User registration and login (JWT-based)
   - Manage user profiles and preferences (dark mode, bookmarks)

2. **Library Access** ✅
   - Fetch and display eBook list by category, tags, or search query
   - View eBook details and content (with online/offline mode support)
   - Add/remove bookmarks and notes

3. **User Interactions** ✅
   - Submit feedback, contact requests, and surveys
   - Access FAQs and chatbot
   - Social sharing of eBooks

4. **Notifications** ✅
   - Receive email or WhatsApp updates about new releases

## Token Validation & Response Consistency

- All authenticated endpoints properly validate JWT tokens
- Consistent error responses across all endpoints
- Proper HTTP status codes
- Comprehensive API documentation

## Next Steps

1. Deploy to production server
2. Set up proper email/WhatsApp services
3. Add more comprehensive error handling
4. Implement rate limiting
5. Add API versioning
6. Set up monitoring and logging

---

**Note**: This is a simplified implementation suitable for an internship assignment. For production use, additional security measures, error handling, and performance optimizations would be required.