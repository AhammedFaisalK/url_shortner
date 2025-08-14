# URL Shortener Backend (Django + DRF + Docker)

This is a **Django REST Framework** backend service for a URL Shortener, containerized with **Docker**.

---

## 🚀 Quick Start (Single Command)

Make sure Docker is installed, then run:

```bash
docker-compose up --build
```

This will:

1. Build the Docker image
2. Install dependencies from `requirements.txt`
3. Run database migrations
4. Collect static files
5. Start the development server at **http://localhost:8000**

---

## 🛠 Useful Commands

### Run Django Management Commands

```bash
docker-compose exec web python manage.py <command>
```

Example:

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 📜 Requirements

- Python 3.11
- Django 5.2.5
- Django REST Framework
- django-cors-headers
- validators

---

## 📂 Project Structure

```
URL_SHORTENER/
│
├── shortener/          # Main Django app
│   ├── api/            # API views
│   ├── migrations/     # DB migrations
│
├── url_shortener/      # Project settings
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── manage.py
```
