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
fastapi run main.py
```

### Step 5. Optional: Run via Docker Compose
```
docker compose up --build -d
```

### Step 6. Optional: Load test data
If running locally (with Poetry):
Use the provided test_data.sql script to populate the database:
```
psql -h localhost -U your_db_user -d your_db_name -f test_data.sql
```
If running via Docker Compose:
Test data will be loaded automatically on first launch thanks to the mounted init script.
```
db:
  volumes:
    - ./test_data.sql:/docker-entrypoint-initdb.d/test_data.sql
```