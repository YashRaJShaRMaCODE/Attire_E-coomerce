# Attire E-commerce (Django)

A clean starter e-commerce web application built with Django, focused on essential storefront pages, account pages, contact/feedback capture, and admin visibility.

## ✨ Highlights

- Django-powered web app with a modular app structure (`basic` project + `home` app).
- Ready-made storefront and informational pages (Home, About, Services, Cart, etc.).
- Authentication flow with login/logout using Django auth.
- Contact and feedback forms persisted to the database.
- Admin panel configured and customized with branded titles.
- SQLite default setup for fast local development.

## 🧰 Tech Stack

- **Backend:** Django
- **Language:** Python 3
- **Database:** SQLite (default)
- **Templates:** Django templates (HTML)
- **Static assets:** Django static files via local `static/` directory

## 📁 Project Structure

```text
Attire_E-coomerce/
├── basic/                 # Django project config (settings, URLs, WSGI/ASGI)
├── home/                  # Main app (views, models, routes)
├── templates/             # Shared template files
├── static/                # Static files
├── db.sqlite3             # Local database (development)
└── manage.py              # Django CLI entrypoint
```

## 🚀 Quick Start

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd Attire_E-coomerce
```

### 2) Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\\Scripts\\activate    # Windows PowerShell
```

### 3) Install dependencies

```bash
pip install django
```

> If you add more dependencies, create a `requirements.txt` and install with `pip install -r requirements.txt`.

### 4) Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5) Create admin user (optional but recommended)

```bash
python manage.py createsuperuser
```

### 6) Run development server

```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## 🧭 Available Routes

| Route | Purpose |
|---|---|
| `/` | Home page |
| `/about/` | About page |
| `/services/` | Services page |
| `/contact/` | Contact form |
| `/feedback/` | Feedback form |
| `/login/` | User login |
| `/logout/` | User logout |
| `/cart/` | Shopping cart page |
| `/my-account/` | Account dashboard |
| `/my-account/my-orders/` | Orders page |
| `/my-account/settings/saved-addresses/` | Saved addresses |
| `/settings/` | General settings page |
| `/purchase-history/` | Purchase history |
| `/admin/` | Django admin |

## 🗃️ Data Models

### `Contact`
Stores contact messages submitted from the contact page.

Fields:
- `name`
- `email`
- `message`

### `Feedback`
Stores feedback submitted from the feedback page.

Fields:
- `name`
- `email`
- `message`

## 🔐 Authentication

- Login uses Django's built-in authentication (`authenticate`, `login`).
- Logout ends the session and redirects to the login page.
- Invalid login attempts show an error message through Django messages.

## 🛠️ Admin Configuration

Admin branding is customized in `basic/urls.py`:

- Site header: `UMSRA Admin`
- Site title: `UMSRA Admin Portal`
- Index title: `Welcome to UMSRA Researcher Portal`

## ⚠️ Notes / Known Gaps

- There are URL patterns for:
  - `/my-account/settings/profile-setting/`
  - `/my-account/settings/account-setting/`

  These currently render template names `profile_setting.html` and `account_setting.html` in views, while existing template files are named `profile_settings.html` and `account_settings.html`. If those routes are used, they should be aligned to avoid `TemplateDoesNotExist`.

- `DEBUG=True` and hardcoded secret key in `settings.py` are acceptable for local development but should be replaced for production.

## 📌 Recommended Next Improvements

1. Add `requirements.txt` with pinned versions.
2. Add `.env` support for secret key and debug configuration.
3. Add model-level timestamps (`created_at`) to `Contact` and `Feedback`.
4. Add unit tests for form submission and auth views.
5. Add CI (lint + tests) and deployment instructions.

## 🤝 Contributing

1. Fork and create a feature branch.
2. Keep commits focused and descriptive.
3. Run checks/tests locally before opening a PR.
4. Submit a PR with clear summary and screenshots for UI changes.

## 📄 License

Set a project license (MIT/Apache-2.0/etc.) and update this section.
