# StreamFolio

StreamFolio is a Django-based streaming watch-history dashboard.

It tracks what users watched, where they watched it, how they reacted, ratings, notes, recommendations, mood, genre, and watch-later items.

## Current Features

- Django backend
- Django Admin
- Django REST Framework API
- SQLite local development database
- Custom user model
- Watch history model
- Homepage dashboard
- Add watch item form
- Search and filter dashboard
- Ratings
- Reactions
- Notes
- Mood
- Genre
- Watch Later tracking
- Would Recommend tracking
- Recommended By field
- Delete watch item button
- JWT token endpoints
- Static CSS file for dashboard styling

## Local Development Commands

Go to the project folder:

    cd C:\Users\GE310\streamfolio

Install requirements:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

Create superuser:

    python manage.py createsuperuser

Start server:

    python manage.py runserver

## Local URLs

Homepage:

    http://127.0.0.1:8000/

Admin:

    http://127.0.0.1:8000/admin/

Watch History API:

    http://127.0.0.1:8000/api/watch-history/

Users API:

    http://127.0.0.1:8000/api/users/

JWT Token Login:

    http://127.0.0.1:8000/api/token/

JWT Token Refresh:

    http://127.0.0.1:8000/api/token/refresh/

## API Endpoints

- /api/users/
- /api/watch-history/
- /api/token/
- /api/token/refresh/

## Tech Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- SQLite for local development
- PostgreSQL-ready for production
- WhiteNoise for static files
- GitHub for version control

## Project Status

Local MVP backend is running.

The dashboard currently supports adding, deleting, searching, filtering, and viewing watch-history records.

## Next Planned Upgrades

- Add edit/update watch history
- Add watch later page
- Add recommendations page
- Add user-specific dashboards
- Add external streaming API integrations
- Prepare production deployment
