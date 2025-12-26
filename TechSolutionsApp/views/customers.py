"""
customers.py

Este módulo contiene las vistas relacionadas con la gestión de clientes del sistema.

Incluye funcionalidades para:
- Agregar nuevos clientes
- Visualizar la lista de clientes
- Editar información de clientes existentes
- Eliminar clientes, con validación de relaciones protegidas (ventas asociadas)

"""


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from TechSolutionsApp.models import Customer
from django.db.models import ProtectedError
from TechSolutionsApp.views.authentication import login_required
from django.db import IntegrityError


@login_required
def add_customer(request):
    '''
    Función para agregar un cliente
    '''
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        id_number = request.POST.get('id_number', '').strip()

        if not id_number.isdigit() or len(id_number) != 9:
            messages.error(request, "La cédula debe contener solo números y tener 9 dígitos.")
            return render(request, 'customers/add_customer.html')
        
        email = request.POST.get('email', '').strip()

        # Verifica los datos ingresados
        if not first_name or not last_name or not id_number:
            messages.error(request, "Todos los campos son obligatorios (correo opcional).")
        
        else: # si los datos son correctos, agrega el cliente
            try:
                Customer.objects.create(
                    firstName=first_name,
                    lastName=last_name,
                    idNumber=id_number,
                    email=email if email else None
                )
                messages.success(request, "Cliente agregado exitosamente.")
            except IntegrityError as e:
                if 'Duplicate entry' in str(e):
                    messages.error(request, "Ya existe un cliente con esa cédula.")
                else:
                    messages.error(request, "Ocurrió un error al guardar el cliente.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado: {str(e)}")

    return render(request, 'customers/add_customer.html')


@login_required
def view_customers(request):
    '''
    Función para ver los clientes, los carga en view_customers.html
    '''    
    customers = Customer.objects.all()
    return render(request, 'customers/view_customers.html', {'customers': customers})


@login_required
def delete_customer(request, id):
    '''
    Elimina un cliente del sistema 
    '''
    try:
        customer = get_object_or_404(Customer, pk=id)
        customer.delete()
        messages.success(request, 'El cliente se eliminó correctamente.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar el cliente porque tiene ventas asociadas.')
    except Exception as e:
        messages.error(request, 'Ocurrió un error inesperado al eliminar el cliente.')
    return redirect('view_customers')


@login_required
def edit_customer(request, id):
    '''
    Función para editar un cliente
    '''  
    customer = get_object_or_404(Customer, pk=id)
    
    if request.method == 'POST':
        customer.firstName = request.POST.get('firstName')
        customer.lastName = request.POST.get('lastName')
        
        
        email = request.POST.get('email', '').strip()
        if email.lower() == 'none':  
            email = ''  
        
        if email and '@' not in email:
            messages.error(request, "El correo electrónico debe contener un @")
            return render(request, 'customers/edit_customer.html', {'customer': customer})
        
        customer.email = email if email else None  # Guarda None si está vacío
        
        # Validación de cédula
        idNumber = request.POST.get('idNumber', '')
        if not idNumber.isdigit() or len(idNumber) != 9:
            messages.error(request, "La cédula debe contener solo números y tener 9 dígitos.")
            return render(request, 'customers/edit_customer.html', {'customer': customer})
        
        if Customer.objects.filter(idNumber=idNumber).exclude(pk=customer.pk).exists():
            messages.error(request, "Ya existe otro cliente con esa cédula.")
            return render(request, 'customers/edit_customer.html', {'customer': customer})
        
        
        customer.idNumber = idNumber
        customer.save()
        messages.success(request, 'El cliente se actualizó correctamente')
        return redirect('view_customers')

    return render(request, 'customers/edit_customer.html', {'customer': customer})