# Benfica-Simple-Data-Base
It is an in-memory database implementation that allows you to read, write and manipulate data in JSON and other formats. Provides several methods for performing common operations on a database.

# Goal

- Stay open source
- Be simple and intuitive
- Use as few external resources as possible

# Features

- Supports CSV and JSON
- Has tools to update, delete and edit databases
- Supports "medium" amounts of data
- Can be easily deployed to your project and does not depend on any additional features like a manager

# Instalation

### `Step 1`
Download the [latest version](https://github.com/Benfica7/Benfica-Simple-Data-Base/releases/)

### `Step 2`
In the same folder as the file use:

```python
pip instal bsdb-1.0.0.tar.gz --use-pep517
```
and it will be ready to use :)

# Documentation

To see the documentation [click here](https://github.com/Benfica7/Benfica-Simple-Data-Base/wiki)

# Why use BSDB?

**here are some advantages and disadvantages of BSDB compared to other databases:**

### SQLite

**✅ Benefits:**

- It does not require installation of an external database.
- Can be easily incorporated into a project as a Python library.
- Provides a simplified user interface for performing common operations on a database.
- It can be used to store small or medium data sets in memory.
- It can be easily modified or extended to meet the specific needs of a project.
- It does not require advanced knowledge of SQL or other database query language.

**❌ Disadvantages:**

- It is not suitable for handling large datasets due to in-memory storage.
- It is not suitable for use in production environments.
- Does not have some features.
- It may be less efficient in terms of performance compared to specialized database.

### MongoDB

**✅ Benefits:**

- It does not require installation of an external database.
- Can be easily incorporated into a project as a Python library.
- Provides a simplified user interface for performing common operations on a database.
- It can be used to store small or medium data sets in memory.
- It can be useful for prototyping or rapid testing.
- It can be easily modified or extended to meet the specific needs of a project.
- It does not require advanced knowledge of SQL or other database query language.

**❌ Disadvantages:**

- It is not suitable for handling large datasets due to in-memory storage.
- It is not suitable for use in production environments.
- Does not have some features.
- It may be less efficient in terms of performance compared to specialized database.

### FireBase

**✅ Benefits:**

- It does not require installation of an external database.
- Can be easily incorporated into a project as a Python library.
- Provides a simplified user interface for performing common operations on a database.
- It can be used to store small or medium data sets in memory.
- It can be useful for prototyping or rapid testing.
- It can be easily modified or extended to meet the specific needs of a project.
- It does not require advanced knowledge of SQL or other database query language.

**❌ Disadvantages:**

- It is not suitable for handling large datasets due to in-memory storage.
- It is not suitable for use in production environments.
- Does not have some features.
- It may be less efficient in terms of performance compared to specialized database.
- It does not offer the same advanced functionality as Firebase, such as user authentication, real-time notifications, and Google Cloud Platform integration.

# Summary

is an in-memory database implementation in Python that lets you read, write, and manipulate data primarily in JSON format, but can also work with other formats. It offers a variety of methods for performing common operations on a database, such as inserting, updating, removing, and finding items, as well as counting and dividing items into pages, and performing statistical calculations. However, it does not offer all the advanced functionality of a specialized database, and it is not suitable for handling large data sets or for use in production environments. Furthermore, it does not offer advanced security options such as user authentication and data encryption.

**General benefits**

- It can be used to simulate a database in a test or development environment, allowing you to test application code without relying on an external database.
- It can be easily integrated with other applications such as web services through the use of libraries such as Flask.
- Pode ser facilmente integrado com outras bibliotecas Python, como o Pandas, para realizar análises de dados avançadas.
- It can be used to work with data in CSV format, easily converting between internal JSON format and CSV format.
- Can be used to store data in JSON format which is widely used and easily human readable.
