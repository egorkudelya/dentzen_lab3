from django.db import connection
from .QueryBuilder import QueryBuilder

class DARepository:
  def __init__(self, model, serializer):
    self.model = model
    self.serializer = serializer
    self.table_name = model._meta.__dict__['db_table']

  def query(self):
    return QueryBuilder(self.table_name)

  def find(self):
    objects = self.model.objects.raw(f"SELECT * FROM {self.table_name}")
    return self.serializer(objects, many=True).data

  def get(self, id):
    found_obj = self.model.objects.raw(f"SELECT * FROM {self.table_name} WHERE id = {id}")
    return self.serializer(found_obj[0]).data if found_obj else None

  def create(self, data):
    columns = ', '.join(data.keys())
    values = ', '.join(f"'{val}'" for val in data.values())
    created_obj = self.model.objects.raw(f"INSERT INTO {self.table_name} ({columns}) VALUES ({values}) RETURNING *;")[0]
    return self.serializer(created_obj).data

  def patch(self, id, data):
    old_data = self.get(id)
    if old_data is None: return None

    updated_data = {
      key: value
      for key, value in data.items()
      if old_data.get(key, not value) != value
    }

    update_str = ', '.join(
      f"{key} = '{value}'"
      if isinstance(value, str)
      else f"{key} = {value}"
      for key, value in updated_data.items()
    )

    updated_obj = self.model.objects.raw(f"UPDATE {self.table_name} SET {update_str} WHERE id={id} RETURNING *;")[0]

    return self.serializer(updated_obj).data

  def delete(self, id):
    with connection.cursor() as cursor:
      cursor.execute(f"DELETE FROM {self.table_name} WHERE id={id}")
