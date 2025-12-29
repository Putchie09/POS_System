# TechSolutions Project

Internal web management system developed with Django, designed to facilitate the management of employees, inventory, sales, and users within a technology company. The system includes access control, an administration interface, reports, and a user-friendly graphical environment.

## Main Features:
- Manage user roles (administrator and employee).
- Control access based on the assigned role.
- Register, edit, and delete employees.
- Register, edit, and delete clients.
- Register and view sales.

## Requirements:
- Python 3.10 or higher
- MySQL Server
- pip

## Installation and Execution:
1. Unzip the project.
2. Create a database in MySQL (name: `TechSolutionsDB`).
3. Configure the database credentials in `settings.py`.
4. (Optional) Modify the superuser credentials in the `create_superuser.py` file.
   - Default credentials: username: `admin`, password: `admin123`
5. Run the `installer.bat` file.
6. Open http://127.0.0.1:8000/ in your web browser.
   - The port in step 6 may vary.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TechSolutionsDB',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Note that the password, host, and port may vary depending on the server configuration.
