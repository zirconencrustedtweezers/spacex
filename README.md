# BiometrIQ SpaceX App 🚀

## Frontend
- Vue.js with Axios and Vite

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
```bash
docker-compose up -d
```
This automatically runs database migrations on build.

## Development
```bash
cd frontend
npm run dev
```
