"""
authentication.py

Este módulo define las vistas y funciones relacionadas con la autenticación de usuarios 
en el sistema, así como el decorador personalizado `@login_required` para proteger 
vistas que requieren sesión activa.

Funcionalidades incluidas:
- Inicio de sesión (login)
- Cierre de sesión (logout_view)
- Validación de sesión (is_authenticated)
- Decorador login_required para restringir acceso a usuarios no autenticados
- Vista principal (index) protegida por sesión

Se utiliza el modelo Employee para autenticar al usuario con su número de identificación
y contraseña, y se almacenan datos clave en la sesión de Django.
"""


from django.shortcuts import render, redirect
from django.contrib import messages
from TechSolutionsApp.models import Employee

def is_authenticated(request):
    '''
    Función para verificar si el usuario está autenticado
    ''' 
    return request.session.get('employee_id') is not None


def login_required(view_func):
    '''
    Decorador para proteger vistas que requieren autorización
    ''' 
    def wrapper(request, *args, **kwargs):
        # si el usuario no está autenticado, lo redirige al login
        if not is_authenticated(request):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def index(request):
    '''
    Función para renderizar el index
    ''' 
    return render(request, 'index.html')


def login(request):
    '''
    Función para manejar el inicio de sesión
    ''' 
    if request.method == 'POST':
        id_number = request.POST['username']
        password = request.POST['password']
        try:
            # busca el empleado por número de identificación
            user = Employee.objects.get(idNumber=id_number)
            if user.check_password(password):
                # Si es correcto, guarda datos del usuario en la sesión
                request.session['employee_id'] = user.employeeId
                request.session['id_number'] = user.idNumber
                request.session['role_id'] = user.role.roleId
                request.session['name'] = f"{user.firstName} {user.lastName}"
                
                return redirect('home')
            else:
                messages.error(request, "Contraseña incorrecta")
        except Employee.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
    # Si no es POST o hubo errores, muestra el formulario de login
    return render(request, 'login.html')


def logout_view(request):
    '''
    Función para cerrar sesión
    ''' 
    
    # Elimina todos los datos de la sesión
    request.session.flush()  
    return redirect('login')
