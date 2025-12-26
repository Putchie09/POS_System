@echo off
echo Activando entorno virtual...
call venv\Scripts\activate

echo instalando dependencias...
pip install -r requirements.txt

echo ejecutando migraciones...
python manage.py makemigrations
python manage.py migrate

echo crear superusuario...
python manage.py create_superuser

echo crear datos por defecto
python manage.py create_roles_and_admin

echo ejecutar servidor
python manage.py runserver

pause

