# Revisión de CaudalTickets: Chile, limpieza y regresiones

27 de octubre de 2026. Rama: `feature/clp-admin-es-without-food`.
Continúa la versión CLP y la administración en español.

## Cambios

- Django y Celery usan `America/Santiago` como zona predeterminada, incluido el
  cambio de hora de Chile. `USE_TZ` permanece activo: las fechas almacenadas no
  se desplazan ni se reescriben. Los eventos conservan su zona propia y los
  cronogramas existentes con zona explícita conservan esa configuración.
- Los listados de tarifas, entradas, pagos, abonos de eventos, descuentos fijos,
  facturas y notas de crédito presentan CLP como `$5.000` y `$5.500`. Se reutiliza
  el formateador de documentos; las monedas históricas mantienen su precisión.
  Los porcentajes y los campos numéricos internos conservan sus reglas actuales.
- La portada presenta Caudal Creativo, La Factoría y El Subte. Se retiró Emergia
  de la presentación y se reajustó la grilla móvil. Los archivos históricos y su
  procedencia se conservan.
- Se eliminó el acceso al Grafana de Revel desde el panel general.
- A solicitud del usuario se ocultan aportes compartidos, Telegram, referidos y
  membresías en la navegación y los puntos de entrada principales. Incluye los
  editores integrados del administrador, el perfil, el registro, la ficha pública
  y los ajustes del productor. Los controles ocultos de formularios conservan los
  valores guardados; los ajustes de contacto del productor siguen disponibles.
- Los modelos, datos, servicios y permisos de esos módulos permanecen. Ocultar
  una sección no desactiva sus API ni el acceso directo autorizado a su historial.
  Tampoco cancela membresías o notificaciones existentes.
- Se extrajo la sección de devoluciones del formulario de tarifas. Todos los
  archivos del frontend cumplen ahora el límite de tamaño configurado.
- Se explicitó la inicialización única del formulario de tarifas: sus campos
  editables se cargan al abrir el diálogo. Las reglas y validaciones permanecen
  reactivas. Se resolvieron además tres errores de tipado del adaptador del admin.
- Se corrigió la doble ejecución de los gráficos del panel: el bloque de scripts
  estaba anidado dentro del contenido y Django lo renderizaba dos veces. Ahora se
  renderiza una sola vez.

Para volver a mostrar las interfaces opcionales, configurar **ambas** variables
y reiniciar los servicios:

```dotenv
# apps/api/.env
CAUDAL_SHOW_OPTIONAL_MODULES=True
# apps/web/.env
PUBLIC_CAUDAL_SHOW_OPTIONAL_MODULES=true
```

Sin estas variables, los módulos se ocultan por defecto. No hay nuevas
dependencias ni migraciones de datos en esta revisión.

## Validación

Las pruebas de API usan una base de pruebas separada. Los recorridos HTTP y de
navegador usan la demostración local: generan reservas y admisiones reales de
prueba, conservando las compras anteriores. Solo se eliminan los borradores
privados creados durante la revisión.

| Comprobación | Resultado |
| --- | --- |
| API seleccionada | 25 pruebas aprobadas: CLP, moneda histórica, horario de verano/invierno, español, permisos, módulos ocultos, valores guardados y gráficos. |
| Frontend seleccionado | 65 pruebas aprobadas: precios, entradas monetarias, módulos, formularios, devoluciones, ventanas de ingreso y reglas de eventos. |
| TypeScript / Svelte | 0 errores; 334 advertencias, frente a las 377 anteriores. |
| Tipado Python | Mypy sin errores en los 8 archivos administrativos revisados. |
| Formato y lint | Ruff, ESLint y Prettier correctos en los archivos modificados. |
| Tamaño de archivos | Todos los archivos fuente del frontend dentro de los límites configurados. |
| Recorrido HTTP | 11 controles aprobados: autenticación, permisos entre productores, edición CLP, reserva gratuita y en puerta, PDF, QR, duplicados secuenciales/simultáneos y correo en Mailpit con PDF/ICS. |
| Navegador | 24 comprobaciones aprobadas: vistas móviles/escritorio, permisos, horarios, precios, creación y edición de borradores, reservas gratuitas/en puerta y control de admisión. Sin errores JavaScript en las vistas revisadas. |
| Accesibilidad automática | Axe WCAG 2 A/AA y 2.1 AA sin infracciones en portada y panel productor a 390 px. |
| Django | Comprobación sin incidencias y sin migraciones de modelo pendientes. |

Las 334 advertencias restantes corresponden a 281 avisos de referencias iniciales
en componentes heredados y 53 avisos CSS por `@apply`. No se ocultaron advertencias
para obtener este resultado. Deben revisarse por componente en futuras mejoras;
no equivalen por sí solas a fallos de compra.

La revisión del navegador usa el build final de producción de esta misma revisión.
El control móvil se ejecutó en Chromium con una vista de 390 px: se verificó la
confirmación manual de admisión, el foco del diálogo, Escape, el QR ya utilizado y
un código inexistente. Esta validación no demuestra el funcionamiento de una
cámara física ni habilita pagos online.

## Capturas

| Vista | Escritorio | Móvil |
| --- | --- | --- |
| Portada | [Ver](screenshots/caudal-revision-home-1440.png) | [Ver](screenshots/caudal-revision-home-390.png) |
| Productor | [Ver](screenshots/caudal-revision-productor-1440.png) | [Ver](screenshots/caudal-revision-productor-390.png) |
| Administración general | [Ver](screenshots/caudal-revision-admin-1440.png) | [Ver](screenshots/caudal-revision-admin-390.png) |

[Listado administrativo de precios](screenshots/caudal-revision-precios-admin.png).

## Actualizar tu prueba local

Desde la raíz del clon existente, guarda tus modificaciones locales propias antes
de cambiar de rama. Conserva los `.env`, archivos subidos y el respaldo habitual
de tu base.

```bash
git status
bash scripts/stop.sh
git fetch origin feature/clp-admin-es-without-food
git switch feature/clp-admin-es-without-food
git pull --ff-only origin feature/clp-admin-es-without-food
bash scripts/setup.sh
bash scripts/dev.sh
```

Si esa rama aún no existe en tu clon, sustituye el `git switch` anterior por
`git switch --create feature/clp-admin-es-without-food FETCH_HEAD`.

El procedimiento corresponde al entorno local Linux del README. `setup.sh`
conserva los archivos de entorno y volúmenes existentes, aplica las migraciones
pendientes de revisiones anteriores, compila traducciones y reconstruye el sitio.
No usar los comandos de reset de la base. Los servicios que se inicien manualmente
en tu servidor deben reiniciarse también para cargar la configuración nueva.

Para repetir las verificaciones funcionales sobre la demostración ya iniciada:

```bash
bash scripts/smoke.sh
```

La configuración de pagos online, la cámara de teléfonos reales y la operación
pública no forman parte de estos tres pasos.
