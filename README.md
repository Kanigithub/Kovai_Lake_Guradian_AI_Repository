# Kovai Lake Guardians

A volunteer coordination platform for lake cleanup drives in Coimbatore, Tamil Nadu.
Built with Django 6.0.5 + Bootstrap 5.

## Features
- Volunteer registration (individual + NGO)
- Event management with QR codes
- Lake explorer with interactive map
- Organizer dashboard
- Check-in / Check-out time tracking (WorkLog)
- Leaderboard & Badges
- Announcements & Messages
- Bulk volunteer import from Excel / Microsoft Forms

## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Login Credentials (after seed_data)
- Organizer: `organizer` / `organizer123`
- Volunteer: `arun_kumar` / `volunteer123`
