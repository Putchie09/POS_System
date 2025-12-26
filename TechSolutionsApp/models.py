'''
models.py

Define los modelos de base de datos del sistema.
Cada clase representa una tabla en la base de datos, con sus respectivos campos y relaciones.

Modelos incluidos:
- Role: define los tipos de roles para empleados.
- Employee: gestiona los usuarios del sistema con autenticación personalizada.
- Customer: almacena información de los clientes.
- Category: clasifica los productos en categorías.
- Product: representa los productos disponibles para la venta.
- Inventory: lleva el control de stock de los productos.
- Sale: contiene los datos generales de una venta.
- SaleDetail: desglosa los productos vendidos en cada venta.
'''
from django.db import models
from django.contrib.auth.hashers import make_password, check_password 


class Role(models.Model):
    '''
    Representa los roles asignables a los empleados del sistema
    (ejemplo: admin, user, etc.)
    '''
    roleId = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description


class Employee(models.Model):
    '''
    Representa a los empleados del sistema.
    Incluye métodos personalizados para la autenticación con contraseña.
    '''
    employeeId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)       
    idNumber = models.PositiveIntegerField(unique=True)
    phoneNumber = models.PositiveIntegerField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    passwordHash = models.CharField(max_length=128, default='')
    
    def __str__(self):
        return self.firstName + self.lastName

    def set_password(self, raw_password):
        self.passwordHash = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.passwordHash)


class Customer(models.Model):
    '''
    Representa a los clientes del sistema.
    Permite almacenar información básica y opcional como correo e identificación.
    '''
    customerId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    idNumber = models.PositiveIntegerField(unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.firstName + self.lastName


class Category(models.Model):
    '''
    Representa las categorías a las que pertenecen los productos.
    '''
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    '''
    Representa los productos disponibles para la venta.
    Incluye precio, categoría, estado, SKU, fecha y una imagen opcional.
    '''
    productId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  
    dateAdded = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    sku = models.CharField(max_length=12, default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    def __str__(self):
        return self.name


class Inventory(models.Model):
    '''
    Representa el inventario de productos.
    Almacena la cantidad disponible y la fecha de última modificación.
    '''
    inventoryId = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    productQuantity = models.PositiveIntegerField()
    modificationDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory"


class Sale(models.Model):
    '''
    Representa una venta realizada.
    Incluye cliente, empleado que la realizó, fecha y descuento aplicado.
    '''
    saleId = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    user = models.ForeignKey(Employee, on_delete=models.PROTECT)
    saleDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    discountPercentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.saleId}'


class SaleDetail(models.Model):
    '''
    Representa los detalles individuales de cada venta.
    Especifica qué productos se vendieron, en qué cantidad y a qué precio.
    '''
    saleDetailId = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  
    quantity = models.PositiveIntegerField()
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('sale', 'product')