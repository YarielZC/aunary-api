# Estructura de Directorios y Arquitectura de Código - Aunary

Este documento detalla la organización de archivos y carpetas del repositorio de la API (`aunary-api`). El proyecto está estructurado bajo el patrón de **Monolito Modular**, agrupando el código según su dominio de negocio (módulos) en lugar de su rol técnico, facilitando la escalabilidad y una eventual migración a microservicios si fuese necesario.

---

## 1. Vista General del Árbol de Directorios

```text
aunary-api/
├── docs/                       # Documentación técnica general del sistema
├── src/                        # Código fuente de la aplicación
│   ├── core/                   # Componentes y utilidades de uso transversal
│   ├── modules/                # Dominios de negocio del monolito modular
│   │   ├── applications/       # Gestión de postulaciones a proyectos
│   │   ├── projects/           # Gestión de proyectos y roles vacantes
│   │   └── users/              # Autenticación, registro y perfiles de usuario
│   ├── config.py               # Gestión de variables de entorno y settings
│   ├── database.py             # Conexión, motor y sesión de la base de datos
│   └── main.py                 # Punto de entrada de la aplicación FastAPI
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Exclusiones de Git
├── docker-compose.yml          # Orquestación local de PostgreSQL y Redis
├── Dockerfile                  # Empaquetado del servicio de la API
└── requirements.txt            # Dependencias de Python del proyecto
```

---

## 2. Descripción Detallada de Carpetas y Archivos

### 📂 Carpeta Raíz
Contiene los archivos de configuración del entorno de desarrollo, empaquetado, dependencias y servicios de infraestructura local.
*   **`docker-compose.yml`**: Configura los contenedores locales de PostgreSQL y Redis con volúmenes de datos persistentes.
*   **`Dockerfile`**: Define la imagen de contenedor basada en `python-slim` para ejecutar la API en producción o entornos similares.
*   **`requirements.txt`**: Lista de dependencias del proyecto utilizando bibliotecas estables como SQLModel, FastAPI y controladores de base de datos.

### 📂 `docs/`
Espacio dedicado exclusivamente a la documentación de arquitectura del proyecto para mantener el repositorio ordenado y legible.

### 📂 `src/` (Directorio de Código Fuente)
Es el núcleo del backend. Todo el código ejecutable de Python reside dentro de esta carpeta para facilitar las importaciones y la modularidad.

#### Archivos Base de `src/`
*   **`main.py`**: Instancia la aplicación FastAPI, configura las políticas de CORS, monta los middleware globales e incluye las rutas de cada módulo.
*   **`config.py`**: Utiliza `pydantic-settings` para validar y tipar las variables de entorno definidas en el archivo `.env`.
*   **`database.py`**: Configura el motor de base de datos (`engine`) de SQLModel, expone la función generadora de sesiones (`get_session`) para inyección de dependencias y maneja la inicialización de las tablas de la base de datos.

#### 📂 `src/core/`
Contiene la lógica transversal del sistema que no pertenece a ningún dominio de negocio específico, pero es requerida por múltiples módulos.
*   **`security.py`**: Implementa las funciones de hasheo de contraseñas (usando `bcrypt`), generación y validación de tokens de acceso JWT.

#### 📂 `src/modules/` (Módulos de Dominio)
Cada submódulo en esta carpeta representa una unidad de negocio autocontenida que encapsula su propia lógica. Para mantener el desacoplamiento, cada módulo utiliza un esquema interno de tres archivos:

1.  **`models.py`**: Define las entidades de la base de datos utilizando herencia de SQLModel (que actúa tanto como esquema de base de datos como esquema de validación Pydantic).
2.  **`router.py`**: Define los endpoints HTTP de FastAPI y expone la interfaz de comunicación para el cliente web.
3.  **`service.py`**: Encapsula las reglas de negocio y las consultas directas a la base de datos a través de la sesión de SQLModel (patrón servicio/capa de persistencia).

##### Dominios Implementados:
*   **`users/`**: Se encarga del registro, inicio de sesión (OAuth y tradicional), perfiles de usuario y asignación de habilidades técnicas (*skills*).
*   **`projects/`**: Maneja la creación de ideas de proyectos, especificación de categorías y publicación de roles o vacantes disponibles dentro de cada proyecto.
*   **`applications/`**: Administra las postulaciones enviadas por los colaboradores a los roles abiertos y la gestión de aprobación o rechazo de las mismas.
