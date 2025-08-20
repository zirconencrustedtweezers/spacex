# BiometrIQ SpaceX App 🚀

## Frontend
- Vue.js with Axios and Vite
- No separate container - build assets served statically by FastAPI

## Database
- PostgreSQL
- Host: localhost:25432
- Database: biometriq
- Username: admin
- Password: password

## Backend
- FastAPI with Alembic and psycopg2

## Script
- `scripts/seed_rockets.py` - Populates rocket data from SpaceX API

## Installation

1. **Build frontend first:**
```bash
cd frontend
npm run build
```

2. **Then start containers:**
```bash
docker-compose up -d
```
This automatically runs database migrations on build.

## Development
```bash
cd frontend
npm run dev
```
