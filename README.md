# Banking System using Django

### This is a simple banking system implemented using Django, allowing users to create accounts, perform transactions, and manage their finances.

## Features

- **User Authentication:** Users can create accounts, log in, and log out securely.
- **Account Management:** Users can view their account details, including balance and transaction history.
- **Transaction Handling:** Allows users to transfer money between accounts and view transaction logs
- **Admin Panel:** Admins have access to manage users, accounts, and transactions.

## Installation

### 1 Clone the repository:

```bash
git clone https://github.com/
cd banking-system
```

### 2 Create a virtual environment:

```bash
python -m venv myenv
source myenv/bin/activate  # For Unix/Linux
myenv\Scripts\activate  # For Windows
```

### 3 Install dependencies:

```bash
pip install -r requirements.txt
```

### 4 Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5 Create a superuser (admin):

```bash
python manage.py createsuperuser

```

### 6 Start the development server:

```bash
python manage.py runserver


```

### 7 Access the application at http://localhost:8000.

## Usage:

- Visit http://localhost:8000/admin and log in with the superuser credentials to access the admin panel.
- Regular users can sign up for accounts, log in, view account details, perform transactions, and log out.

## Technologies Used

- Django
- Python
- HTML/CSS (Bootstrap for styling)
- SQLite (for development, can be swapped with other databases for production)
