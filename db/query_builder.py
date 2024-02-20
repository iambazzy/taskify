class QueryBuilder:
    @staticmethod
    def build_select_query(table_name, condition):
        return f"SELECT * FROM {table_name} WHERE {condition}"
