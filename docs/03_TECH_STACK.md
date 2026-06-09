# Especificación del Stack Tecnológico - Aunary

## 1. Arquitectura General
El sistema adopta una estrategia de **múltiples repositorios (Multi-repo)** para separar de forma estricta las responsabilidades de la interfaz de usuario y el procesamiento de datos del backend:
*   `aunary-web`: Repositorio del cliente web (Frontend).
*   `aunary-api`: Repositorio de la API (Backend).

ambos servicios se despliegan de forma independiente en la infraestructura serverless de **Vercel**.

---

## 2. Frontend (`aunary-web`)

| Tecnología | Rol en el Proyecto | Justificación |
| :--- | :--- | :--- |
| **Next.js** | Framework de React | Permite Renderizado en el Servidor (SSR) y Generación Estática (SSG). Esto es esencial para que los proyectos públicos de Aunary se indexen correctamente en motores de búsqueda (SEO) y carguen rápido. |
| **Tailwind CSS** | Estilizado | Permite diseñar interfaces de forma rápida mediante clases de utilidad directamente en el HTML/JSX, manteniendo el peso del CSS al mínimo. |
| **HeroUI** | Biblioteca de Componentes | Provee componentes de interfaz de usuario preconstruidos y accesibles (botones, modales, formularios), lo que agiliza el desarrollo visual sin sacrificar la personalización. |

---

## 3. Backend (`aunary-api`)

| Tecnología | Rol en el Proyecto | Justificación |
| :--- | :--- | :--- |
| **Python** | Lenguaje de Programación | Es el lenguaje estándar en la industria para el manejo de datos y machine learning, dejando la puerta abierta a futuras integraciones de inteligencia artificial (ej. recomendación inteligente de proyectos). |
| **FastAPI** | Framework Web (API) | Es uno de los frameworks más rápidos de Python. Cuenta con soporte nativo para programación asíncrona (`async/await`), tipado estricto mediante Pydantic y generación automática de la documentación de la API (Swagger). |

---

## 4. Persistencia, Caché y Almacenamiento

| Tecnología | Rol en el Proyecto | Justificación |
| :--- | :--- | :--- |
| **PostgreSQL** | Base de Datos Relacional | Excelente para manejar las relaciones complejas de la aplicación (Usuarios -> Proyectos -> Roles -> Solicitudes) garantizando la integridad de los datos. |
| **Redis** | Base de Datos en Memoria | Actúa como capa de caché para almacenar las consultas pesadas del feed público o los listados de habilidades, reduciendo el tiempo de carga de la aplicación. |
| **Cloudinary** | Almacenamiento de Medios | Gestiona, optimiza y sirve las imágenes de perfil de los usuarios y portadas de los proyectos a través de su CDN, evitando sobrecargar nuestro servidor. |

---

## 5. Infraestructura y Despliegue

| Tecnología | Rol en el Proyecto | Justificación |
| :--- | :--- | :--- |
| **Vercel** | Hosting y Serverless | Aloja tanto el frontend de Next.js como el backend de FastAPI (ejecutado como funciones serverless). Ofrece despliegues automáticos basados en Git, SSL gratuito y escalabilidad automática sin costo en su plan inicial. |
| **Neon / Supabase** *(Recomendado)* | Proveedor de PostgreSQL Serverless | Ofrecen bases de datos Postgres administradas con mecanismos integrados de **Connection Pooling**, indispensables para evitar la saturación de conexiones causada por el comportamiento de las funciones serverless de Vercel. |
