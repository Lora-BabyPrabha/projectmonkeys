                 3MONKEYS – Property Booking & Holiday Planning Backend API

Welcome to the backend API for I**3MONKEYS**, a powerful platform that enables users to book holiday properties like resorts, farmhouses, service apartments, and trips. This backend is built using **Django REST Framework** and designed to handle vendors, customers, secure bookings, and advanced features like wishlist, reviews, and availability management.


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

3monkeys/
├── projectmonkeys/ # Django Project
├── app3monkeys/ # Main App 
│ ├── models.py # Models (User, Property, Booking, etc.)
│ ├── views.py # Viewsets & API Logic
│ ├── serializers.py # Serializers for each model
│ ├── urls.py # App URLs
├── media/ # Uploaded media (images)
├── requirements.txt 
└── manage.py


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


