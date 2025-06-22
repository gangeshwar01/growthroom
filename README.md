# Growth Room

Growth Room is a dedicated digital space created to nurture, guide, and accelerate the personal and professional development of interns, team members, and collaborators.

## Features

- Employee Portal System
- Training & Development Management
- Task & Project Management
- Performance Tracking
- Certificate Management
- Attendance Management
- Work & Attendance Tracking
- Training & Development Schedule
- Task & Project Updates
- Performance & Progress Tracking
- Certification Management
- Support & Contact System

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `growthroom/` - Main project directory
- `accounts/` - User authentication and profile management
- `attendance/` - Work and attendance tracking
- `training/` - Training schedules and resources
- `tasks/` - Task and project management
- `performance/` - Performance tracking and evaluation
- `certificates/` - Certificate management system
- `employee_portal/` - Employee portal for self-service

## Contributing

Please read our contributing guidelines before submitting pull requests.

## License

This project is proprietary and confidential. 