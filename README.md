# Track-It - Video Learning Management System

A Flask-based video learning management system that allows admins to manage educational content and students to track their learning progress.

## Features

- **User Authentication**: Secure login and registration system
- **Role-based Access**: Admin and Student roles with different permissions
- **Video Management**: Upload and organize videos by subject
- **Progress Tracking**: Students can track their video watching progress
- **Learning Reports**: Generate study statistics and analytics
- **Responsive Design**: Modern, user-friendly interface

## Project Structure

```
TrackIt/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── create_test_users.py   # Script to create test users
├── static/
│   ├── css/
│   │   └── style.css      # Application styles
│   ├── js/
│   │   ├── main.js        # Main JavaScript
│   │   └── video_tracker.js # Video tracking logic
│   └── videos/            # Uploaded video storage
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── dashboard.html     # Student dashboard
│   ├── subjects.html      # Subjects list
│   ├── videos.html        # Videos for a subject
│   ├── player.html        # Video player
│   ├── reports.html       # Learning reports
│   └── admin.html         # Admin panel
├── database/
│   └── db.sqlite3         # SQLite database
└── venv/                  # Python virtual environment
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nandini599/Track-It.git
   cd Track-It
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install flask flask-sqlalchemy werkzeug
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

## Quick Login (Test Credentials)

The application comes with two pre-configured test users. Click the quick-login buttons on the login page:

### Admin Account
- **Email:** admin@gmail.com
- **Password:** 123456
- **Role:** Can manage subjects, upload videos, and view all users

### Student Account
- **Email:** student1@gmail.com
- **Password:** 123456
- **Role:** Can view subjects, watch videos, and track progress

## Usage

### For Administrators

1. **Login as Admin:**
   - Use the "Admin Login" button or manually enter admin credentials

2. **Manage Subjects:**
   - Go to Admin Panel (`/admin`)
   - Use "Create New Subject" form to add subject categories

3. **Upload Videos:**
   - Use "Upload Video" form to upload educational videos
   - Select the subject category
   - Choose the video file (max 500MB)

4. **View Users:**
   - See all registered users in the admin dashboard
   - Option to delete users if needed

### For Students

1. **Register/Login:**
   - Register with your email and password
   - Or use "Student Login" button for quick access

2. **Browse Videos:**
   - Navigate to Subjects to view all categories
   - Click on a subject to see available videos

3. **Watch Videos:**
   - Click on a video to open the player
   - Your progress is automatically tracked

4. **Track Progress:**
   - View your learning statistics on the dashboard
   - Check detailed reports on the Reports page

## Configuration

Key configurations in `app.py`:

- `SECRET_KEY`: Session encryption key (change in production)
- `DATABASE_URI`: SQLite database location
- `UPLOAD_FOLDER`: Video storage directory
- `MAX_CONTENT_LENGTH`: Maximum upload file size (500MB)

## Database Models

### User
- id, name, email, password_hash, role (admin/student)
- Relationships: progress

### Subject
- id, name
- Relationships: videos

### Video
- id, title, subject_id, file_path, duration
- Relationships: progress

### Progress
- id, user_id, video_id, watched_duration, completed
- Tracks student video viewing progress

## API Endpoints

### Public Routes
- `GET /` - Home page
- `GET/POST /login` - Login
- `GET/POST /signup` - Registration
- `GET /logout` - Logout

### Student Routes
- `GET /dashboard` - Student dashboard
- `GET /subjects` - List all subjects
- `GET /videos/<subject_id>` - Videos for subject
- `GET /player/<video_id>` - Video player
- `POST /progress/update` - Update watching progress
- `GET /reports` - Learning reports

### Admin Routes
- `GET /admin` - Admin dashboard
- `POST /admin/subject` - Create subject
- `POST /admin/upload` - Upload video
- `POST /admin/user/delete/<user_id>` - Delete user

## Technologies Used

- **Backend:** Flask, SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Security:** Werkzeug (password hashing)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Author

**Nandini** - [GitHub Profile](https://github.com/Nandini599)

---

**Last Updated:** April 2026
