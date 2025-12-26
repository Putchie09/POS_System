"""
categories.py

Contiene las vistas encargadas de gestionar las categorías de productos
en el sistema.

Operaciones disponibles:
- Agregar nuevas categorías (evitando duplicados)
- Ver y filtrar las categorías existentes
- Editar una categoría, con validación de unicidad de nombre
- Eliminar una categoría existente

"""


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from TechSolutionsApp.models import Category
from TechSolutionsApp.views.authentication import login_required
from django.db.models import Q

@login_required
def add_category(request):
    '''
    Función para agregar una categoría
    '''
    
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if not name:
            messages.error(request, 'El nombre de la categoría no puede estar vacío.')
            return render(request, 'categories/add_category.html')
        
        # validar si ya existe la categoría
        if Category.objects.filter(name__iexact=name).exists():
            messages.error(request, 'Ya existe una categoría con ese nombre.')
            return render(request, 'categories/add_category.html')
        
        # SI no existe, se crea la categoría
        category = Category(name = name)
        category.save()
        
        messages.success(request, 'Categoría agregada correctamente.')
    return render(request, 'categories/add_category.html')


@login_required
def view_categories(request):
    '''
    Función para ver las categorías agregaadas, permite filtrar por nombre
    '''
    
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    role = request.session.get('role_id')
    
    if query:
        categories = categories.filter(Q(name__icontains=query))
    
    return render(request, 'categories/view_categories.html', {'categories': categories, 'role': role})


@login_required
def edit_category(request, id):
    '''
    Función para editar una categoría
    '''
    
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    
    category = get_object_or_404(Category, categoryId=id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            messages.error(request, 'El nombre no puede estar vacío.')
            
        # verifica si existe otra categoría con ese nombre    
        elif Category.objects.filter(name__iexact=name).exclude(categoryId=id).exists():
            messages.error(request, 'Ya existe otra categoría con ese nombre.')
        
        # si no existe otra categoría con ese nombre, la modifica    
        else:
            category.name = name
            category.save()
            messages.success(request, 'Categoría modificada correctamente.')
            return redirect('view_categories')  

    return render(request, 'categories/edit_category.html', {'category': category})


@login_required
def delete_category(request, id):
    '''
    Función para borrar una categoría
    '''
    
    role = request.session.get('role_id')
    if role != 1:
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('home')
    
    category = get_object_or_404(Category, categoryId=id)
    if request.method == 'POST':
        category.delete()
    return redirect('view_categories')
