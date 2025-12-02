# Docker Setup

## Running the App

```bash
# Start everything
docker-compose up --build
```

App runs at http://localhost:5000

## First Time Only

The database starts empty. After containers are running, seed it:

```bash
docker-compose exec app python rebuild_db.py
```

## Useful Commands

```bash
# Run in background
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop everything
docker-compose down

# Reset database (deletes all data)
docker-compose down -v
```

## Notes

- PostgreSQL runs on port 5432
- Redis runs on port 6379
- Change SECRET_KEY in docker-compose.yml for production
