- Crear entorno virtual usando "virtualenv"
python3 -m venv venv
activar el entorno virtual en "/venv/scritps/activate"

- Instalar repositorios desde "requeriments" usando "pip"
"pip install -r requirements.txt"

- Crear base de datos en MySQL con una database que se llame "login" y dos tablas: "user" y "data"
Encabezados de tablas:
- User:
id -> smallint(3) ->  Primary key 
username -> varchar(20)
password -> char(102)
fullname -> varchar(50)

Data:
code -> char(6) -> Primary key
name -> varchar(60)
credits -> tinyint(3)

- Para crear una password hasheada e insertarla en la base de datos:
descomentar el "print" del archivo "src\models\entities\User.py", esto nos generará una password hasheada la cual deberemos insertar dentro de la base
de datos con su respectivo username.

- Al loguearnos desde el formulario web localhost:5000/login esto nos generará una api key por consola la cual usaremos para los endpoints de la API REST

- Endpoint API REST:

GET: http://127.0.0.1:5000/courses
POST: http://127.0.0.1:5000/courses

Ejemplo de json que recibe el metodo POST:

{
    "code": "2",
    "credits" : 5,
    "name" : "Kenwin"
}

Recordar enviar el access token en el header mediante la variable "x-access-token"
