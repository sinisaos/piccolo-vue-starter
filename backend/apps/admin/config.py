from piccolo_admin.endpoints import create_admin

from apps.tasks.tables import Task

ADMIN = create_admin(
    tables=[Task],
)
