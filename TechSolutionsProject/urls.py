from django.contrib import admin
from django.urls import path
from TechSolutionsProject import settings
from django.conf.urls.static import static
from TechSolutionsApp.views import customers, categories, products, authentication, sales, employees


urlpatterns = [
    #Login and start
    path('admin/', admin.site.urls),
    path('', authentication.login, name='login'),
    path('logout/', authentication.logout_view, name='logout'),
    path('home/', authentication.index, name='home'),

    # Sales
    path('add_sale/', sales.add_sale, name='add_sale'),
    path('view_sales/', sales.view_sales, name='view_sales'),
    path('edit_sale/<int:id>/', sales.edit_sale, name='edit_sale'),
    path('delete_sale/<int:id>/', sales.delete_sale, name='delete_sale'),
    
    # Customers
    path('add_customer/', customers.add_customer, name='add_customer'),
    path('edit_customer/<int:id>/', customers.edit_customer, name='edit_customer'),
    path('delete_customer/<int:id>/', customers.delete_customer, name='delete_customer'),
    path('view_customers/', customers.view_customers, name='view_customers'),

    #Employees
    path('employees/', employees.view_employees, name='view_employees'),
    path('add_employee/', employees.add_employee, name='add_employee'),
    path('edit_employee/<int:id>/', employees.edit_employee, name='edit_employee'),
    path('delete_employee/<int:id>/', employees.delete_employee, name='delete_employee'),
    
    # Products
    path('edit_product/<int:id>/', products.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', products.delete_product, name='delete_product'),
    path('view_products/', products.view_products, name='view_products'),
    path('add_product/', products.add_product, name='add_product'),
    
    # Categories
    path("add_category/", categories.add_category, name="add_category"),
    path('view_categories/', categories.view_categories, name='view_categories'),
    path('edit_category/<int:id>/', categories.edit_category, name='edit_category'),

    path('delete_category/<int:id>', categories.delete_category, name='delete_category')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)