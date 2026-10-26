# Primera evolución de Caudal Creativo

26 de octubre de 2026. Rama `feature/caudal-creativo-platform`.

Parte del checkout existente en `f4a37c9`: incorpora la rama de experiencias
(`982440b`) y conserva el cambio posterior a pesos chilenos. No se ha creado otro
proyecto, reemplazado Revel ni cambiado el contrato de emisión de entradas.

## Inspección y dependencias

| Superficie | Base reutilizada | Decisión de esta etapa |
| --- | --- | --- |
| Portada | Carga SSR de descubrimiento y ofertas reales | Nueva entrada al ecosistema; búsqueda y categorías conectadas al catálogo. |
| Explorar | `/events`, filtros, calendario y `EventCard` | Añadir categorías por etiquetas y conservar búsqueda, comuna, paginación y permisos. |
| Acceso | Cookies protegidas, bootstrap, refresh y formularios existentes | Conservar sesiones y endpoints. Cambiar la identidad visual compartida. |
| Organizaciones | Listado público y perfiles `/org/[slug]` | Reutilizar el directorio y presentar una selección regional en Comunidad. |
| Productores | `/producer`, permisos y panel `/org/[slug]/admin` | Mantener eventos, tarifas, participantes y puerta. Acceso desde el menú personal y las invitaciones a publicar. |
| Entradas | Dashboard, checkout, PDF, QR y servicios Django | Mantener su lógica y su formato CLP; presentar Caudal Tickets como servicio. |
| Administración | `/administration` y administración Django | Conservar acceso limitado al administrador de plataforma. |

La navegación compartida vive en `Header`, `MobileNav`, `UserMenu` y `Footer`.
Los layouts públicos y autenticados reutilizan esos componentes. La portada y
Comunidad consultan solo información pública; no serializan credenciales ni tokens.

## Experiencia implementada

- **Caudal Creativo** es la identidad principal, con el logotipo original
  suministrado y su símbolo sin redibujar. Fuentes locales, temas claro/oscuro,
  controles de movimiento y lenguaje editorial monocromático.
- **Inicio:** presentación territorial, buscador, calendario, ocho intereses,
  próximas actividades, organizaciones, servicios e invitación a publicar.
- **Explorar:** catálogo real con categorías que se conservan en la URL, al
  paginar y al cambiar el período del calendario. Seleccionar una etiqueta
  manual reemplaza la categoría editorial. No se rellenan resultados ficticios.
- **Agenda:** `/agenda` diferencia el calendario existente, disponible desde un
  enlace directo, del futuro servicio Caudal Agenda. No hay formularios de
  matrícula, mensualidad o reserva de horas que aparenten funcionar.
- **Comunidad:** `/comunidad` presenta organizaciones publicadas de Los Ríos,
  lugares presentes en actividades y la futura presencia de artistas,
  instructores, facilitadores y profesionales. Los perfiles de organizaciones
  enlazan al sistema existente; no se inventan personas ni colaboraciones.
- **Ecosistema:** `/ecosistema` presenta La Factoría, El Subte y Hecho en Valdivia,
  además de los servicios de Caudal. Hecho en Valdivia aparece como texto, sin
  inventar un logo normalizado o un dominio. No se anuncian integraciones.
- **Caudal Tickets:** `/tickets` explica y enlaza las herramientas operativas,
  con reservas gratuitas o pago presencial. Cobros online y liquidaciones
  permanecen pendientes.
- **Mi Caudal:** `/dashboard` conserva los datos de la cuenta e incorpora
  accesos a entradas, asistencias/reservas, organizaciones seguidas y calendario.
  Cuando todavía no hay actividades personales, el acceso al calendario conduce
  al calendario público. Las futuras inscripciones se distinguen de esos accesos.

Emergia se retiró del componente público del ecosistema. Se conservaron el activo
histórico y su documentación de procedencia; no se cargan ni se enlazan en la
experiencia pública. Se mantienen las licencias y avisos de terceros.

## Categorías: contrato editorial inicial

`apps/web/src/lib/caudal/categories.ts` traduce ocho intereses a los nombres de
etiqueta que ya admite la API. La consulta utiliza la unión de las etiquetas de
la categoría, con el comportamiento existente del backend.

| URL `category` | Etiquetas actuales |
| --- | --- |
| `musica` | música, concierto, dj |
| `escena` | artes escénicas, danza, teatro, cine, audiovisual |
| `oficios` | taller, oficios, artesanía |
| `formacion` | curso, formación, charla |
| `movimiento` | deporte, movimiento, yoga |
| `bienestar` | bienestar, terapias, salud |
| `naturaleza` | naturaleza, experiencias, aire libre |
| `comunidad` | comunidad, encuentro, actividad comunitaria |

No es clasificación automática ni un catastro cultural. Los productores deben
asignar etiquetas coherentes a sus actividades. No se agregaron etiquetas,
colaboradores ni actividades a la demostración para inflar resultados. Categorías
sin publicaciones muestran un estado vacío; una API indisponible muestra un error.
Una categoría desconocida no se envía como filtro.

La selección de organizaciones consulta las primeras 20 organizaciones públicas,
filtra su ubicación en Los Ríos y presenta hasta tres. No equivale al directorio
completo, que sigue accesible por `/organizations`. La selección de lugares parte
de las primeras 20 próximas actividades regionales y muestra hasta tres lugares
únicos. No presenta ese conjunto como un catastro completo de espacios.

## Archivos y responsabilidades

| Grupo de archivos | Responsabilidad |
| --- | --- |
| `apps/web/src/routes/(public)/+page.*` | Portada, datos públicos y metadatos principales. |
| `apps/web/src/routes/(public)/{agenda,comunidad,ecosistema,tickets}/` | Nuevas entradas del ecosistema. |
| `apps/web/src/routes/(public)/events/+page.*` | Categorías y continuidad del calendario del catálogo. |
| `apps/web/src/lib/components/caudal/` | Categorías, servicios, organizaciones, Mi Caudal y ecosistema. |
| `apps/web/src/lib/components/common/{Header,MobileNav,UserMenu,Footer}.svelte` | Navegación y accesos por sesión. |
| `apps/web/src/lib/components/brand/RevelWordmark.svelte` | Interfaz compartida conservada, mostrando el logo original Caudal Creativo. |
| `apps/web/src/lib/server/caudal/community.ts` | Selección pública regional y estados de indisponibilidad. |
| `apps/web/src/lib/caudal/categories.*`, `src/lib/utils/filters.ts` | Clasificación editorial, parámetros y pruebas de continuidad CLP. |
| `apps/web/src/lib/seo/`, `src/app.html`, sitemap | Nombre, imágenes originales y metadatos de la plataforma. |
| `apps/web/src/app.css`, `messages/*.json` | Ritmo editorial compartido y textos en seis idiomas. |
| `apps/web/src/routes/(auth)/dashboard/+page.svelte` | Accesos unificados en Mi Caudal, conservando consultas existentes. |
| `scripts/configure.py` | Identidad de la nueva configuración local, preservando archivos ya existentes. |
| `scripts/review_creative.mjs` | Recorrido de navegador y capturas reproducibles con las cuentas locales. |

No hay nuevas dependencias, migraciones, pasarelas, credenciales externas ni cambios
al servicio financiero o a los servicios de tickets. La configuración local actual
adopta el nombre Caudal Creativo; otros entornos existentes pueden actualizar
`SITE_NAME` y el nombre visible de `DEFAULT_FROM_EMAIL` sin cambiar su dirección.
Los scripts no sobrescriben sus `.env`.

## Propuesta para la siguiente fase

Antes de migrar modelos conviene acordar estos contratos:

1. **Actividades:** mantener `Event` como actividad publicable en esta etapa.
   Evaluar una taxonomía explícita y modalidades de participación antes de
   convertir las categorías editoriales en un esquema persistente. No tratar
   toda actividad como una venta de entradas.
2. **Personas y roles:** proponer un perfil creativo vinculado a la cuenta y
   relaciones explícitas con organizaciones. Una persona puede ejercer distintos
   roles y publicar con más de una organización, sujeto a permisos.
3. **Lugares compartidos:** el modelo actual de lugar conserva su organización
   administradora. Para compartirlo entre organizadores hace falta una relación
   de autorización y uso; no basta con quitar el filtro de organización.
   La interfaz actual no atribuye propiedad ni exclusividad a los espacios.
4. **Agenda:** separar curso, sesiones, inscripción, recurso reservable,
   disponibilidad e instructor. Resolver cupos y conflictos de horario con
   transacciones, zona horaria `America/Santiago` y pruebas de concurrencia.
   Evaluar recurrencia y excepciones antes de implementar mensualidades.
5. **Dinero:** definir pasarela, país, impuestos y contratos de cobro/reembolso
   antes de habilitar online en CLP. Una reserva en puerta sigue sin probar cobro.

Son propuestas para revisión, no modelos creados ni funcionalidades activadas.

## Proyección Android e iOS

La API Django, las organizaciones y el cliente generado con OpenAPI son reutilizables.
También lo son tarjetas, formularios, filtros, calendario y piezas de identidad
Svelte que no dependen de un proceso de servidor.

El build actual usa **adapter-node y SSR**: no se puede copiar directamente a
Capacitor como una aplicación estática. Las cargas `+page.server.ts`, acciones,
cookies protegidas y refresh requieren un servidor. Una evaluación de Capacitor
debe comparar un contenedor de la web remota con un cliente móvil propio que
comparta componentes y consuma la API; no se cambió el adaptador en esta etapa.

Para un cliente móvil propio se necesitan un contrato explícito de autenticación,
alojamiento de la sesión en almacenamiento seguro, orígenes/CORS autorizados,
enlaces profundos y recuperación de acceso. La cámara QR, calendarios del sistema,
notificaciones y funcionamiento sin conexión requieren pruebas y permisos nativos.
No incluir secretos de servidor en el paquete móvil ni guardar tokens en capturas.

No se crearon proyectos Android/iOS ni se añadieron plugins nativos. La revisión
actual cubre el navegador móvil y sus anchos; no certifica cámara física ni apps
nativas. El resultado de las comprobaciones y capturas se registra en
[validación de esta evolución](validacion-caudal-creativo.md).
