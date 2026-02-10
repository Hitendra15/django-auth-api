# Authentication System API

REST API for user registration and JWT-based authentication.

## Features
- User registration
- Login using JWT
- Access & refresh tokens

## Tech Stack
- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL / SQLite

## API Endpoints
POST   /gettoken/                       # for generating jwttoken  
POST   /verifytoken/                    # for verifying jwttoken  
POST   /refreshtoken/                   # for refreshing jwttoken  
POST   /accounts/registration/          # for creating a user 
GET    /accounts/registration/          # for displaying all users
PUT    /accounts/registration/userid/   # for updating user
DELETE /accounts/registration/userid/   # for deleting a user

## Setup
1. git clone repo
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py runserver
