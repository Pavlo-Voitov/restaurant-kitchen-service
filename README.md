"# restaurant-kitchen-service" 

A Django web application for managing dishes, dish types, ingredients, and cooks in a restaurant kitchen.
This project demonstrates CRUD operations, user authentication, search & filter, formsets, pagination, and unit testing.

---

## Features

### Core Functionality

- User login/logout
- Manage dishes (Create / Read / Update / Delete)
- Manage dish types
- Manage ingredients
- Assign cook to dishes
- Add ingredients to dishes using formsets
- Search & filtering for dishes by name, type, and cook
- Pagination
- Sidebar filters

### Testing

- Unit tests for models
- CRUD tests for views
- Filter tests
- Permissions tests

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default Django)
- **Frontend:** Bootstrap 4
- **Forms:** Django Crispy Forms
- **Tests:** Django Test Framework

---

## Project Structure

```text
restaurant-kitchen-service/
├─ kitchen/ # main Django app
│ ├─ migrations/
│ ├─ templates/ # HTML templates
│ ├─ tests/ # test modules
│ ├─ models.py
│ ├─ views.py
│ ├─ urls.py
│ └─ ...
├─ restaurant_kitchen_service/
├─ static/
├─ templates/
├─ manage.py
└─ README.md
```

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/Pavlo-Voitov/restaurant-kitchen-service.git
cd restaurant-kitchen-service
```

2. Create and activate a Python virtual environment

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Apply migrations

python manage.py migrate

5. Create a superuser

python manage.py createsuperuser

6. Run the development server

python manage.py runserver

Running Tests: 
To run all unit tests: python manage.py test

## Screenshots

### Dish List: 
![img.png](screenshots/img.png)

### Dish detail: 
![img_1.png](screenshots/img_1.png)


Author

Pavlo Voitov
Junior Python / Django Developer

GitHub: https://github.com/Pavlo-Voitov

Available at primary URL : https://restaurant-kitchen-service-akh3.onrender.com

Username: test_user
Password: 12345test
