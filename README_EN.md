# Maziyar Shop | مازیار شاپ

Maziyar Shop — A full-featured e-commerce web application built with Django

## Overview

Maziyar Shop is an online store with complete features including product management, shopping cart, review & rating system, newsletter, admin panel, and dark/light theme.

## Features

### Users
- Sign up and login
- Change username and password
- User profile
- Rate and review products (logged-in users only)

### Products
- Display products with images, prices, ratings, and descriptions
- Filter by category, price, rating, and sorting
- Product search
- Sale/discount display

### Shopping Cart
- Add to cart (AJAX)
- Change product quantity
- Remove items from cart

### Admin Panel
- Dashboard with overall stats (products, categories, users, reviews)
- Product management (add, edit, delete)
- Category management
- User management (activate/deactivate, delete)
- Comment management (show/hide, delete)
- Advanced product filters in admin panel

### Design
- Responsive (mobile and desktop compatible)
- Dark and light theme
- Vazirmatn Persian font
- Bootstrap Icons
- Bootstrap 5 framework

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 5.0 |
| Database | SQLite (development) / PostgreSQL (production) |
| Frontend | Bootstrap 5, jQuery |
| Font | Vazirmatn |
| Icons | Bootstrap Icons |
| Static Files | WhiteNoise |
| Server | Gunicorn |

## Installation

### Prerequisites
- Python 3.11+
- pip

### Setup Steps

```bash
# Clone the project
git clone https://github.com/Thrymheim/Maziyar-shop.git
cd Maziyar-shop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Site is available at `http://127.0.0.1:8000`

## Project Structure

```
Maziyar-shop/
├── maziyar_shop/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                  # Main shop application
│   ├── models.py          # Models (Product, Category, Comment, Newsletter)
│   ├── views.py           # Views
│   ├── urls.py            # URLs
│   ├── forms.py           # Forms
│   ├── admin.py           # Django admin
│   └── templates/         # Templates
│       ├── base.html
│       ├── navbar.html
│       ├── index.html
│       ├── product.html
│       ├── profile.html
│       ├── contact.html
│       └── admin_panel/   # Admin panel templates
├── cart/                  # Shopping cart application
│   ├── cart.py
│   ├── views.py
│   └── context_processors.py
├── static/                # Static files
│   ├── css/
│   ├── js/
│   ├── fonts/
│   └── assets/
├── media/                 # Uploaded files
├── requirements.txt
├── runtime.txt
├── build.sh
└── manage.py
```

## Models

### Product
- name, discription, price, category, picture, star
- is_sale, sale_price

### Category
- name

### Comment
- product, user, rating (1-5), body, created_at, is_active

### Newsletter
- email, created_at, is_active

### Order
- product, customer, quantity, address, phone, date, status

## Admin Panel Access

Only users with `is_staff=True` have access to the admin panel.

## Author

**Maziyar Kolagari** — [@Thrymheim](https://github.com/Thrymheim)
