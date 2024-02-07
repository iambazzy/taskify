# Taskify

<i> Taskify is your go-to solution for effortless and efficient task management. Seamlessly integrated into your daily workflow, Taskify empowers you to create, organize, and track your tasks with unparalleled ease. </i>


**Python:** Taskify leverages the power of Python for its backend, ensuring a reliable and scalable foundation.

**Flask Framework:** Built on the Flask web framework, Taskify delivers a lightweight and flexible structure for creating web applications, making it an ideal choice for task management.

**PostgreSQL Database:** Taskify relies on the PostgreSQL database for robust data storage and retrieval. The use of PostgreSQL ensures data integrity and reliability.

**Without ORM:** Taskify manages its database operations without the use of an Object-Relational Mapping (ORM) system. Instead, it employs custom SQL queries for direct interaction with the PostgreSQL database for more control over the db queries.


## Endpoints

### 1. Register User

#### Endpoint: `/auth/register`
- Method: `POST`

**Request:**
```json
{
  "firstname": "John",
  "lastname": "Doe",
  "email": "john.doe@example.com",
  "password": "secure_password"
}
```

### 2. Login

### Endpoint: `/auth/login`
- Method: `POST`

**Request:**
```json
{
  "email": "john.doe@example.com",
  "password": "secure_password"
}
```

### 3. Reset Password

### Endpoint: `/auth/reset-password`
- Methods: `POST` (Initiate reset)

**POST Request:**
```json
{
  "email": "john.doe@example.com"
}
```

### 4. Update Password

### Endpoint: `/auth/reset-password`
- Methods: `PUT` (Complete reset)

**PUT Request:**
```json
{
    "token": "the_token",
    "password": "honey1234"
}
```
