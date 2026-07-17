# Sistema de Detección de Anomalías en Builds

**Versión actual: 1.0.0**

Aplicación web desarrollada en Python y Flask para el procesamiento y análisis de datasets de TravisTorrent.

El sistema permite cargar archivos CSV, limpiar y validar los datos, analizar la duración de los builds, detectar valores atípicos mediante el método del rango intercuartílico (IQR), generar visualizaciones y descargar los resultados del análisis en un archivo ZIP.


## Características principales

El sistema permite:

- Cargar datasets en formato CSV.
- Procesar archivos de gran tamaño.
- Detectar automáticamente diferentes esquemas de TravisTorrent.
- Limpiar y validar los datos.
- Analizar la distribución de la duración de los builds.
- Calcular el rango intercuartílico (IQR).
- Detectar valores atípicos u outliers.
- Validar los resultados obtenidos.
- Generar siete gráficas para la visualización de los datos.
- Mostrar una interpretación de los resultados.
- Visualizar el progreso durante la carga y procesamiento.
- Descargar los resultados generados en un archivo ZIP.
- Generar logs de ejecución.

## Tecnologías utilizadas

El proyecto utiliza las siguientes tecnologías:

- Python
- Flask
- pandas
- Matplotlib
- HTML
- CSS
- JavaScript

## Requisitos previos

Antes de ejecutar el proyecto es necesario contar con:

- Python instalado.
- pip disponible.
- Conexión a Internet durante la instalación inicial de las dependencias.
- Espacio suficiente en disco para almacenar y procesar los datasets.

Se recomienda utilizar la versión de Python compatible con las dependencias especificadas en `requirements.txt`.

Para comprobar que Python está instalado, ejecutar:

### Windows

```powershell
python --version
```

### macOS

```bash
python3 --version
```

También se puede comprobar la disponibilidad de pip.

### Windows

```powershell
python -m pip --version
```

### macOS

```bash
python3 -m pip --version
```

## Descargar o copiar el proyecto

El proyecto debe encontrarse almacenado en una carpeta local del equipo.

La estructura principal es la siguiente:

```text
SistemaAnomaliasBuilds/
├── src/
│   ├── analisis_datos.py
│   ├── app.py
│   ├── logger_sistema.py
│   ├── main.py
│   ├── procesamiento_datos.py
│   ├── prueba_servicio.py
│   └── servicio_analisis.py
│
├── static/
│   ├── css/
│   │   └── estilos.css
│   │
│   └── js/
│       └── progreso.js
│
├── templates/
│   └── index.html
│
├── requirements.txt
├── .gitignore
└── README.md
```

Las carpetas de archivos cargados y resultados pueden ser creadas automáticamente durante la ejecución del sistema.

## Instalación en Windows

### 1. Abrir PowerShell

Abrir PowerShell y dirigirse a la carpeta raíz del proyecto.

Ejemplo:

```powershell
cd "D:\ruta\del\proyecto\SistemaAnomaliasBuilds"
```

Es importante ejecutar los siguientes comandos desde la carpeta donde se encuentran:

```text
requirements.txt
src/
static/
templates/
```

### 2. Crear el entorno virtual

Ejecutar:

```powershell
python -m venv env
```

Este comando creará la carpeta:

```text
env/
```

El entorno virtual permite instalar las dependencias del proyecto de forma aislada.

### 3. Activar el entorno virtual

En PowerShell ejecutar:

```powershell
.\env\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script, utilizar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Después volver a activar el entorno:

```powershell
.\env\Scripts\Activate.ps1
```

Cuando el entorno esté activo, la terminal mostrará algo similar a:

```text
(env) PS D:\ruta\del\proyecto\SistemaAnomaliasBuilds>
```

### 4. Instalar las dependencias

Ejecutar:

```powershell
python -m pip install -r .\requirements.txt
```

Esperar hasta que finalice la instalación.

### 5. Validar las dependencias

Ejecutar:

```powershell
python -m pip check
```

El resultado esperado es:

```text
No broken requirements found.
```

### 6. Iniciar la aplicación Flask

Ejecutar:

```powershell
python .\src\app.py
```

Si la aplicación inicia correctamente, la terminal mostrará la dirección local del servidor.

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

### 7. Detener la aplicación

Para detener Flask, regresar a PowerShell y presionar:

```text
Ctrl + C
```

### 8. Desactivar el entorno virtual

Cuando se termine de utilizar el proyecto, ejecutar:

```powershell
deactivate
```

## Instalación en macOS

### 1. Abrir Terminal

Abrir Terminal y dirigirse a la carpeta raíz del proyecto.

Ejemplo:

```bash
cd "/ruta/del/proyecto/SistemaAnomaliasBuilds"
```

### 2. Crear el entorno virtual

Ejecutar:

```bash
python3 -m venv env
```

### 3. Activar el entorno virtual

Ejecutar:

```bash
source env/bin/activate
```

Cuando el entorno esté activo, la terminal mostrará:

```text
(env)
```

al inicio de la línea de comandos.

### 4. Instalar las dependencias

Ejecutar:

```bash
python -m pip install -r requirements.txt
```

### 5. Validar las dependencias

Ejecutar:

```bash
python -m pip check
```

El resultado esperado es:

```text
No broken requirements found.
```

### 6. Iniciar la aplicación Flask

Ejecutar:

```bash
python src/app.py
```

Después abrir en el navegador:

```text
http://127.0.0.1:5000
```

### 7. Detener la aplicación

Para detener Flask, regresar a Terminal y presionar:

```text
Control + C
```

### 8. Desactivar el entorno virtual

Ejecutar:

```bash
deactivate
```

## Ejecuciones posteriores

Después de realizar la instalación inicial, no es necesario volver a crear el entorno virtual ni instalar las dependencias cada vez que se utiliza el sistema.

### Windows

Abrir PowerShell en la carpeta del proyecto.

Activar el entorno virtual:

```powershell
.\env\Scripts\Activate.ps1
```

Iniciar Flask:

```powershell
python .\src\app.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

### macOS

Abrir Terminal en la carpeta del proyecto.

Activar el entorno virtual:

```bash
source env/bin/activate
```

Iniciar Flask:

```bash
python src/app.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Uso del sistema

Una vez iniciada la aplicación:

1. Abrir la interfaz web.
2. Seleccionar un archivo CSV.
3. Presionar el botón `Procesar dataset`.
4. Esperar a que finalice la carga y procesamiento.
5. Revisar las métricas obtenidas.
6. Consultar los resultados del método IQR.
7. Revisar la interpretación generada.
8. Consultar los outliers por estado.
9. Visualizar las gráficas.
10. Descargar el archivo ZIP con los resultados.

Durante la carga de archivos grandes, la aplicación muestra un indicador visual de progreso y el tiempo transcurrido.

No se debe cerrar la aplicación ni la terminal mientras se está procesando un dataset.

## Compatibilidad de datasets

El sistema reconoce automáticamente diferentes versiones del esquema de TravisTorrent.

### Esquema reciente

El sistema puede procesar archivos que contienen las columnas:

```text
tr_duration
gh_build_started_at
tr_status
gh_project_name
tr_log_num_tests_run
tr_log_num_tests_failed
tr_log_frameworks
```

### Esquema anterior

También puede procesar archivos que contienen:

```text
tr_duration
tr_started_at
tr_status
gh_project_name
tr_tests_run
tr_tests_fail
tr_frameworks
```

Las equivalencias entre ambos esquemas se interpretan internamente durante el procesamiento.

El archivo CSV original no es modificado.

## Método de detección de anomalías

La detección de valores atípicos se realiza mediante el método del rango intercuartílico.

Primero se calculan:

```text
Q1 = Primer cuartil

Q3 = Tercer cuartil

IQR = Q3 - Q1
```

Posteriormente se calculan los límites:

```text
Límite inferior = Q1 - (1.5 × IQR)

Límite superior = Q3 + (1.5 × IQR)
```

Los registros cuya duración se encuentra fuera de estos límites son clasificados como outliers.

## Resultados generados

Por cada análisis, el sistema genera una carpeta independiente dentro de:

```text
resultados/
```

Cada ejecución utiliza un identificador basado en la fecha y hora.

Ejemplo:

```text
resultados/
└── analisis_20260712_213929/
```

Dependiendo de la configuración actual del sistema, la carpeta contiene archivos como:

```text
dataset_limpio.csv
outliers_detectados.csv
resumen_resultados.txt
ejecucion_sistema.log
resultados_analisis.zip
```

También contiene las gráficas generadas durante el análisis.

## Visualizaciones generadas

El sistema genera siete visualizaciones:

1. Histograma de duración de builds.
2. Cantidad de builds por estado.
3. Boxplot para la identificación visual de outliers.
4. Comparación entre builds normales y outliers.
5. Outliers por estado del build.
6. Tendencia de fallos en el tiempo.
7. Proporción de fallos en el tiempo.

## Archivos principales

### `src/app.py`

Contiene la aplicación Flask y las rutas utilizadas para cargar datasets, mostrar los resultados y descargar el archivo ZIP.

### `src/servicio_analisis.py`

Coordina el flujo completo de procesamiento y análisis.

### `src/procesamiento_datos.py`

Se encarga de cargar, validar, limpiar y preparar los datasets.

También permite detectar automáticamente los diferentes esquemas compatibles.

### `src/analisis_datos.py`

Realiza el análisis estadístico, calcula el IQR, detecta los outliers y genera las visualizaciones.

### `src/logger_sistema.py`

Registra los principales eventos ocurridos durante la ejecución.

### `templates/index.html`

Contiene la estructura de la interfaz web.

### `static/css/estilos.css`

Contiene los estilos visuales de la aplicación.

### `static/js/progreso.js`

Controla el indicador visual utilizado durante la carga y procesamiento de los datasets.

## Archivos que no se incluyen en el repositorio

El archivo `.gitignore` excluye elementos que no forman parte del código fuente, entre ellos:

```text
env/
uploads/
resultados/
logs/
graficas/
__pycache__/
*.csv
*.zip
```

Esto evita almacenar entornos virtuales, datasets de gran tamaño y archivos generados automáticamente.

## Consideraciones para archivos grandes

El sistema ha sido diseñado para trabajar con datasets de gran tamaño.

Sin embargo, el tiempo de procesamiento depende de:

- Tamaño del archivo.
- Cantidad de registros.
- Memoria RAM disponible.
- Velocidad del procesador.
- Espacio disponible en disco.

Durante el procesamiento se generan archivos adicionales, por lo que se recomienda contar con suficiente espacio libre.

## Solución de problemas

### El comando `python` no funciona en Windows

Comprobar la instalación con:

```powershell
py --version
```

Si el comando `py` está disponible, se puede crear el entorno con:

```powershell
py -m venv env
```

### PowerShell no permite activar el entorno

Ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Después:

```powershell
.\env\Scripts\Activate.ps1
```

### Aparece `ModuleNotFoundError`

Comprobar que el entorno virtual se encuentre activo e instalar nuevamente las dependencias:

```powershell
python -m pip install -r .\requirements.txt
```

En macOS:

```bash
python -m pip install -r requirements.txt
```

### Flask indica que el puerto está ocupado

Comprobar que no exista otra instancia de la aplicación ejecutándose.

Detener la instancia anterior y volver a ejecutar:

```powershell
python .\src\app.py
```

o en macOS:

```bash
python src/app.py
```

### El procesamiento tarda varios minutos

Los archivos de gran tamaño requieren más tiempo de lectura, limpieza, análisis y generación de resultados.

La interfaz muestra un indicador visual mientras el sistema continúa trabajando.

No cerrar ni actualizar la página durante el procesamiento.

## Autores

Proyecto académico desarrollado por Angel Daniel Vega Miranda como parte de la estancia profesional
de TSU en Desarrollo de Software.

## Estado del proyecto

Versión final funcional para entrega académica.


