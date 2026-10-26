# Validación de la primera evolución de Caudal Creativo

26 de octubre de 2026. Rama `feature/caudal-creativo-platform`, sobre `f4a37c9`.
Se revisó el frontend compilado para producción contra la API y la base local.
No se desplegó el sitio públicamente ni se configuraron pagos reales.

## Resultados

| Comprobación | Resultado |
| --- | --- |
| Build SvelteKit / Vite / adapter-node | Completado. Advertencias sobre tamaño de chunks y tiempos de plugins. |
| Tipos Svelte / TypeScript | 0 errores; 377 advertencias en el último recorrido, principalmente referencias iniciales a propiedades de componentes heredados. |
| Comprobación del verificador de tipos | Correcta: detectó errores deliberados tanto en `.ts` como en `.svelte`; los archivos temporales se retiraron. |
| Prettier y ESLint de archivos modificados | Correctos, sin errores ni advertencias de ESLint. |
| Traducciones | Estructura, equivalencias entre seis idiomas, compilación actualizada y ausencia de nuevas cadenas fuera del catálogo: correctas. `Agenda` se admite como término compartido en esos idiomas. |
| Pruebas seleccionadas del frontend | 49 aprobadas en seis archivos: categorías, filtros, continuidad CLP, ofertas, territorio, metadatos y renderizado SEO. |
| Django `check` | Sin incidencias. |
| API de roles y espacios Caudal | 11 pruebas aprobadas. Una advertencia heredada de Django sobre el esquema por defecto de URLField. |
| Prueba funcional HTTP/PDF/QR | 11 controles aprobados: autenticación, aislamiento, edición de tarifa CLP, reserva gratis, PDF, lectura óptica de QR, duplicado secuencial y simultáneo, reserva en puerta, cuenta y correo con PDF/ICS en Mailpit. |
| Recorrido principal de Chromium | 34 comprobaciones registradas; 0 errores de JavaScript. |
| Escritorio y móvil | Seis páginas públicas revisadas a 1440 y 390 px, más Mi Caudal y panel productor. Portada revisada en seis idiomas a 320, 390, 768, 1024, 1280 y 1440 px. Sin desbordamiento horizontal en esas vistas. |
| Navegación | Buscador real, categoría sin resultados, calendario con etiquetas y persistencia de categoría al cambiar mes; limpiar categoría conserva el modo calendario. Menú móvil con foco contenido, Escape y retorno del foco. |
| Temas y movimiento | Tema claro persistente, pausa persistente y respeto de movimiento reducido. El símbolo original deja de animarse con movimiento reducido. |
| Accesibilidad automática | Ocho revisiones Axe WCAG 2 A/AA y 2.1 AA sin infracciones: seis páginas públicas en escritorio, portada clara móvil y Mi Caudal. |
| Contraste de temas | 0 fallos WCAG y 0 pares confundibles en la auditoría existente de tokens. |
| Acceso protegido | Comprador y productor sin acceso a administración general; productor B sin acceso al panel A. Administrador de plataforma conserva su panel. |
| Creación y edición en navegador | Borrador nuevo, guardado, dos tarifas CLP gratuitas/en puerta y edición posterior: correctos. Solo se eliminaron los borradores creados por estas pruebas. |
| Compra en navegador | Reserva gratuita y reserva en puerta por $5.000 completadas. Confirmación y entrada con PDF/QR accesibles; precio visible sin decimales. |
| Retiro de Emergia | Sin coincidencias en textos visibles ni logos de las páginas recorridas; sin referencias en el código público de interfaz. Activo histórico conservado sin uso visible. |
| Tokens en HTML | Comprobador existente sin fugas de access tokens en cargas SSR. |
| Límite general de longitud de archivos | No aprobado: `TierForm.svelte` tiene 757 líneas, frente al máximo 750. Ya tenía esas 757 líneas en `f4a37c9`; no se modificó en este rediseño. Los nuevos archivos respetan el límite. |

No se ejecutó la suite completa del monorepo ni una auditoría integral de seguridad,
rendimiento o accesibilidad. Las cuentas, contraseñas, sesiones y logs completos
permanecen en `.local/`, fuera de Git.

La primera pasada rápida de navegador recibió HTTP 429 por superar el límite de
solicitudes de la API. Se espació el recorrido y se reutilizó la página al revisar
anchos; la repetición completa terminó correctamente. No se deshabilitaron las
protecciones de la aplicación. Las pruebas de formularios esperaron la hidratación
del cliente antes de interactuar; los borradores de los intentos se retiraron.

Las reservas y los check-in de prueba agregan entradas y registros a la base local.
Se conservaron los anteriores. Las reservas en puerta no generaron pagos online ni
prueban recepción de efectivo. No se modificó el servicio de emisión ni su bloqueo
para impedir el doble ingreso.

## Capturas

| Vista | Escritorio | Móvil |
| --- | --- | --- |
| Caudal Creativo | [Ver](screenshots/caudal-v4-home-desktop.png) | [Ver](screenshots/caudal-v4-home-mobile.png) |
| Caudal Agenda | [Ver](screenshots/caudal-v4-agenda-desktop.png) | [Ver](screenshots/caudal-v4-agenda-mobile.png) |
| Comunidad | [Ver](screenshots/caudal-v4-comunidad-desktop.png) | [Ver](screenshots/caudal-v4-comunidad-mobile.png) |
| Ecosistema | [Ver](screenshots/caudal-v4-ecosistema-desktop.png) | [Ver](screenshots/caudal-v4-ecosistema-mobile.png) |
| Explorar | [Ver](screenshots/caudal-v4-catalogo-desktop.png) | [Ver](screenshots/caudal-v4-catalogo-mobile.png) |
| Caudal Tickets | [Ver](screenshots/caudal-v4-tickets-desktop.png) | [Ver](screenshots/caudal-v4-tickets-mobile.png) |
| Mi Caudal | [Ver](screenshots/caudal-v4-mi-caudal-desktop.png) | [Ver](screenshots/caudal-v4-mi-caudal-mobile.png) |
| Productor | [Ver](screenshots/caudal-v4-productor-desktop.png) | [Ver](screenshots/caudal-v4-productor-mobile.png) |

[Portada clara móvil](screenshots/caudal-v4-home-light-mobile.png) ·
[Confirmación gratuita](screenshots/caudal-v4-confirmacion-free.png) ·
[Confirmación con pago en puerta](screenshots/caudal-v4-confirmacion-at_the_door.png).

## Reproducción

Usar el checkout y las dependencias existentes. Antes de reconstruir el frontend,
detenerlo; reiniciar cuando termine el build:

```bash
bash scripts/stop.sh
source scripts/common.sh
(cd apps/web && corepack pnpm paraglide:compile && corepack pnpm build)
bash scripts/dev.sh
```

En otra terminal, desde la raíz:

```bash
bash scripts/smoke.sh
node scripts/review_creative.mjs
```

El recorrido de navegador usa `@playwright/test`, Axe y Chromium del entorno
(`/usr/bin/chromium`, configurable mediante `CHROMIUM_EXECUTABLE_PATH`). Necesita
las cuentas locales ya preparadas en `.local/demo-credentials.json`. Sus resultados
se guardan en `.local/creative-review.json` y las capturas en `docs/screenshots/`.

Pruebas seleccionadas:

```bash
# apps/web, con scripts/common.sh cargado
corepack pnpm exec vitest run src/lib/caudal/caudal.test.ts src/lib/caudal/categories.test.ts src/lib/seo/build.test.ts src/lib/seo/types.test.ts src/lib/seo/SeoHead.test.ts src/lib/seo/text.test.ts
# apps/api, con scripts/common.sh cargado
uv run --frozen pytest src/events/tests/test_controllers/test_caudal_controller.py --no-cov -q
```

## Riesgos y límites

- Las categorías dependen de etiquetas editoriales exactas. No clasifican por sí
  solas el catálogo ni constituyen un catastro de Valdivia.
- Las selecciones públicas de organizaciones y lugares son parciales, con errores
  y vacíos explícitos. No acreditan convenios ni relaciones exclusivas.
- La nueva carga de organizaciones agrega una consulta pública a la portada,
  paralela a la carga de actividades y con timeout. Se debe medir rendimiento con
  un catálogo representativo antes de operar públicamente.
- El calendario existente no incorpora todavía el motor de Caudal Agenda.
  Cursos, recurrencias avanzadas, matrículas, mensualidades, horarios individuales
  y perfiles de profesionales siguen pendientes.
- El navegador móvil revisado no sustituye pruebas con cámaras físicas ni una
  aplicación Android/iOS. La propuesta de integración móvil y los contratos de
  modelos pendientes están en [la documentación de implementación](evolucion-caudal-creativo.md).
