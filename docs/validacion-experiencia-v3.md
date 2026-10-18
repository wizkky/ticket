# Validación de recorridos CaudalTickets

Fecha: 18 de octubre de 2026. Rama: `feature/caudal-complete-experiences`,
continuación de `205b693` (identidad visual Caudal).

## Comprobaciones

| Comprobación | Resultado |
| --- | --- |
| Compilación de producción | SvelteKit / Vite / adapter-node completados. |
| TypeScript / Svelte | 0 errores; permanecen 368 advertencias, principalmente de componentes heredados. |
| ESLint en archivos del frontend modificados | Sin errores. |
| Ruff y comprobación de Django | Sin errores. |
| Pruebas nuevas de API | 11 aprobadas: autenticación, roles, aislamiento, permisos revocados, métricas y ubicación efectiva del evento. |
| Pruebas seleccionadas de frontend | 84 aprobadas: territorio, precios, filtros, sanitización y documentos insertables. |
| Traducciones | Validación estructural, textos nuevos y equivalencias entre seis idiomas aprobadas. Los nombres geográficos idénticos se permiten expresamente. |
| Contraste del sistema de temas | 0 fallos WCAG y 0 pares confundibles en la auditoría existente de ambos temas. |
| Prueba HTTP completa | 11 comprobaciones aprobadas: reserva gratis, PDF, lectura óptica del QR, aislamiento, duplicados secuenciales y simultáneos, pago en puerta y correo con PDF/ICS en Mailpit. |
| Navegador de producción | Chromium, escritorio de 1440 px y móvil de 390 px; 20 vistas sin desbordamiento horizontal. |
| Permisos en navegador | Comprador y productor reciben 403 en administración general; el productor B no accede al panel A. |
| Herramientas generales | Acceso con la cuenta de administrador al listado real de organizaciones de Django. |
| Accesibilidad automática | Axe WCAG 2 A/AA y 2.1 AA: sin infracciones en los paneles productor y general y en la portada clara móvil revisados. |

No equivale a una auditoría integral de seguridad, accesibilidad o rendimiento.
La revisión automática de colores cubre las combinaciones declaradas por el sistema
de temas, y Axe cubre las pantallas indicadas.

## Recorridos ejecutados en navegador

- Crear un borrador, guardar su ubicación, configurar una tarifa gratuita y otra en
  puerta, volver a editar y guardar. Los borradores de revisión se eliminaron al
  finalizar; no se publicaron eventos adicionales.
- Reservar una entrada gratuita y una con pago en puerta, completar el nombre del
  titular, comprobar la confirmación y abrir la entrada con su PDF y QR.
- Filtrar por Valdivia y comprobar una búsqueda sin resultados.
- Pausar movimiento, recargar y comprobar la persistencia de la preferencia.
- Cambiar el tema con teclado, cerrar con Escape y recuperar el foco; conservar el
  tema claro tras recargar, respetar movimiento reducido y recorrer el menú móvil
  con el foco contenido. Comprobar un título largo sin desbordamiento.
- Usar la puerta desde la vista móvil: foco contenido en el diálogo, Escape,
  confirmación de admisión, QR ya usado deshabilitado y mensaje ante un código
  inexistente. El formulario manual cabe en 390 px.

La reserva en puerta de Revel puede emitirse como `active`: se trata de una
entrada habilitada, sin `Payment` online. Ni esa emisión ni su admisión se cuentan
como pago online. El productor comprueba el cobro presencial por separado.

Cada ejecución de reservas y check-in deja entradas de prueba reales y registros
en la base local. La revisión final registró 29 comprobaciones de páginas, permisos
y accesibilidad sin errores de JavaScript, más seis comprobaciones de tema,
movimiento y navegación. No se borraron compras anteriores. Los secretos, sesiones,
correos y artefactos de las pruebas permanecen en `.local/`, excluidos de Git.

## Capturas

Todas corresponden a datos de demostración y al frontend compilado para producción.

| Pantalla | Escritorio | Móvil |
| --- | --- | --- |
| Portada | [Ver](screenshots/caudal-v3-home-desktop.png) | [Ver](screenshots/caudal-v3-home-mobile.png) |
| Catálogo | [Ver](screenshots/caudal-v3-catalogo-desktop.png) | [Ver](screenshots/caudal-v3-catalogo-mobile.png) |
| Ficha de evento | [Ver](screenshots/caudal-v3-evento-desktop.png) | [Ver](screenshots/caudal-v3-evento-mobile.png) |
| Acceso | [Ver](screenshots/caudal-v3-acceso-desktop.png) | [Ver](screenshots/caudal-v3-acceso-mobile.png) |
| Registro | [Ver](screenshots/caudal-v3-registro-desktop.png) | [Ver](screenshots/caudal-v3-registro-mobile.png) |
| Mis entradas | [Ver](screenshots/caudal-v3-entradas-desktop.png) | [Ver](screenshots/caudal-v3-entradas-mobile.png) |
| Panel productor | [Ver](screenshots/caudal-v3-productor-desktop.png) | [Ver](screenshots/caudal-v3-productor-mobile.png) |
| Editor | [Ver](screenshots/caudal-v3-editor-desktop.png) | [Ver](screenshots/caudal-v3-editor-mobile.png) |
| Puerta y QR | [Ver](screenshots/caudal-v3-puerta-desktop.png) | [Ver](screenshots/caudal-v3-puerta-mobile.png) |
| Administración general | [Ver](screenshots/caudal-v3-administracion-desktop.png) | [Ver](screenshots/caudal-v3-administracion-mobile.png) |

[Tema claro móvil](screenshots/caudal-v3-claro-mobile.png) ·
[Confirmación gratuita](screenshots/caudal-v3-confirmacion-free.png) ·
[Confirmación de reserva en puerta](screenshots/caudal-v3-confirmacion-at_the_door.png).

## Reproducción en este entorno

Usar el checkout y sus dependencias ya instaladas. No es necesario reinstalar.

```bash
bash scripts/dev.sh
bash scripts/smoke.sh
```

Antes de reconstruir el frontend, detenerlo con `bash scripts/stop.sh`. La
compilación reemplaza los archivos que sirve adapter-node; arrancar otra vez con
`scripts/dev.sh` únicamente cuando termine todo el build.

Las cuentas para una revisión privada se encuentran en `.local/demo-credentials.json`.
No copiar ese archivo a Git ni incluir sus valores en capturas o informes.

Los esquemas del cliente se regeneraron desde Django:

```bash
# apps/api, con scripts/common.sh cargado
uv run --frozen python src/manage.py dump_openapi
# apps/web
BACKEND_SPEC=/workspace/ticket/apps/api/.artifacts/openapi.json corepack pnpm generate:api
```

Las pruebas de API específicas están en
`apps/api/src/events/tests/test_controllers/test_caudal_controller.py` y las de
territorio/ofertas/filtros en `apps/web/src/lib/caudal/caudal.test.ts`.

## Pendiente

CLP, pagos online, liquidaciones, operación pública y perfiles/mercado creativo.
Falta probar la cámara física en teléfonos del equipo. Las herramientas avanzadas
de Django mantienen su sesión y presentación propias. Continúan los límites y
avisos heredados registrados en [la validación de la base](validacion-prueba.md).
No se contrataron servicios ni se publicó un despliegue.
