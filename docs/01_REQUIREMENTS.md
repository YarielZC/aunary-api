# Documento de Especificación de Requisitos (SRS)

**Proyecto:** Aunary
**Arquitectura:** Monolito Modular (Serverless Backend / Multi-repo)
**Stack Tecnológico:** Next.js, FastAPI, PostgreSQL, Redis, Cloudinary.

## 1. Requisitos Funcionales (FRs)

### Módulo de Autenticación y Usuarios (User Domain)

*   **FR1.1:** El sistema debe permitir el registro y login mediante correo electrónico/contraseña y OAuth 2.0 (Google y GitHub).
*   **FR1.2:** El sistema debe permitir a los usuarios crear y editar un perfil profesional que incluya: Biografía, enlaces externos (GitHub, LinkedIn, Portafolio) y nivel de experiencia.
*   **FR1.3:** El sistema debe permitir a los usuarios asociar un conjunto de "Habilidades Técnicas" (Skills) a su perfil a partir de un catálogo predefinido (ej. React, Python, Figma).

### Módulo de Proyectos (Project Domain)

*   **FR2.1:** Un usuario (Creador) debe poder crear un Proyecto especificando: Título, Descripción, Categoría, Estado actual (Idea, MVP, En progreso) y una imagen de portada (procesada y almacenada en Cloudinary).
*   **FR2.2:** El Creador debe poder definir múltiples "Posiciones/Roles Abiertos" dentro de un proyecto (ej. "Desarrollador Frontend", "Diseñador UI"), especificando las habilidades requeridas y el tipo de compensación (Equity, Pro-bono, Pago).
*   **FR2.3:** El sistema debe permitir al creador la edición, pausa (cerrar vacantes temporalmente) o cierre definitivo de un proyecto.

### Módulo de Descubrimiento (Discovery Domain)

*   **FR3.1:** El sistema debe proveer un *Feed* público y paginado de proyectos activos.
*   **FR3.2:** El sistema debe proporcionar un motor de filtros combinados: por Categoría de proyecto, Habilidades requeridas, y Tipo de compensación.
*   **FR3.3:** El sistema debe incluir un motor de búsqueda por texto libre que evalúe coincidencias en el título o descripción del proyecto.

### Módulo de Colaboración (Collaboration Domain)
*   **FR4.1:** Un usuario (Colaborador) debe poder enviar una "Solicitud de Unión" (Application) a una posición específica y abierta de un proyecto, incluyendo un breve mensaje de presentación (Pitch).
*   **FR4.2:** El Creador debe recibir las solicitudes, poder visualizar el perfil completo del solicitante, y actualizar el estado de la solicitud a: "Aceptada", "Rechazada" o "En revisión".
*   **FR4.3:** El sistema debe proveer un panel de control (Dashboard) diferenciado: una vista de "Mis Proyectos" (creados) y "Mis Solicitudes" (enviadas).

---

## 2. Requisitos No Funcionales (NFRs)

*   **NFR1 - Rendimiento (Performance):** El tiempo de respuesta de la API (FastAPI) para consultas de lectura en el feed público no debe exceder los 300ms en el percentil 95 (p95).
*   **NFR2 - Escalabilidad de BD (Connection Pooling):** Dado que la API se desplegará en un entorno Serverless (Vercel), las funciones se crean y destruyen dinámicamente. El sistema **debe usar un Connection Pooler** externo (como PgBouncer, o la integración nativa de Neon DB/Supabase) para evitar exceder el límite máximo de conexiones concurrentes de PostgreSQL durante los *cold starts*.
*   **NFR3 - Caché (Redis):** Las consultas de alto tráfico, específicamente el "Feed principal de proyectos" y el "Catálogo de Skills", deben estar cacheadas en Redis para minimizar la carga de lectura en PostgreSQL.
*   **NFR4 - Seguridad:** La autenticación entre `aunary-web` y `aunary-api` debe realizarse mediante tokens JWT (JSON Web Tokens) implementados preferiblemente como cookies HttpOnly para mitigar ataques XSS. Todas las contraseñas nativas deben ser encriptadas usando algoritmos robustos (bcrypt o Argon2).
*   **NFR5 - Disponibilidad y Resiliencia:** El sistema debe tolerar fallas en servicios de terceros. Por ejemplo, si la API de Cloudinary no responde, la UI debe cargar avatares y portadas por defecto (fallbacks) sin interrumpir la experiencia del usuario.

---

## 3. Historias de Usuario (User Stories) Core

**US1: Como Creador, quiero publicar una idea de proyecto para encontrar colaboradores.**
*   *AC1:* El formulario de creación exige título, descripción mínima de 100 caracteres y al menos 1 posición/rol requerido.
*   *AC2:* Al subir una imagen de portada, el backend la envía a Cloudinary y guarda únicamente la URL devuelta en PostgreSQL.
*   *AC3:* El proyecto se marca como 'activo' y aparece inmediatamente en el Feed público.

**US2: Como Colaborador, quiero filtrar proyectos por tecnología para encontrar aquellos que encajen con mis habilidades.**
*   *AC1:* La interfaz de usuario (UI) debe mostrar un panel de filtros dinámicos.
*   *AC2:* Si el usuario selecciona "React" y "Python", el feed debe mutar para mostrar exclusivamente proyectos que requieran al menos una de esas dos tecnologías.
*   *AC3:* Si los filtros no devuelven coincidencias, se debe mostrar un *Empty State* amigable que invite a cambiar la búsqueda.

**US3: Como Colaborador, quiero postularme a un rol específico de un proyecto para ofrecer mi ayuda.**
*   *AC1:* En la vista de detalle del proyecto, cada rol con vacantes abiertas debe tener un botón "Aplicar".
*   *AC2:* Al hacer clic, se despliega un modal (HeroUI) con un área de texto para un mensaje de máximo 500 caracteres.
*   *AC3:* El sistema debe impedir (validación en backend y frontend) que un usuario se postule más de una vez al mismo rol en el mismo proyecto.

**US4: Como Creador, quiero revisar las solicitudes recibidas para elegir al candidato ideal.**
*   *AC1:* El panel de administración del proyecto muestra tarjetas tabuladas con los aplicantes agrupados por rol.
*   *AC2:* Un clic en el aplicante despliega su mensaje, perfil, habilidades y enlaces (GitHub/LinkedIn).
*   *AC3:* Acciones de "Aceptar" o "Rechazar" cambian el estado en la base de datos y proveen feedback visual inmediato.

**US5: Como Usuario, quiero iniciar sesión con mi cuenta de GitHub para agilizar mi registro y mostrar credibilidad técnica.**
*   *AC1:* El sistema implementa flujo OAuth 2.0 con GitHub.
*   *AC2:* En el primer inicio de sesión exitoso, el sistema extrae el correo, nombre y avatar de GitHub para crear automáticamente un perfil en la base de datos de Aunary.
