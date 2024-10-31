### Instalation

Clone repository in fresh virtualenv.

```bash
git clone https://github.com/sinisaos/piccolo-vue-starter.git
```

### Install requirements


```bash
cd backend
pip install -r requirements/requirements.txt
```

### Create database


```bash
sudo -i -u yourpostgresusername psql
CREATE DATABASE your_database_name;
\q;
```

### Setup
-------------------------------------------------------
Create ``.env`` file in root of the project.

```bash
DB_NAME=your_db_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
SECRET_KEY=your_secret_key
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Migrations

```bash
./scripts/migrations.sh
```

### Create admin user

```bash
./scripts/user.sh
```

### Testing

Install test requirements.

```bash
pip install -r requirements/test-requirements.txt
```

Run tests.

```bash
./scripts/test.sh
```

### Linting

```bash
./scripts/lint.sh
```

### Getting started 

```bash
./scripts/start.sh
```

After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/) or
API docs [localhost:8000/docs/](http://localhost:8000/docs/).
