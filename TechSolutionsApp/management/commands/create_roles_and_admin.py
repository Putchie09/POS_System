from django.core.management.base import BaseCommand
from TechSolutionsApp.models import Role, Employee  
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    # Descripción del comando que aparece en la ayuda
    help = 'Crea los roles Admin y User, y un empleado administrador si no existen.'

    # Método principal que se ejecuta al correr el comando
    def handle(self, *args, **kwargs):
        '''
        Crea los roles "Admin" y "User" si no existen en la base de datos.
        Además, genera un empleado administrador con una cédula predeterminada
        si no hay uno registrado.
        '''

        # Crear rol Admin si no existe
        admin_role, created_admin = Role.objects.get_or_create(
            roleId=1, defaults={'description': 'Admin'}
        )

        # Crear rol User si no existe
        user_role, created_user = Role.objects.get_or_create(
            roleId=2, defaults={'description': 'User'}
        )

        if created_admin:
            self.stdout.write(self.style.SUCCESS('Rol "Admin" creado'))
        else:
            self.stdout.write(self.style.WARNING('Rol "Admin" ya existe'))

        if created_user:
            self.stdout.write(self.style.SUCCESS('Rol "User" creado'))
        else:
            self.stdout.write(self.style.WARNING('Rol "User" ya existe'))

        # Verificar si existe un empleado administrador con cédula predeterminada
        id_number = '123456789'
        if not Employee.objects.filter(idNumber=id_number).exists():
            # Crear empleado administrador con contraseña encriptada
            admin = Employee.objects.create(
                firstName='Admin',
                lastName='User',
                idNumber=id_number,
                phoneNumber='88888888',
                role=admin_role,
                passwordHash=make_password('Admin123') 
            )
            self.stdout.write(self.style.SUCCESS(f'Empleado administrador creado: ID {admin.employeeId}'))
        else:
            self.stdout.write(self.style.WARNING(f'Ya existe un empleado con idNumber {id_number}'))
