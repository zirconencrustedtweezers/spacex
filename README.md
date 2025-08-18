# BiometrIQ SpaceX App 🚀

A simple web application that demonstrates FastAPI serving a Vue.js frontend with PostgreSQL database setup.

## Features

- **FastAPI Backend**: Serves both API endpoints and static files
- **Minimal Vue 3 Frontend**: Single HTML file with Bulma CSS - no build process!
- **PostgreSQL Database**: Ready for future SpaceX data storage
- **Docker Compose**: Easy development environment setup

## Quick Start

### Prerequisites

- Docker and Docker Compose only!

### Development Setup

1. **Clone and navigate to the project:**
   ```bash
   cd biometriq
   ```

2. **Start everything:**
   ```bash
   docker-compose up
   ```
   This will start:
   - PostgreSQL database on port 5432
   - FastAPI backend on port 8000
   - Vue app served at http://localhost:8000

3. **That's it!** No npm, no build process, no configuration files!

### Current Functionality

- **GET /api/user**: Returns user information (John Doe)
- **Vue Frontend**: Displays "Hello [firstName] [lastName]" fetched from the API
- **PostgreSQL**: Database ready for future SpaceX data storage

## Project Structure

```
biometriq/
├── docker-compose.yml          # Multi-service setup
├── backend/
│   ├── Dockerfile
│   ├── app.py                  # FastAPI application
│   ├── requirements.txt
│   └── static/
│       └── index.html          # Single Vue app file (that's it!)
└── README.md
```

## Development Workflow

1. **Backend changes**: Edit files in `backend/`, Docker will auto-reload
2. **Frontend changes**: Edit `backend/static/index.html`, refresh browser - done!

## Database Connection

The PostgreSQL database is accessible at:
- Host: localhost
- Port: 5432
- Database: biometriq
- Username: admin
- Password: password

## API Endpoints

- `GET /api/user` - Returns user information
- `GET /` - Serves Vue.js application (if built)
- `GET /docs` - FastAPI interactive documentation

## Next Steps

This setup is ready for expanding with:
- SpaceX API integration
- Rocket and launch data storage
- Crew member management
- Additional Vue components and pages
