"""
employees.py

Este módulo contiene las vistas relacionadas con la gestión de empleados del sistema.

Funciones principales:
- Ver empleados
- Agregar empleados
- Editar empleados
- Eliminar empleados
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from TechSolutionsApp.models import Employee, Role
from django.db.models import ProtectedError
from TechSolutionsApp.views.authentication import login_required


@login_required
def view_employees(request):
    '''
    Función para ver los empleados, los carga en view_employees.html
    '''
    role = request.session.get('role_id')

    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    employees = Employee.objects.all()

    return render(request, 'employees/view_employees.html', {'employees': employees,'role': role})


@login_required
def add_employee(request):
    '''
    Función para agregar un empleado/usuario
    '''  
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        idNumber = request.POST.get('idNumber')
        phoneNumber = request.POST.get('phoneNumber')
        role = get_object_or_404(Role, pk=2) # id 2 corresponde a user
        password = request.POST.get('password').strip()

        errors = []

        # validar contrasenna 
        if not password:
            errors.append("La contraseña no puede estar vacía")
        elif len(password) < 6:
            errors.append("La contraseña debe tener al menos 6 caracteres")

        # validar identificación
        if  not idNumber.isdigit():
            errors.append("La identificación debe contener solo números")
        elif len(idNumber) != 9:
            errors.append("La identificación debe tener exactamente 9 dígitos")
        
        # validar número
        if  not phoneNumber.isdigit():
            errors.append("El número de télefono debe contener solo números")
        elif len(phoneNumber) != 8:
            errors.append("El número de telefono solo debe tener exactamente 8 dígitos")

        # Validar unicidad
        if Employee.objects.filter(idNumber=idNumber).exists():
            errors.append("Ya existe un empleado con esa identificación.")
        if Employee.objects.filter(phoneNumber=phoneNumber).exists():
            errors.append("Ya existe un empleado con ese número de teléfono.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'employees/add_employee.html')
        
        # Crear el empleado
        employee = Employee(
            firstName=firstName,
            lastName=lastName,
            idNumber=idNumber,
            phoneNumber=phoneNumber,
            role=role
        )
        # encriptar contrasenna
        employee.set_password(password)
        employee.save()
        messages.success(request, 'Empleado agregado correctamente.')
        return redirect('view_employees')

    roles = Role.objects.all()
    return render(request, 'employees/add_employee.html', {'roles': roles})


@login_required
def edit_employee(request, id):
    '''
    Función para editar un empleado
    '''

    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    employee = get_object_or_404(Employee, pk=id)

    if request.method == 'POST':
        firstName = request.POST.get('firstName', '').strip()
        lastName = request.POST.get('lastName', '').strip()
        idNumber = request.POST.get('idNumber', '').strip()
        phoneNumber = request.POST.get('phoneNumber', '').strip()
        current_password = request.POST.get('currentPassword', '').strip()
        new_password = request.POST.get('newPassword', '').strip()

        errors = []

        if not idNumber.isdigit() or len(idNumber) != 9:
            errors.append("La cédula debe tener exactamente 9 dígitos y deben ser enteros positivos.")

        if not phoneNumber.isdigit() or len(phoneNumber) != 8:
            errors.append("El teléfono debe tener exactamente 8 dígitos y deben ser enteros positivos.")

        # Validación de contraseña (solo si se quiere cambiar)
        if current_password or new_password:
            if not employee.check_password(current_password):
                errors.append("La contraseña actual es incorrecta.")
            elif len(new_password) < 6:
                errors.append("La nueva contraseña debe tener al menos 6 caracteres.")

        # Validar datos duplicados
        if Employee.objects.filter(idNumber=idNumber).exclude(pk=employee.pk).exists():
            errors.append("Ya existe otro empleado con esa identificación.")

        if Employee.objects.filter(phoneNumber=phoneNumber).exclude(pk=employee.pk).exists():
            errors.append("Ya existe otro empleado con ese número de teléfono.")


        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'employees/edit_employee.html', {'employee': employee})

        employee.firstName = firstName
        employee.lastName = lastName
        employee.idNumber = idNumber
        employee.phoneNumber = phoneNumber
        
        # Cambiar contraseña si se indicó
        if current_password and new_password:
            employee.set_password(new_password)
        
        employee.save()
        messages.success(request, 'Empleado actualizado correctamente.')
        return redirect('view_employees')

    return render(request, 'employees/edit_employee.html', {'employee': employee})


@login_required
def delete_employee(request, id):
    '''
    Elimina un empleado del sistema
    '''
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    employee = get_object_or_404(Employee, pk=id)

    if employee.role.roleId == 1:
        messages.error(request, "No se puede eliminar un usuario con rol Administrador")
        return redirect('view_employees')
    try:
        employee.delete()
        messages.success(request, "Empleado eliminado correctamente.")
    except ProtectedError:
        messages.error(
            request,
            "No se puede eliminar este empleado porque tiene ventas registradas."
        )
    except Exception as e:
        messages.error(request, 'Ocurrió un error inesperado al eliminar el empleado.')
    return redirect("view_employees")

