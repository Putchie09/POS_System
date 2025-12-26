'''
admin.py

Configura la interfaz de administración de Django para los modelos del sistema
Define cómo se muestran y gestionan los modelos en el panel de administración

Modelos registrados:
- Role
- Employee
- Customer
- Category
- Product
- Inventory
- Sale
- SaleDetail
'''

from django.contrib import admin
from .models import Role, Employee, Customer, Category, Product, Inventory, Sale, SaleDetail


# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('roleId', 'description')
    search_fields = ('description',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeeId', 'firstName', 'lastName', 'idNumber', 'phoneNumber', 'role')
    search_fields = ('firstName', 'lastName', 'idNumber')
    list_filter = ('role',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customerId', 'firstName', 'lastName', 'email', 'idNumber')
    search_fields = ('firstName', 'lastName', 'email', 'idNumber')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryId', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productId', 'name', 'price', 'category', 'status', 'sku', 'dateAdded', 'modificationDate')
    search_fields = ('name', 'sku')
    list_filter = ('status', 'category')
    readonly_fields = ('dateAdded', 'modificationDate')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inventoryId', 'product', 'productQuantity', 'modificationDate')
    list_filter = ('modificationDate',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('saleId', 'customer', 'user', 'saleDate', 'discountPercentage', 'modificationDate')
    list_filter = ('saleDate', 'user', 'modificationDate')
    search_fields = ('customer__firstName', 'customer__lastName')


@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('saleDetailId', 'sale', 'product', 'quantity', 'unitPrice')
    search_fields = ('sale__id', 'product__name')
    list_filter = ('product',)