from django.db import connection
from django.db.utils import DatabaseError
from django.utils import timezone


class HealthRepository:

    def get_timestamp(
        self,
    ) -> str:
        return timezone.now().isoformat()

    def is_database_online(
        self,
    ) -> bool:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1",
                )
                cursor.fetchone()

            return True

        except DatabaseError:
            return False