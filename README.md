# Handbook Service (test task)

## Install and setup
Poetry is used as package managment system. You can find it and installation guide at [Poetry official site](https://python-poetry.org/docs/)

### Step 1. Initializing poetry
Installing from poetry is pretty simple. Just type
```
poetry install
```
at the project directory

### Step 2. Create configuration
Create file `config.yaml` in project directory and fill it as it shown in `config.yaml.example`


### Step 3. Initialize alembic
Create PostgreSQL database and apply migrations
```
alembic upgrade head
```

### Step 4. Launch the application
```
uvicorn main:app
```

### Step 5. Optional: Run via Docker Compose
```
docker compose up --build -d
```

### Step 6. Optional: Load test data
Use the provided test_data.sql script to populate the database:  
If running locally (with Poetry):
```
psql -h localhost -U your_db_user -d handbook_service -f test_data.sql
```
If running via Docker Compose:
```
docker exec -i database psql -U your_db_user -d handbook_service < test_data.sql
```
