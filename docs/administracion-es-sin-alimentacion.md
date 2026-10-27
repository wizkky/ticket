# CaudalTickets CLP: administración en español

27 de octubre de 2026. Base: `f4a37c9`, rama `feature/clp-whole-pesos`.
Revisión: `feature/clp-admin-es-without-food`.

Esta revisión parte de la ticketera anterior al rediseño de Caudal Creativo.

## Administración

- Panel, estadísticas, enlaces rápidos, gráficos, estados y buscador en español.
- Identidad de administración de CaudalTickets.
- Español en el administrador incluso si el navegador o la cuenta tienen otro
  idioma. El frontend conserva su selección de idioma por usuario.
- Traducción de nombres de aplicaciones, modelos, grupos, encabezados, opciones
  y campos administrativos mediante un catálogo y adaptadores de presentación.
- Los nombres ingresados por las personas, identificadores, códigos técnicos y
  mensajes procedentes de servicios externos conservan sus valores originales.

La personalización utiliza `CaudalAdminSite`, basado en Unfold, y clases de
administración localizadas. Traduce metadatos al presentar formularios, tablas y
filtros; conserva valores de consultas, validadores, permisos y almacenamiento.
Las pequeñas adaptaciones de plantillas mantienen la atribución MIT de Unfold.

## Gestión alimentaria retirada

Se retiran los cuatro apartados de la captura original:

- Restricciones alimentarias.
- Preferencias alimentarias.
- Preferencias alimentarias de usuarios.
- Alimentos.

Se eliminan sus registros y formularios en el administrador, los campos anidados
alimentarios del usuario, los gestores del perfil y el resumen alimentario del
evento. También se retira la invitación a usar esa función en el acceso de invitados.

Las rutas `/api/dietary/*` y
`/api/events/{event_id}/dietary-summary` dejan de estar publicadas. El cliente
TypeScript se regeneró desde OpenAPI. Se retiraron los componentes y los archivos
de pruebas exclusivos de esos endpoints y pantallas eliminados.

Los modelos y las migraciones históricas permanecen para conservar la información
existente y la compatibilidad de las exportaciones. No se borraron tablas ni
registros alimentarios guardados. La coordinación de aportes compartidos
(`potluck`) es una función distinta y no forma parte de los cuatro apartados
retirados en esta revisión.

## Idioma predeterminado y migración

`LANGUAGE_CODE` pasa a español. La migración generada
`accounts.0036_default_spanish_language` cambia únicamente el valor predeterminado
del campo `language` a `es` para nuevas cuentas. No reemplaza el idioma guardado de
las cuentas existentes ni cambia precios, monedas o tickets.

Los catálogos `.po` se compilan mediante el script existente
`scripts/compile_translations.py`. No se necesitan nuevas dependencias.

## Comprobaciones realizadas

- Build de producción SvelteKit/Vite completado.
- TypeScript/Svelte: 0 errores; 377 advertencias pendientes de componentes de la base.
- Ruff en el Python modificado: sin errores.
- ESLint y Prettier en los componentes frontend modificados: correctos.
- `manage.py check`: sin incidencias.
- Migración aplicada en la base local y sin cambios de modelo pendientes.
- Cliente API regenerado y catálogos de traducción compilados.
- Inspección visual del administrador en navegador con idioma inglés: panel,
  listado de eventos y formulario de edición presentados en español.

No se ejecutaron suites de pruebas automatizadas ni nuevas reservas o check-in en
esta etapa. Las reservas, emisión, QR y lógica financiera no se modificaron. No se
reinició la base ni se desplegó públicamente.

[Captura del administrador](screenshots/caudal-clp-admin-es.png).

## Descargar esta revisión por primera vez en tu servidor

Desde el checkout existente, guardar primero cualquier cambio local propio. Los
siguientes comandos crean una rama local nueva a partir de la revisión remota,
incluso si el clon original descargó una sola rama:

```bash
cd /ruta/a/ticket
bash scripts/stop.sh
git fetch origin feature/clp-admin-es-without-food
git switch --create feature/clp-admin-es-without-food FETCH_HEAD
bash scripts/setup.sh
bash scripts/dev.sh
```

Si la rama local ya existe, usar en su lugar:

```bash
git switch feature/clp-admin-es-without-food
git pull --ff-only origin feature/clp-admin-es-without-food
```

Después de actualizar, ejecutar de nuevo `scripts/setup.sh` y `scripts/dev.sh`
para aplicar la migración, compilar las traducciones y reconstruir el frontend.
El setup conserva los `.env` y los volúmenes existentes. Mantener también los
archivos subidos de tu instalación. El procedimiento corresponde a la prueba
local Linux documentada en el README.
