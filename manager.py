import re as re
import json as json
import csv as csv
import os
import statistics
from collections import defaultdict
from collections import OrderedDict
from typing import Dict, List, Union

class Database:
    def __init__(self, file_path: str = None, file_type: str='json'): 
        """
        Initializes a new instance of the Database class.

            Parameters:
            - `file_path`: the path to the file to load data from (default `None`)
            - `file_type`: the type of file (default `'json'`)
            """
        self.database: List[Dict] = list()
        self.file_path: str = file_path
        self.file_type: str = file_type.lower()
        if self.file_type not in ('json','csv'):
            raise ValueError("Invalid file type")
        if self.file_path:
            if os.path.exists(self.file_path):
                self.load()
            else:
                raise ValueError("The file does not exist")

    # Loading methods

    def load(self) -> None:
        """
        Loads data from the file specified in file_path.
        """
        if not self.file_path:
            return
        if self.file_type == 'json':
            self.load_json(self.file_path)
        elif self.file_type == 'csv':
            self.load_csv(self.file_path)
        else:
            raise ValueError(f"Error: Invalid option {self.file_type}")

    def load_json(self, file_path: str) -> None:
        """
        Loads data from a JSON file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_contents = file.read()
        except IOError as e:
            raise ValueError(f'Error opening file: {e}')
        if len(file_contents) < 1:
            return
        try:
            self.database = json.loads(file_contents)
            self.file_path = file_path
        except ValueError as e:
            raise ValueError(f'Error reading file as JSON: {e}')

    def load_csv(self, file_path: str) -> None:
        """
        Loads data from a CSV file.
        """
        try:
            with open(file_path, 'r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.database.append(row)
            self.file_path = file_path
        except IOError as e:
            raise ValueError(f'Error opening file: {e}')

    # Search methods

    def find(self, criteria: Dict, logic: str = 'AND') -> List[Dict]:
        """
        Returns a list of items in the database that match the specified criteria.

        The criteria is a dictionary where the keys are field names and the values are the values to match.
        The logic parameter specifies the boolean operator to use when matching the criteria.
        Valid values for logic are 'AND', 'OR', and 'NOT'.
        """
        def matches(item: Dict) -> bool:
            if logic == 'AND':
                return all(item.get(k) == v for k, v in criteria.items())
            elif logic == 'OR':
                return any(item.get(k) == v for k, v in criteria.items())
            elif logic == 'NOT':
                return not any(item.get(k) == v for k, v in criteria.items())
            else:
                raise ValueError("Invalid logic")
        return [item for item in self.database if matches(item)]

    def find_one(self, key: str, value) -> Union[Dict, None]:
        """
        Returns the first item in database where the value of key is value.
        """
        return next((item for item in self.database if item.get(key) == value), None)

    def find_many(self, key: str, value) -> List[Dict]:
        """
        Returns a list of items in database where the value of key is value.
        """
        return [item for item in self.database if item.get(key) == value]

    def find_regex(self, field: str, regex: str) -> List[Dict]:
        """
        Returns a list of items in database where the value of field matches the regular expression regex.
        """
        return [item for item in self.database if re.match(regex, item.get(field))]

    def create_index(self, field: str) -> None:
        """
        Creates an index for the specified field in the database.

        The index is a dictionary where the keys are the values of the field
        and the values are the items in the database with that value.
        """
        self.indexes = {field: {item[field]: item for item in self.database}}

    def find_one_indexed(self, field: str, value) -> Union[None, dict]:
        """
        Returns the first item in the database where the value of the indexed field is value.

        If no index exists for the field, or no item is found, returns None.
        """
        if field in self.indexes:
            return self.indexes[field].get(value)
        return None

    def find_many_indexed(self, field: str, value) -> List[dict]:
        """
        Returns a list of items in the database where the value of the indexed field is value.

        If no index exists for the field, returns an empty list.
        """
        if field in self.indexes:
            return [item for item in self.indexes[field].values() if item[field] == value]
        return []

    def get_fields(self) -> List[str]:
        """
        Returns a list of the field names in the database.
        """
        if not self.database:
            return []
        return list(self.database[0].keys())

    # Editing methods

    def insert_one(self, item: Dict) -> None:
        """
        Inserts a single item into database.
        """
        self.database.append(item)

    def insert_many(self, items: List[Dict]) -> None:
        """
        Inserts a list of items into database.
        """
        self.database.extend(items)

    def update_one(self, key: str, value, new_values: Dict) -> None:
        """
        Updates the first item in database where the value of key is value with the key-value pairs in new_values.
        """
        item = self.find_one(key, value)
        if item:
            item.update(new_values)

    def update_many(self, criteria: Dict, new_values: Dict) -> None:
        """
        Updates all items in database that match the key-value pairs in criteria with the key-value pairs in new_values.
        """
        items = self.find(criteria)
        for item in items:
            item.update(new_values)

    def delete_one(self, key: str, value) -> None:
        """
        Deletes the first item in database where the value of key is value.
        """
        item = self.find_one(key, value)
        if item:
            self.database.remove(item)

    def delete_many(self, criteria: Dict) -> None:
        """
        Deletes all items in database that match the key-value pairs in criteria.
        """
        items = self.find(criteria)
        for item in items:
            self.database.remove(item)

    def delete_all(self) -> None:
        """
        Deletes all items in database.
        """
        self.database = list()

    def add_field(self, field: str, default_value=None) -> None:
        """
        Adds a field with the specified default value to all items in the database.
        """
        for item in self.database:
            item[field] = default_value

    def remove_field(self, field: str) -> None:
        """
        Removes the specified field from all items in the database.
        """
        for item in self.database:
            if field in item:
                del item[field]

    # Visualization methods

    def get_database_as_table(self) -> str:
        """
        Returns a string representation of the database as a table.

        The table has a header row with the field names, a separator row,
        and one row for each item in the database.
        """
        table_rows = list()
        # Add header row
        table_rows.append(' | '.join(self.database[0].keys()))
        # Add separator row
        table_rows.append(' | '.join(['---'] * len(self.database[0])))
        # Add data rows
        for item in self.database:
            table_rows.append(' | '.join(str(v) for v in item.values()))
        return '\n'.join(table_rows)

    def count(self) -> int:
        """
        Returns the number of items in database.
        """
        return len(self.database)

    def paginate(self, page_size: int, page_number: int) -> List[Dict]:
        """
        Returns a list of items from the database, paginated by the specified page size and page number.
        """
        start = (page_number - 1) * page_size
        end = start + page_size
        return self.database[start:end]

    # Treatment methods

    def sort_by_size(self, field: str, reverse: bool = False) -> List:
        """
        Sorts the database by the size of the specified field.

        Parameters:
            field (str): The name of the field to sort by.

        Returns:
            A list of the items in the database, sorted by the size of the specified field.
        """
        if isinstance(self.database[0][field], (str, list)):
            return sorted(self.database, key=lambda item: item[field], reverse=reverse)
        elif isinstance(self.database[0][field], (int, float)):
            return sorted(self.database, key=lambda item: item[field], reverse=reverse)
        else:
            raise TypeError("The field must be a string, a list, or an integer.")

    def sort_by_multiple_fields(self, fields: List[str], reverse: bool = False) -> List:
        """
        Sorts the database by the specified fields.

        Parameters:
            fields (List[str]): The list of field names to sort by.
            reverse (bool): Whether to sort the database in reverse order. Defaults to False.

        Returns:
            A list of the items in the database, sorted by the specified fields.
        """
        return sorted(self.database, key=lambda item: [item[field] for field in fields], reverse=reverse)

    def min(self, field: str) -> Union[int, float]:
        """
        Returns the minimum value of the specified field.
        """
        return min(item[field] for item in self.database)

    def max(self, field: str) -> Union[int, float]:
        """
        Returns the maximum value of the specified field.
        """
        return max(item[field] for item in self.database)

    def sum(self, field: str) -> Union[int, float]:
        """
        Returns the sum of the values of the specified field.
        """
        return sum(item[field] for item in self.database)

    def stddev(self, field: str) -> float:
        """
        Returns the standard deviation of the values of the specified field.
        """
        return statistics.stdev(item[field] for item in self.database)

    def avg(self, field: str) -> float:
        """
        Returns the average value of the specified field.
        """
        return statistics.mean(item[field] for item in self.database)
 
    def median(self, field: str) -> float:
        """
        Returns the median of the values of the specified field.
        """
        return statistics.median(item[field] for item in self.database)

    def mode(self, field: str) -> Union[int, float]:
        """
        Returns the mode of the values of the specified field.
        """
        return statistics.mode(item[field] for item in self.database)

    def distinct(self, field: str) -> List:
        """
        Returns a list of the distinct values for the specified field.
        """
        return list(set(item[field] for item in self.database))

    def transform(self, field: str, transformation_function: str) -> None:
        """
        Applies a transformation function to the specified field in all items in the database.

        Valid transformation functions are 'uppercase', 'lowercase', 'float', 'integer', and 'string'.
        """
        for item in self.database:
            if field in item:
                value = item[field]
                if transformation_function == 'uppercase':
                    value = value.upper()
                elif transformation_function == 'lowercase':
                    value = value.lower()
                elif transformation_function == 'float':
                    value = float(value)
                elif transformation_function == 'integer':
                    value = int(value)
                elif transformation_function == 'string':
                    value = str(value)
                else:
                    raise ValueError("Invalid transformation function")
                item[field] = value

    def validate(self, item: dict, constraints: dict) -> bool:
        """
        Validates an item by checking that its field values match the specified constraints.

        Returns True if the item is valid, False otherwise.
        """
        for field, value in constraints.items():
            if item.get(field) != value:
                return False
        return True

    def field_exists(self, field: str) -> bool:
        """
        Returns True if the specified field exists in at least one item in the database, False otherwise.
        """
        return any(field in item for item in self.database)

    # Export methods

    def to_json(self, file_path: str) -> None:
        """
        Saves the database to a JSON file at the specified file path.
        """
        if len(self.database) == 0:
            with open(file_path, 'w') as file:
                file.write('')
            return

        with open(file_path, 'w+b') as file:
            file.write(json.dumps(self.database, indent=4).encode('utf-8'))

    def to_csv(self, file_path: str) -> None:
        """
        Saves the database to a CSV file at the specified file path.
        """
        if len(self.database) == 0:
            with open(file_path, 'w') as file:
                file.write('')
            return

        with open(file_path, 'w', newline='') as csv_file:
            fieldnames = list(self.database[0].keys())
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.database:
                writer.writerow(item)

    def save(self) -> None:
        """
        Saves the current data to the file specified in file_path.
        """
        if not self.file_path:
            return

        if self.file_type == 'json':
            self.to_json(self.file_path)
        elif self.file_type == 'csv':
            self.to_csv(self.file_path)
        else:
            raise ValueError(f"Error: Invalid option {self.file_type}")