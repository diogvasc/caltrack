# CalTrack

CalTrack is a Django web application for tracking daily food intake, meals, hydration, and nutrition goals.

## Features

- Food category management (`CategoriAlimento`)
- Food catalog with nutrition per 100g (`Alimento`)
- Daily log entries (`RegistoDiario`)
- Meal records linked to a day (`Refeicao`)
- Meal items with quantity in grams (`RefeicaoAlimento`)
- User nutrition goals (`Objetivo`)
- Dashboard with daily totals:
  - calories
  - protein
  - carbs
  - fat
  - remaining calories vs target
- Image upload support for foods

## Tech Stack

- Python
- Django 5
- PostgreSQL
- python-dotenv
- Pillow (for image fields)

## Project Structure

```text
caltrack/
├── manage.py
├── caltrack/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── workshop/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/workshop/
└── media/
    └── alimentos/
```

## Prerequisites

- Python 3.10+
- PostgreSQL running locally or remotely

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd caltrack
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install django psycopg2-binary python-dotenv pillow
```

4. Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_NAME=caltrack
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

5. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. (Optional) Create an admin user:

```bash
python manage.py createsuperuser
```

7. Start the development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Main Routes

- `/` - Dashboard (daily summary)
- `/categorias/` - Food categories
- `/alimentos/` - Foods
- `/registos/` - Daily logs
- `/refeicoes/` - Meals
- `/objetivos/` - Goals
- `/admin/` - Django admin

## Data Model Overview

- `CategoriAlimento` -> has many `Alimento`
- `RegistoDiario` -> has many `Refeicao`
- `Refeicao` -> has many `RefeicaoAlimento`
- `RefeicaoAlimento` -> links `Refeicao` and `Alimento` with quantity
- `Objetivo` -> belongs to a Django `User`

## Notes

- The app currently uses generic class-based views for list/create/delete flows.
- The dashboard picks the most recent active goal and compares it with today's intake.
- Media files are served via Django in development.

## Future Improvements

- Add authentication-restricted views per user
- Add update/detail pages for all entities
- Add automated tests for views and calculations
- Add requirements file and Docker setup

## License

No license file is included yet. If this repository is public, consider adding a license (for example MIT).
