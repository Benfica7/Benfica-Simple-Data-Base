import json
import statistics
import csv
from collections import defaultdict

class Database:
    def __init__(self, file_path: str=None):
        self.database = list()
        self.file_path = file_path
        self.load()

    def load(self):
        if not self.file_path:
            return
        with open(self.file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        if len(file_contents) < 1:
            return
        self.database = json.loads(file_contents)

    def save(self):
        with open(self.file_path, 'w+b') as file:
            file.write(json.dumps(self.database, indent=4).encode('utf-8'))

    def find_one(self, key, value):
        return next((item for item in self.database if item.get(key) == value), None)

    def find_many(self, key, value):
        return [item for item in self.database if item.get(key) == value]

    def insert_one(self, item: dict):
        self.database.append(item)

    def insert_many(self, items: list):
        self.database.extend(items)

    def update_one(self, key, value, new_values: dict):
        item = self.find_one(key, value)
        if item:
            item.update(new_values)

    def update_many(self, criteria: dict, new_values: dict):
        items = self.find(criteria)
        for item in items:
            item.update(new_values)

    def delete_one(self, key, value):
        item = self.find_one(key, value)
        if item:
            self.database.remove(item)

    def delete_many(self, criteria: dict):
        items = self.find(criteria)
        for item in items:
            self.database.remove(item)

    def count(self):
        return len(self.database)

    def find(self, criteria: dict, logic: str = 'AND'):
        def matches(item):
            if logic == 'AND':
                return all(item.get(k) == v for k, v in criteria.items())
            elif logic == 'OR':
                return any(item.get(k) == v for k, v in criteria.items())
            elif logic == 'NOT':
                return not any(item.get(k) == v for k, v in criteria.items())
            else:
                raise ValueError("Invalid logic")
        return [item for item in self.database if matches(item)]

    def paginate(self, page_size: int, page_number: int):
            start = (page_number - 1) * page_size
            end = start + page_size
            return self.database[start:end]

    def backup(self, backup_file_path: str):
        with open(backup_file_path, 'w+b') as file:
            file.write(json.dumps(self.database, indent=4).encode('utf-8'))

    def min(self, field: str):
        values = [item[field] for item in self.database]
        return min(values)

    def max(self, field: str):
        values = [item[field] for item in self.database]
        return max(values)

    def sum(self, field: str):
        values = [item[field] for item in self.database]
        return sum(values)

    def average(self, field: str):
        values = [item[field] for item in self.database]
        return statistics.mean(values)

    def get_database_as_table(self) -> str:
        table_rows = []
        # Add header row
        table_rows.append(' | '.join(self.database[0].keys()))
        # Add separator row
        table_rows.append('-' * len(table_rows[0]))
        # Add data rows
        for item in self.database:
            table_rows.append(' | '.join(str(x) for x in item.values()))

        return '\n'.join(table_rows)

    def transform(self, field: str, transformation_function: str):
        for item in self.database:
            if field in item:
                if transformation_function == 'uppercase':
                    item[field] = item[field].upper()
                elif transformation_function == 'lowercase':
                    item[field] = item[field].lower()
                else:
                    raise ValueError("Invalid transformation function")

    def create_index(self, field: str):
        self.indexes = {field: {item[field]: item for item in self.database}}

    def find_one_indexed(self, field: str, value):
        if field in self.indexes:
            return self.indexes[field].get(value)
        return None

    def find_many_indexed(self, field: str, value):
        if field in self.indexes:
            return [item for item in self.indexes[field].values() if item[field] == value]
        return []

    def to_csv(self, file_path: str):
        with open(file_path, 'w', newline='') as csv_file:
            fieldnames = list(self.database[0].keys())
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.database:
                writer.writerow(item)

    def load_csv(self, file_path: str):
        with open(file_path, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.database.append(row)

    def add_field(self, field: str, default_value=None):
        for item in self.database:
            item[field] = default_value

    def remove_field(self, field: str):
        for item in self.database:
            if field in item:
                del item[field]

    def get_fields(self):
        if not self.database:
            return []
        return list(self.database[0].keys())

    def validate(self, item: dict, constraints: dict):
        for field, value in constraints.items():
            if item.get(field) != value:
                return False
        return True

    def field_exists(self, field: str):
        return any(field in item for item in self.database)

if __name__ == '__main__':
    database = Database('database.bsdl')
    database.load_csv('teste2.csv')
    print(database.get_database_as_table())