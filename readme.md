   ## 3MONKEYS – Property Booking & Holiday Planning Backend API

Welcome to the backend API for **3MONKEYS**, a powerful platform that enables users to book holiday properties like resorts, farmhouses, service apartments, and trips. This backend is built using **Django REST Framework** and designed to handle vendors, customers, secure bookings, and advanced features like wishlist, reviews, and availability management.


## FEATURES

-  JWT Authentication (Login / Register)
-  Role-based access (Vendor & Customer)
-  Property Listing and Filtering
-  Availability Calendar for Bookings
-  Booking System with Price Calculation
-  Wishlist Functionality
-  Customer Reviews
-  File/Image Uploads
-  Admin & Vendor Dashboards (customizable)
-  Scalable and API-ready Architecture


## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Auth**: JWT (using `djangorestframework-simplejwt`)
- **Image Handling**: Django ImageField (local)
- **Deployment**: Render


## Project Structure

monkeysdata/
├── projectmonkeys/          # Main Django project settings
│   └── __init__.py
│   └── settings.py
│   └── urls.py
│   └── wsgi.py / asgi.py
│
├── app3monkeys/             # Core application logic
│   ├── __init__.py
│   ├── admin.py             # Admin panel configurations
│   ├── apps.py
│   ├── models.py            # Models: User, Property, Booking, etc.
│   ├── permissions.py       # Custom permissions for roles
│   ├── serializers.py       # Serializers for API data handling
│   ├── urls.py              # App-level URL patterns
│   ├── utils.py             # Utility functions (e.g., OTP, helpers)
│   ├── views.py             # API views and logic
│   └── migrations/          # Django model migrations
│
├── media/                   # Uploaded media (e.g., images)
├── .env                     # Environment variables
├── .gitignore
├── manage.py                # Django management script
├── procfile                 # Render deployment config
├── readme.md
├── render.yaml              # Render platform build & deploy settings
└── requirements.txt         # Python dependencies


## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Lora-BabyPrabha/projectmonkeys.git
   cd app3monkeys

2. **Create & Activate a Virtual Environment**
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt

4. **Set Up PostgreSQL Database**
   Create a PostgreSQL database (postgres3monkeys)
   Update DATABASES in settings.py and .env (Put external url in settings.py or .env)
    
5. **Apply Migrations**
   python manage.py makemigrations
   python manage.py migrate
   
6. **Run Server**
   python manage.py runserver

 
## authentication-related APIs

The following authentication-related APIs are fully implemented and tested:

1. **Register API**
Endpoint: /api/register/
Fields: 'username', 'email', 'password', 'role'
Method: POST
Description: Allows a new user to register as a customer or vendor.

2. **Login API**
Endpoint: /api/token/
Fields: 'username', 'password'
Method: POST
Description: Returns JWT access and refresh tokens after validating user credentials.

3. **Forgot Password API**
Endpoint: /api/send-otp/
Endpoint: /api/New-password/
Method: POST
Fields: 'Email' (For send-otp)
        'Email', 'OTP', 'New Password', 'Confirm Password' (For New-Password)
Description: Sends an OTP to the registered email address to initiate password reset.
             Verifies OTP and allows the user to set a new password.

4. **Reset Password API**
Endpoint: /api/new-password/
Method: POST
Fields: 'Old Password', 'New Password', 'Confirm Password'
Description: Verifies Old Password and allows the user to reset a new password.


## Deployment Guide

This section outlines the deployment process for the 3MONKEYS backend using Render and PostgreSQL.  

**Requirements**
Python ≥ 3.9
Django ≥ 4.0
PostgreSQL (Cloud DB or Render-managed)
Render Account (https://render.com)
GitHub Repository (Code must be pushed here)

**Deployment Setup**
 - Push Code to GitHub
 - Ensure backend project is versioned and pushed to a public or private GitHub repository.
 - Go to Render → Dashboard
 - Create a PostgreSQL database
 - Note down:
   DB Name, User, Password, Host, Port
 - Configure Django Settings
   In settings.py update Database details
   ALLOWED_HOSTS = ['*']
   DEBUG = False
   Set Up Static & Media Files (Optional but recommended for production)

**Deploy on Render**
 - Create a New Web Service
 - Select: "New Web Service"
 - Choose the GitHub repo
 - Environment: Python 3
 - Build Command: pip install -r requirements.txt
 - Start Command: gunicorn projectmonkeys.wsgi:application
 - Add Environment Variables from .env
 - Then Deploy

**Post Deployment**
Test all major API endpoints (/api/register/, /api/token/, etc.)



