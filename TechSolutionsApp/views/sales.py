from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from TechSolutionsApp.models import Sale, SaleDetail, Customer, Product, Inventory, Employee
from TechSolutionsApp.views.authentication import login_required
from django.db.models import Q
from django.utils import timezone
from django.db import IntegrityError


'''
SALES SECTION
views related to sales functionality
'''

@login_required
def add_sale(request):
    '''
    Vista para registrar una nueva venta, incluyendo creación de cliente si es necesario 
    '''
    # Inicializar datos del cliente
    customer_data = {
        'customer_name': '',
        'customer_last_name': '',
        'customer_id': '',
        'customer_email': '',
        'discount': '0'
    }

    if request.method == 'GET' and 'q' in request.GET:
        _load_customer_data_for_search(request, customer_data)

    elif request.method == 'POST':
        _save_data_to_session(request, customer_data)

        if not _has_at_least_one_product(request, Product.objects.all()):
            messages.error(request, "Debe agregar al menos un producto a la venta")
            return redirect('add_sale')

        customer = _process_customer_data(request)
        if not customer:
            return redirect('add_sale')   

        if _register_sale(request, customer):
            messages.success(request, "Venta registrada exitosamente")
            request.session.pop('sale_form_data', None)
            return redirect('add_sale')

    return _render_add_sale_form(request, customer_data)

def _load_customer_data_for_search(request, customer_data):
    session_data = request.session.get('sale_form_data', {})
    customer_data.update(session_data)

    for key in customer_data.keys():
        if key in request.GET:
            customer_data[key] = request.GET.get(key)

def _save_data_to_session(request, customer_data):
    for key in customer_data.keys():
        if key in request.POST:
            customer_data[key] = request.POST.get(key)
    request.session['sale_form_data'] = customer_data

def _register_sale(request, customer):
    try:
        sale = Sale.objects.create(
            customer=customer,
            user=Employee.objects.get(employeeId=request.session.get('employee_id')),
            saleDate=timezone.now(),
            discountPercentage=request.POST.get('discount', 0)
        )

        _create_sale_details(request, sale, Product.objects.all())
        return True

    except Exception as e:
        messages.error(request, f"Error al procesar la venta: {str(e)}")
        return False

# Procesa los datos del cliente desde el formulario, crea o actualiza el cliente si es necesario
def _process_customer_data(request):
    first_name = request.POST.get('customer_name', '').strip()
    last_name = request.POST.get('customer_last_name', '').strip()
    
    id_number = request.POST.get('customer_id', '').strip()
    if not id_number.isdigit() or len(id_number) != 9:
        messages.error(request, "La cédula debe contener solo números y tener 9 dígitos.")
        return None
    
    email = request.POST.get('customer_email', '').strip().lower()

    if not all([first_name, last_name, id_number]):
        messages.error(request, "Nombre, apellido e identificación son obligatorios")
        return None

    existing_customer = Customer.objects.filter(idNumber=id_number).first()
    
    if existing_customer:
        # Verificar coincidencia de datos
        if (request.POST.get('customer_name', '').strip().lower() != existing_customer.firstName.lower() or
            request.POST.get('customer_last_name', '').strip().lower() != existing_customer.lastName.lower()):
            
            messages.error(
                request,
                f"Error: La cédula {id_number} pertenece a {existing_customer.firstName} {existing_customer.lastName}. "
                "Por favor ingrese los datos correctos o use otra cédula."
            )
            return None

    try:      
        customer = Customer.objects.filter(idNumber=id_number).first() # Buscar cliente por cédula
        
        if customer:
            # Cliente existe, verificar y actualizar email si es diferente y no está vacío
            if email and email != customer.email:
                # Verifica si el nuevo email no existe en otro cliente
                if Customer.objects.filter(email=email).exclude(idNumber=id_number).exists():
                    messages.error(request, "El correo electrónico ya está registrado para otro cliente")
                    return None
                
                customer.email = email
                customer.save()
                messages.info(request, "Correo electrónico del cliente actualizado")
            return customer
        else:
            # Crea nuevo cliente
            customer_data = {
                'firstName': first_name,
                'lastName': last_name,
                'idNumber': id_number,
                'email': email if email else None  
            }

            if email and Customer.objects.filter(email=email).exists():
                messages.error(request, "El correo electrónico ya está registrado")
                return None
                
            customer = Customer.objects.create(**customer_data)
            messages.success(request, "Nuevo cliente registrado exitosamente")
            return customer

    except IntegrityError as e:
        messages.error(request, "Error al registrar el cliente: La cédula ya existe")
        return None
    except Exception as e:
        messages.error(request, f"Error al procesar cliente: {str(e)}")
        return None


def _has_at_least_one_product(request, products):
    '''
    Verifica que se haya seleccionado al menos un producto con cantidad mayor a cero
    '''
    for product in products:
        quantity = request.POST.get(f'quantity_{product.productId}')
        if quantity and int(quantity) > 0:
            return True
    return False


def _create_sale_details(request, sale, products):
    '''
    Crea los detalles de venta y actualiza el inventario
    '''
    for product in products:
        quantity = request.POST.get(f'quantity_{product.productId}')
        if quantity and int(quantity) > 0:
            quantity = int(quantity)

            SaleDetail.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unitPrice=product.price
            )

            inventory = Inventory.objects.filter(product=product).first()
            if inventory:
                if inventory.productQuantity >= quantity:
                    inventory.productQuantity -= quantity
                    inventory.save()
                else:
                    messages.error(request, f"No hay suficiente inventario para {product.name}")


def _render_add_sale_form(request, customer_data):
    """
    Renderiza la vista del formulario de agregar venta con productos filtrados
    """
    query = request.GET.get('q', '')
    
    # Solo se muestran productos activos
    products = Product.objects.filter(status=True)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))

    filtered_products = []
    for product in products:
        inventory = Inventory.objects.filter(product=product).first()
        stock = inventory.productQuantity if inventory else 0
        if stock > 0:
            product.stock = stock
            filtered_products.append(product)

    return render(request, 'sales/add_sale.html', {
        'products': filtered_products,
        'query': query,
        'customer_data': customer_data
    })


@login_required
def view_sales(request):
    '''
    Muestra la lista de ventas registradas con subtotal, descuento y total calculado
    '''
    sales = Sale.objects.all().order_by('-saleDate').prefetch_related('saledetail_set', 'user', 'customer')
    role = request.session.get('role_id')
    
    for sale in sales:
        sale.subtotal = sum(detail.quantity * detail.unitPrice for detail in sale.saledetail_set.all())
        discount = sale.subtotal * (sale.discountPercentage / 100)
        sale.total = sale.subtotal - discount
    return render(request, 'sales/view_sales.html', {
        'sales': sales,
        'role': role
        })


@login_required
def edit_sale(request, id):
    '''
    Edita una venta existente, validando que las nuevas cantidades no superen el inventario
    ''' 
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')

    sale = get_object_or_404(Sale, saleId=id)
    customers = Customer.objects.all()
    details = SaleDetail.objects.filter(sale=sale)

    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        discount = request.POST.get('discount') or 0

        sale.customer = get_object_or_404(Customer, customerId=customer_id)
        sale.discountPercentage = discount
        sale.save()

        if _update_sale_details(request, details):
            return redirect('edit_sale', id=id)

        messages.success(request, "Venta actualizada exitosamente")
        return redirect('view_sales')

    return render(request, 'sales/edit_sale.html', {
        'sale': sale,
        'customers': customers,
        'details': details,
    })


def _update_sale_details(request, details):
    '''
    Valida y actualiza cada detalle de la venta, considerando el inventario.
    Retorna True si hubo algún error.
    '''
    error_occurred = False

    for detail in details:
        quantity_str = request.POST.get(f'quantity_{detail.product.productId}')
        if quantity_str:
            try:
                new_quantity = int(quantity_str)

                if new_quantity <= 0:
                    messages.error(request, f'La cantidad de {detail.product.name} debe ser mayor a cero.')
                    error_occurred = True
                    continue

                inventory = Inventory.objects.get(product=detail.product)
                available_stock = inventory.productQuantity + detail.quantity

                if new_quantity > available_stock:
                    messages.error(
                        request,
                        f'No hay suficiente inventario para {detail.product.name}. '
                        f'Disponible: {available_stock}, solicitado: {new_quantity}'
                    )
                    error_occurred = True
                    continue

                inventory.productQuantity = available_stock - new_quantity
                inventory.save()

                detail.quantity = new_quantity
                detail.save()

            except ValueError:
                messages.error(request, f'Cantidad inválida para {detail.product.name}')
                error_occurred = True

    return error_occurred

@login_required
def delete_sale(request, id):
    '''
    Elimina una venta del sistema
    ''' 
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    sale = get_object_or_404(Sale, saleId=id)

    if request.method == 'POST':
        sale.delete()

    messages.success(request, "Venta eliminada exitosamente")
    return redirect('view_sales')
