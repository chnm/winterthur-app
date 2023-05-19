"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):

  def handle(self, *args, **options):
    self.stdout.write('Waiting for database...')
    db_conn = None
    while not db_conn:
      try:
        self.check(databases=['default'])
        connection.ensure_connection()
        db_conn = True
      except (Psycopg2OpError, OperationalError):
        self.stdout.write('Database unavailable, waiting 1 second...')
        time.sleep(1)

    self.stdout.write(self.style.SUCCESS('Database available!'))
