# Fintual-Software-Engineer

## **Descripción del Proyecto**

Este proyecto es una aplicación web en Django que permite a los usuarios crear un portafolio de acciones. Los usuarios pueden seleccionar acciones reales, ingresar fechas de inicio y fin, y calcular la rentabilidad del portafolio basándose en los precios de las acciones en esas fechas. El proyecto usa **yfinance** para obtener los precios reales de las acciones y valida que las fechas no sean futuras, ya que el sistema funciona con datos reales.

---

## **Requerimientos del Sistema**

- Python 3.8 o superior
- pip (Python package installer)
- Git

---

## **Instrucciones para clonar el repositorio y ejecutar el proyecto localmente**

### 1. **Clonar el Repositorio**

Primero, clona el repositorio en tu máquina local usando Git. En tu terminal o línea de comandos, ejecuta el siguiente comando:

```bash
git clone https://github.com/sachondo7/Fintual-Software-Engineer.git
```


### 2. **Crear y Activar un Entorno Virtual**

Es recomendable utilizar un entorno virtual para aislar las dependencias del proyecto. Ejecuta los siguientes comandos para crear y activar un entorno virtual:

```bash
# Navega al directorio del proyecto clonado
cd Fintual-Software-Engineer

# Crear un entorno virtual
python -m venv env

# Activar el entorno virtual:
# En Windows:
env\Scripts\activate
# En macOS/Linux:
source env/bin/activate
```

### 3. **Instalar Dependencias**

Una vez que el entorno virtual esté activado, instala las dependencias necesarias desde el archivo `requirements.txt` que contiene todas las bibliotecas que el proyecto utiliza.

```bash
pip install -r requirements.txt
```

Esto instalará Django e yfinance que son las dependencias del proyecto.

### 4. **Migrar la Base de Datos**

Django utiliza una base de datos para almacenar información sobre el portafolio y las acciones. Para configurar la base de datos, ejecuta los siguientes comandos para aplicar las migraciones necesarias:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. **Crear Datos de Ejemplo (Acciones)**

Para este proyecto, hemos utilizado 5 acciones populares. Inserta las siguientes acciones en la base de datos ejecutando el comando interactivo de Django:

```bash
python manage.py shell
```

Luego, ejecuta el siguiente código para insertar las acciones:

```python
from portfolio.models import Stock

Stock.objects.create(name="Apple Inc.", symbol="AAPL")
Stock.objects.create(name="Microsoft Corp.", symbol="MSFT")
Stock.objects.create(name="Amazon.com Inc.", symbol="AMZN")
Stock.objects.create(name="Alphabet Inc.", symbol="GOOGL")
Stock.objects.create(name="Tesla Inc.", symbol="TSLA")

exit()  # Para salir del shell interactivo
```

### 6. **Ejecutar el Servidor de Desarrollo**

Finalmente, ejecuta el servidor de desarrollo de Django con el siguiente comando:

```bash
python manage.py runserver
```

Esto levantará el servidor localmente. Podrás acceder a la aplicación abriendo un navegador y yendo a la siguiente URL:

```
http://127.0.0.1:8000/
```

### 7. **Uso de la Aplicación**

1. **Crear un Portafolio**: Una vez en la página de inicio, selecciona las fechas de inicio y fin, elige las acciones que deseas incluir en tu portafolio, asigna los porcentajes correspondientes y haz clic en "Crear Portafolio".
2. **Ver Precios**: El sistema obtendrá los precios de las acciones seleccionadas en las fechas indicadas, calculará las ganancias y mostrará los precios correspondientes.

---

## **Estructura del Proyecto**

El proyecto sigue la estructura típica de Django. A continuación, se describen algunos de los archivos y carpetas más importantes:

```
nombre-del-repositorio/
│
├── portfolio/                # Aplicación principal
│   ├── migrations/           # Archivos de migración de la base de datos
│   ├── static/               # Archivos estáticos como CSS y JS
│   │   └── portfolio/        # Archivos específicos de la app (CSS, JS)
│   │       ├── styles.css    # Estilos personalizados
│   │       └── scripts.js    # Lógica JS para la validación y llamadas AJAX
│   ├── templates/            # Archivos de plantilla (HTML)
│   │   └── create_portfolio.html # Página principal para crear el portafolio
│   │   └──portfolio_summary.html # Página principal de los datos que obtuvo el portafolio
│   ├── models.py             # Definición de los modelos (acciones, portafolios)
│   ├── views.py              # Definición de las vistas (lógica del servidor)
│   └── urls.py               # Configuración de las rutas
│
├── portfolio_project/         # Configuración del proyecto Django
│   ├── settings.py           # Configuración del proyecto (base de datos, staticfiles, etc.)
│   ├── urls.py               # Rutas del proyecto
│
├── manage.py                  # Script de Django para administrar el proyecto
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación del proyecto
```

---

## **Dependencias Clave**

- **Django**: El framework web principal que gestiona el backend de la aplicación.
- **yfinance**: Biblioteca que se utiliza para obtener datos de precios reales de las acciones desde Yahoo Finance.

---