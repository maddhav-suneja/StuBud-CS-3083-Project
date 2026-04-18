# StuBud - Study Group Collaboration Platform

A web-based application for NYU students to create, join, and manage study groups with integrated feedback and scheduling features.

## Project Overview

StuBud is a comprehensive student collaboration application built on a modern web architecture with:
- Flask-based backend with RESTful API
- Supabase (PostgreSQL) database backend
- Responsive HTML/CSS frontend
- JWT-based authentication
- Role-based access control

## Database Design

### Tables

1. **Student**: User accounts with authentication details
2. **Student_Available_Time**: Availability slots for each student
3. **Course**: Course information
4. **Student_Course**: Enrollment relationships
5. **Location**: Physical meeting locations
6. **Meeting**: Study group meetings
7. **Meeting_Request**: Student meeting participation
8. **Feedback**: Meeting ratings and comments
9. **Invitation**: Meeting invitations
10. **Study_Material**: Shared files and resources

### Key Relationships

- Students belong to courses (`Student_Course`)
- Students attend meetings (`Meeting_Request`)
- Meetings have locations and courses
- Feedback links students to meetings with ratings

## Project Structure

```
Complete\ Demo/
├── app.py                         # Main Flask application
├── requirements.txt               # Python dependencies
├── backend/
│   ├── config.py                 # Configuration (Supabase credentials)
│   ├── routes/
│   │   ├── auth_routes.py        # Login/signup endpoints
│   │   ├── public_routes.py      # Public data endpoints
│   │   ├── profile_routes.py     # Profile management
│   │   ├── dashboard_routes.py   # Dashboard data
│   │   └── groups_and_feedbacks.py  # Groups and feedback endpoints
│   ├── services/
│   │   ├── db.py                 # Supabase database client
│   │   ├── auth.py               # Authentication logic
│   │   ├── student_service.py    # Student data operations
│   │   └── responses.py          # Response formatting
│   └── __init__.py
├── templates/                     # HTML templates (Flask Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── groups.html
│   ├── create-group.html
│   ├── group-details.html
│   ├── group-feedback.html
│   ├── join-group.html
│   ├── students.html
│   └── student-info.html
├── static/                        # Static files
│   └── styles.css                # Main stylesheet
└── SQL\ Code/
    ├── Create_Table.sql          # Database schema
    └── Insert_data.sql           # Sample data
```

## Setup & Deployment

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Supabase account (https://supabase.com)
- PostgreSQL database (Supabase hosted)

### Installation Steps

1. **Clone/Download the project**
   ```bash
   cd Complete\ Demo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Supabase connection**
   - Create a `.env` file in the project root:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_api_key
   JWT_SECRET=your_jwt_secret_key
   ```

5. **Set up the database**
   - Log into your Supabase dashboard
   - Run the SQL scripts in this order:
     1. `SQL Code/Create_Table.sql` - Creates all tables
     2. `SQL Code/Insert_data.sql` - Populates sample data

6. **Run the application**
   ```bash
   python app.py
   ```
   The application will start on `http://localhost:5000`

### Deployment

For production deployment:

1. **Deploy to a web server** (Heroku, Render, AWS, etc.)
2. **Set environment variables** on your hosting platform
3. **Use Gunicorn** for production WSGI:
   ```bash
   gunicorn app:app
   ```

## Features

### Authentication & Authorization
- User signup with NYU email validation
- Secure login with JWT tokens
- Password hashing with bcrypt
- Role-based access (admin/student)

### Group Management
- Create new study groups
- Browse active and expired groups
- Join existing groups
- View group details and members

### User Profiles
- Update personal information
- Manage course enrollment
- Set availability times
- Change password

### Feedback System
- Rate study groups (1-10 scale)
- Leave comments on group experiences
- View feedback from other members

### Search & Discovery
- Search students by name or email
- Filter groups by status
- Browse available courses

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login

### Public Data
- `GET /` - List all courses
- `GET /groups` - Get all meetings
- `GET /courses` - List courses

### Protected Endpoints (require JWT token)
- `GET /profile` - Get user profile
- `PATCH /profile` - Update profile
- `GET /dashboard` - Get dashboard data
- `POST /create-group` - Create new meeting
- `GET /group-feedback` - Get feedback for a meeting
- `POST /group-feedback` - Submit feedback

## Technology Stack

- **Backend**: Flask, Python
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: JWT (PyJWT), Bcrypt
- **Frontend**: HTML5, CSS3, JavaScript (fetch API)
- **Deployment**: Flask development server (Gunicorn for production)

## Security Features

### Database Level
- Foreign key constraints
- Role-based access control setup ready
- Data validation and constraints

### Application Level
- JWT token-based authentication
- Password hashing with bcrypt
- Email validation (@nyu.edu)
- Input sanitization
- CORS protection
- Bearer token verification

## Sample Credentials

The sample data includes test users:
- Email: `ab1001@nyu.edu` (Admin)
- Email: `ab1002@nyu.edu` through `ab1015@nyu.edu` (Students)

All sample passwords are hashed. Update them in the database for testing.

## Advanced SQL Features Used

1. **Foreign Key Relationships**: Enforce referential integrity
2. **Composite Primary Keys**: Meeting_Request and Feedback tables
3. **Joins**: Complex queries across related tables
4. **Aggregate Functions**: Count, average feedback ratings
5. **Date/Time Functions**: Meeting scheduling and filtering

## Future Enhancements

- Video call integration
- Email notifications
- Real-time chat
- File upload and sharing
- Advanced scheduling with calendar
- Mobile app development
- Analytics dashboard
- Export data as CSV/JSON

## Support & Troubleshooting

### Common Issues

**"Module not found" error**
- Ensure Python path includes the backend directory
- Check virtual environment is activated
- Verify `sys.path.insert(0, ...)` in app.py

**Database connection issues**
- Verify `.env` file has correct Supabase credentials
- Check network access to Supabase
- Ensure PostgreSQL tables are created

**JWT token issues**
- Tokens expire after 7 days
- Clear localStorage and re-login
- Verify JWT_SECRET is set consistently

## Authors & Credits

Developed as a semester-long database project for NYU Tandon School of Engineering.

## License

For educational purposes.

## Environment Variables

```
SUPABASE_URL         # Your Supabase project URL
SUPABASE_KEY         # Your Supabase API key
JWT_SECRET           # Secret key for JWT signing (default: "dev-secret")
```

---

**Note**: Replace placeholder credentials with your actual Supabase credentials before deployment.
