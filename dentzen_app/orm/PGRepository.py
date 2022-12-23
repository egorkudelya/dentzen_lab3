from django.db import connection

from .QueryBuilder import QueryBuilder

def value_to_db(val):
  return (
    'NULL' if val is None
    else f'{val}' if isinstance(val, int)
    else f"'{val}'"
  )

class PGRepository:
  def __init__(self, model):
    self.model = model
    self.table_name = model._meta.__dict__['db_table']

  def query(self, alias=None):
    return QueryBuilder(self.table_name if alias is None else f'{self.table_name} as {alias}')

  def find(self):
    with connection.cursor() as cursor:
      cursor.execute(f"SELECT COALESCE(json_agg({self.table_name}), '[]'::json) FROM {self.table_name}")

      return cursor.fetchone()[0]

  def get(self, id):
    with connection.cursor() as cursor:
      cursor.execute(f"SELECT json_agg({self.table_name}) FROM {self.table_name} WHERE id = {id}")
      found_obj, = cursor.fetchone()
      return found_obj[0] if found_obj else None

  def create(self, data):
    fields = [
      field
      for field in self.model._meta.get_fields()
      if (
        field.concrete
        and not field.primary_key
        and field.column
      )
    ]

    columns = ', '.join(
      field.column  if field.is_relation
      else field.name
      for field in fields
    )
    values = ', '.join(value_to_db(data.get(field.name, field.get_default())) for field in fields)

    with connection.cursor() as cursor:
      cursor.execute(f"INSERT INTO {self.table_name} ({columns}) VALUES ({values}) RETURNING row_to_json({self.table_name});")

      return cursor.fetchone()[0]

  def patch(self, id, data):
    old_data = self.get(id)
    if old_data is None: return None

    updated_data = {
      key: value
      for key, value in data.items()
      if old_data.get(key, not value) != value
    }

    update_str = ', '.join(
      f"{key} = {value_to_db(value)}"
      for key, value in updated_data.items()
    )

    with connection.cursor() as cursor:
      cursor.execute(f"UPDATE {self.table_name} SET {update_str} WHERE id={id} RETURNING row_to_json({self.table_name});")

      return cursor.fetchone()[0]


  def delete(self, id):
    with connection.cursor() as cursor:
      cursor.execute(f"WITH deleted AS (DELETE FROM {self.table_name} WHERE id={id} RETURNING *) SELECT count(*) FROM deleted;")

      deleted_count, = cursor.fetchone()

      return deleted_count > 0
