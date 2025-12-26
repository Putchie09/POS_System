# Proyecto TechSolutions
TechSolutions es un sistema web de gestión interna desarrollado con Django, diseñado para facilitar el manejo de empleados, inventario, ventas y usuarios dentro de una empresa de tecnología. El sistema incluye control de accesos, interfaz de administración, reportes y un entorno gráfico amigable.


# Funcionalidades principales:
- Gestionar roles de usuario (administrador y empleado).
- Controlar acceso según el rol asignado.
- Registrar, editar y eliminar empleados.
- Registrar, editar y eliminar clientes.
- Registrar y consultar ventas.


## Requisitos:
- Python 3.10 o superior
- Servidor MySQL
- pip


## Instalación y ejecución:
1. descomprimir el proyecto.
2. Crear una base de datos en MySQL (nombre: 'TechSolutionsDB')
3. Configurar las credenciales de la base de datos en `settings.py`:
4. (Opcional) modificar las credenciales del super usuario en el archivo create_superuser.py
    - datos por defecto: usuario: admin, contraseña: admin123
5. Ejecutar el archivo 'installer.bat'
6. En el navegador web abrir http://127.0.0.1:8000/
 - El puerto del punto 6 puede variar

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
Tomar en cuenta que la contrasena, el host y el puerto pueden variar dependiendo del servidor