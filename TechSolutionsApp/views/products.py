"""
products.py

Este módulo contiene las vistas relacionadas con la gestión de productos dentro del sistema,

Funciones incluidas:
- view_products: muestra todos los productos con filtros por nombre, SKU o categoría.
- add_product: permite agregar un nuevo producto y su cantidad inicial en inventario.
- edit_product: permite modificar datos del producto y actualizar su inventario.
- delete_product: elimina un producto (solo para usuarios administradores).

"""


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from TechSolutionsApp.models import Product, Category, Inventory
from django.db.models import Q
from TechSolutionsApp.views.authentication import login_required

@login_required
def view_products(request):
    '''
    Función para cargar los productos en view_products.html, permite filtrar
    por categoría, nombre o sku y asigna el inventario y categoría
    '''
    
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')  # Para el combobox

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))

    # Filtra los productos por categoría especificada (en caso de)
    if category_id and category_id != '0':
        products = products.filter(category__categoryId=category_id)

    # Agregar stock
    for product in products:
        inventory = Inventory.objects.filter(product=product).first()
        product.stock = inventory.productQuantity if inventory else 0

    categories = Category.objects.all()
    role = request.session.get('role_id')

    return render(request, 'products/view_products.html', {
        'products': products,
        'query': query,
        'role': role,
        'categories': categories,
        'selected_category': int(category_id) if category_id else 0
    })



@login_required
def edit_product(request, id):
    '''
    Función para editar un producto, carga los datos del producto en el formulario edit_product.html
    '''
    
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        sku = request.POST.get('sku')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        stock_input  = request.POST.get('stock')
        status = request.POST.get('status')
        is_active = True if status == 'activo' else False

        #obtiene el objeto categoría, a partir del category_id que tiene el producto
        category_id = int(category_id)
        try:
            category = Category.objects.get(categoryId=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe.')
            return redirect('edit_product', id=id)

        try:
            price = float(price)
        except ValueError:
            messages.error(request, 'El precio ingresado no es válido.')
            return redirect('edit_product', id=id)


        try:
            inventory = Inventory.objects.get(product=product)
            current_stock = inventory.productQuantity
        except Inventory.DoesNotExist:
            inventory = None
            current_stock = 0
            
        # Validar o conservar el stock
        if stock_input is None or stock_input.strip() == '':
            stock = current_stock
        else:
            try:
                stock = int(stock_input)
                if stock < 0:
                    raise ValueError()
            except ValueError:
                messages.error(request, 'La cantidad debe ser un número entero positivo.')
                return redirect('edit_product', id=id)

        # Actualizar campos del producto
        product.name = name
        product.price = price
        product.sku = sku
        product.category = category
        product.status = is_active
        if image:
            product.image = image
        product.save()

        # Actualizar cantidad en inventario
        if inventory is None:
            inventory = Inventory(product=product)
        inventory.productQuantity = stock
        inventory.save()

        messages.success(request, 'Producto actualizado exitosamente.')
        return redirect('view_products')

    else:
        categories = Category.objects.all()
        # Obtener stock actual
        try:
            inventory = Inventory.objects.get(product=product)
            stock_quantity = inventory.productQuantity
        except Inventory.DoesNotExist:
            stock_quantity = 0

        context = {
            'product': product,
            'categories': categories,
            'stock_quantity': stock_quantity
        }
        return render(request, 'products/edit_product.html', context)



@login_required
def delete_product(request, id):
    '''
    Función para eliminar un producto, recibe el id desde view_products.html
    '''
    
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    product = get_object_or_404(Product, productId=id)
    
    if request.method == 'POST':
        product.delete()
    return redirect('view_products')


@login_required
def add_product(request):
    '''
    Función para agregar un producto, valida los datos y asigna la categoría y el inventario
    '''
    
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        sku = request.POST.get('sku')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        stock = request.POST.get('stock')
        status = request.POST.get('status')
        is_active = True if status == 'activo' else False # convertir a booleano

        # Obtener objeto categoría a partir del id
        try:
            category = Category.objects.get(categoryId=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe.')
            return redirect('add_product')

        # Validar precio 
        try:
            price = float(price)
        except ValueError:
            messages.error(request, 'El precio ingresado no es válido.')
            return redirect('add_product')

        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError()
        except ValueError:
            messages.error(request, 'La cantidad en inventario debe ser un número entero positivo.')
            return redirect('add_product')

        # Guardar el producto
        product = Product(
            name=name,
            price=price,
            sku=sku,
            category=category,
            image=image,
            status=is_active
        )
        product.save()

        # Crear entrada de inventario con el stock ingresado
        Inventory.objects.create(product=product, productQuantity=stock)

        messages.success(request, 'Producto agregado exitosamente.')
        return redirect('add_product')

    else:
        categories = Category.objects.all()
        return render(request, 'products/add_product.html', {'categories': categories})


