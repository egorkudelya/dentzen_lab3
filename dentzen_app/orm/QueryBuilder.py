from django.db import connection

class QueryBuilder:
  def __init__(self, table_name):
    self.select_data = []
    self.where_data = []
    self.group_by_data = []
    self.order_by_data = []
    self.having_data = []
    self.join_data = []
    self.limit_data = None
    self.table_name = table_name

  def select(self, *args):
    self.select_data.extend(args)
    return self

  def where(self, query):
    self.where_data.extend(['AND', query] if len(self.where_data) else [query])
    return self

  def and_where(self, query):
    self.where_data.extend(['AND', query] if len(self.where_data) else [query])
    return self

  def or_where(self, query):
    self.where_data.extend(['OR', query] if len(self.where_data) else [query])
    return self

  def group_by(self, *args):
    self.group_by_data.extend(args)
    return self

  def order_by(self, *args):
    self.order_by_data.extend(args)
    return self

  def having(self, query):
    self.having_data.extend(['AND', query] if len(self.having_data) else [query])
    return self

  def and_having(self, query):
    self.having_data.extend(['AND', query] if len(self.having_data) else [query])
    return self

  def or_having(self, query):
    self.having_data.extend(['OR', query] if len(self.having_data) else [query])
    return self

  def limit(self, n):
    self.limit_data = n
    return self

  def join(self, table_name, query, join_type=''):
    self.join_data.append({ table_name: table_name, join_type: join_type, query: query })
    return self

  def sql(self):
    join_block = ' '.join(
      map(
        lambda join_statement:
          f"{join_statement.join_type} JOIN {join_statement.table_name} ON {join_statement.query}",
        self.join_data
      )
    )

    return (
        f'''SELECT {','.join(self.select_data)} ''' +
        f'''FROM {self.table_name} ''' +
        f'''{join_block} ''' +
        f'''{f"WHERE {' '.join(self.where_data)}" if len(self.where_data) else ""} ''' +
        f'''{f"GROUP BY {','.join(self.group_by_data)}" if len(self.group_by_data) else ""} ''' +
        f'''{f"HAVING {' '.join(self.having_data)}" if len(self.having_data) else ""} ''' +
        f'''{f"ORDER BY {','.join(self.order_by_data)}" if len(self.order_by_data) else ""} ''' +
        f'''{f"Limit {self.limit_data}" if self.limit_data else ""}'''
      )

  def execute(self, one=False):
    with connection.cursor() as cursor:
      cursor.execute(self.sql())

      return cursor.fetchone() if one else cursor.fetchall()
