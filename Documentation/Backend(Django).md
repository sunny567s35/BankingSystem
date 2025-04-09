# ⚙️ BankingSystem – Backend Code Structure & Explanation

This markdown provides a detailed explanation of the backend structure of the **BankingSystem** Django project. It breaks down the roles of core files in the `app/`, `BankingSystem/`, and `Custom_admin/` directories, and explains how Celery is configured for asynchronous tasks.

---

## 📁 1. app/

### `views.py` – Summary of Views

| **View Name**               | **Description**                                                                 |
|----------------------------|---------------------------------------------------------------------------------|
| `home`                     | Loads the homepage showing announcements and general information.              |
| `register`                 | Handles new user registration and sends a welcome email.                       |
| `login`                    | Authenticates users and logs the login timestamp.                              |
| `password_reset`           | Sends reset link or OTP for secure password changes.                           |
| `dashboard`                | Displays the user's account summary, recent transactions, and notifications.   |
| `user_logout`              | Logs out users and logs the logout event.                                      |
| `my_profile`               | Allows users to view and update their personal profile.                        |
| `withdraw`                 | Handles withdrawal operations, ensures sufficient balance, updates logs.       |
| `validate_account`         | Validates the target account before processing a transfer.                     |
| `transfer`                 | Transfers funds between two accounts and creates transaction records.          |
| `interest`                 | Shows interest earned or applied based on account type.                        |
| `statement`                | Displays a user's transaction history.                                         |
| `deposit`                  | Allows customers to deposit money and logs the transaction.                    |
| `interest_summary`         | Summarizes interest rates and earnings for various account types.              |
| `send_otp`                 | Sends a one-time password for secure operations.                               |
| `verify_balance_password`  | Double-verifies password before executing critical tasks.                      |
| `download_statement_pdf`   | Generates and allows download of PDF bank statements.                          |
| `about`                    | Loads the about page explaining the bank or app.                               |
| `setting`                  | User preferences and configurations like email/notification settings.          |
| `send_transaction_email`   | Background utility to send transaction email notifications.                    |
| `send_registration_email`  | Sends a welcome email upon registration.                                       |

---

## 📁 2. BankingSystem/

### `settings.py` ⚙️

- Configures Django project including:
  - Installed apps
  - Middleware stack
  - Static and media file handling
  - MySQL database setup
  - Celery integration using Redis
  - Email backend for OTPs and alerts
  - Defines project-wide constants and timezone/language settings.

### `urls.py`

- Maps the base URLs of the project.
- Includes:
  - `app.urls` for user routes
  - `Custom_admin.urls` for custom admin panel
  - Handles media and static file routing in development.

### `celery.py`

- Initializes Celery application and binds it with Django settings.
- Enables background job discovery from all installed apps.

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BankingSystem.settings')
app = Celery('BankingSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

## 📄 Other Key Files

- **`__init__.py`**: Imports Celery app to run when Django starts.
- **`wsgi.py`**: Entry point for WSGI servers (e.g., Gunicorn) for deployment.
- **`asgi.py`**: Used for async deployments and WebSockets (e.g., via Daphne/Uvicorn).

---

## 📁 3. Custom_admin/

Other than `views.py`, `admin.py`, and `templates/`, these files include:

- **`models.py`**:  
  May contain additional admin-specific models such as logs, metadata, or system controls.

- **`forms.py`**:  
  Custom forms to enhance admin UX with validation, styling, or extra logic.

- **`urls.py`**:  
  Maps custom admin dashboard and features.

- **`static/`**:  
  Custom styles and scripts for an enhanced admin UI/UX.

- **`utils.py`** _(if present)_:  
  Admin helper functions or formatting utilities.

---

## 🔁 4. Celery Integration

### `celery.py` (in `BankingSystem/`)

- Sets up Celery app and binds Django configuration.
- Uses Redis for broker and result backend.

---

### `tasks.py` (in `app/`)

Contains reusable asynchronous tasks like:

- Sending OTPs
- Triggering emails
- Interest recalculation
- Statement generation in background

```python
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, message, recipient_list):
    send_mail(subject, message, 'noreply@bankingsystem.com', recipient_list)
```

