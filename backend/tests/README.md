# Testing

Set a test database in `piccolo_conf_test.py`.

```python
from piccolo_conf import *  # noqa
from settings import DB_HOST, TEST_DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DB = PostgresEngine(
    config={
        "database": TEST_DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }
)
```
Running tests from root directory.

```
piccolo tester run
```