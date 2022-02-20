Open terminal and run:

```shell
virtualenv -p python3 envname
cd envname
source bin/activate
git clone https://github.com/sinisaos/piccolo-vue-starter.git
cd piccolo-vue-starter/backend
pip install -r requirements.txt
sudo -i -u yourpostgresusername psql
CREATE DATABASE yourdb;
\q
touch .env
## put this in .env file
## DB_NAME="your db name"
## TEST_DB_NAME="your test db name"
## DB_USER="your db username"
## DB_PASSWORD="your db password"
## DB_HOST="your db host"
## DB_PORT=5432
## SECRET_KEY="your secret key"

## runing migrations for admin
piccolo migrations forwards user
piccolo migrations forwards session_auth
## runing migrations for site
piccolo migrations forwards home
## create admin user
piccolo user create
python main.py
```
After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/) or
API docs [localhost:8000/docs/](http://localhost:8000/docs/).


