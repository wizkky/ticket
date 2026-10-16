# CaudalTickets: costos, licencias y selección ampliada

Revisión documental del 16 de octubre de 2026. Complementa y actualiza la [investigación inicial](investigacion-bases-ticketing.md).

## Resultado

Podemos usar código existente como primera base de CaudalTickets y ofrecer un producto comercial, cumpliendo la licencia de la edición elegida. Contratar el servicio alojado del autor no es un requisito general para ejecutar las ediciones abiertas en infraestructura propia.

La ampliación incorpora tres candidatos relevantes: **Revel**, **Event Schedule** y **TiBillet**. También se revisaron Eventmie Lite y Nosht, descartados de la selección principal. Revel pasa a ser el primer candidato para una prueba técnica de producto propio; pretix conserva el mejor respaldo documental de mantenimiento y operación entre los finalistas; Hi.Events sigue siendo una alternativa funcional atractiva.

Ninguna aplicación ha sido instalada, ejecutada ni auditada por esta investigación. Se revisaron fuentes oficiales, licencias, manifiestos, lockfiles, configuración de CI y avisos públicos. La existencia de un workflow no prueba que la última ejecución haya pasado.

## Qué se paga y qué no

Hay cuatro costos distintos:

1. **Licencia del código o de módulos:** depende de la edición. Las ediciones abiertas comparadas permiten uso sin canon, bajo sus condiciones. Algunos módulos comerciales requieren compra.
2. **Servicio alojado:** el proveedor opera servidores, actualizaciones y soporte. Puede cobrar mensualidad, comisión por ticket/pedido o ambas. Es opcional si elegimos autoalojamiento.
3. **Nuestra operación:** servidor, base de datos, almacenamiento, correo de tickets, copias de seguridad, dominio, observabilidad y mantenimiento.
4. **Cobro del dinero:** comisiones de la pasarela, posibles servicios de pagos a productores y devoluciones. Autoalojar no elimina esos costos.

No existe un presupuesto de infraestructura de CaudalTickets todavía: depende del tráfico, concurrencia, disponibilidad y país de operación. Las integraciones Stripe documentadas no demuestran compatibilidad con nuestra futura entidad comercial o pasarela local.

| Proyecto | Código autoalojado | Qué puede generar un pago al proveedor |
| --- | --- | --- |
| Hi.Events | Core sin canon; AGPL con atribución. | Cloud, retirada de atribución y funcionalidades Enterprise, incluidas butacas reservadas y taquilla para eventos reales. Son permisos distintos. |
| pretix | Community sin canon; AGPL con atribución. | Hosted, soporte y plugins/edición Enterprise. La documentación Enterprise solicita estimación anual de entradas y cantidad de servidores. |
| Eventyay | Repositorio principal Apache-2.0 sin canon; comprobar plugins elegidos. | Alojamiento y servicios de soporte. No se confirmó una tarifa vigente. |
| alf.io | Core GPL-3.0 sin canon. | Swicket, su oferta premium administrada, y servicios opcionales. |
| Attendize | AAL sin canon conservando atribución. | Marca blanca y soporte comercial, según su documentación. Importes no confirmados. |
| Revel | Backend y frontend MIT; el README declara ningún cargo a Revel por autoalojar. | Su servicio alojado cobra comisión por pedidos pagados online y membresías. |
| Event Schedule | AAL; README declara todas las funciones incluidas al autoalojar, sin claves de activación ni comisión de plataforma. | Su servicio alojado tiene plan gratuito y planes pagados. Importes no confirmados. |
| TiBillet | Código AGPL-3.0 sin canon. | La cooperativa ofrece alojamiento y acompañamiento; no se confirmó una tarifa vigente. |

### Cifras verificadas y límite de acceso

El [README oficial de Revel](https://github.com/letsrevel/revel-backend#fees-and-data), consultado en esta revisión, publica:

- **Autoalojado:** nada a Revel; infraestructura y procesador de pagos aparte.
- **Alojado, pedidos pagados online:** 1,5 % + 0,25 EUR **por pedido** para Revel, más Stripe y el IVA aplicable a su comisión.
- Su ejemplo para tarjetas estándar del Espacio Económico Europeo combina Revel y Stripe: **3 % + 0,50 EUR por pedido**. No es una tarifa aplicable automáticamente a Chile ni a otros países.
- **Membresías alojadas:** 1,5 % para Revel sin componente fijo, más Stripe.
- Su tarifa fija por pedido se cobra una vez aunque ese pedido incluya varias entradas.

Las conexiones a páginas externas de precios de Hi.Events, pretix, alf.io y Event Schedule fueron bloqueadas por el proxy del entorno. No fue posible corroborar allí precios comerciales vigentes. No se usan las cifras comparativas que un competidor publica sobre otro proveedor como confirmación de sus precios actuales.

Los enlaces para una futura comprobación directa son [Hi.Events pricing](https://hi.events/pricing), [Hi.Events licensing](https://hi.events/licensing), [pretix pricing](https://pretix.eu/about/en/pricing/), [Event Schedule pricing](https://eventschedule.com/pricing) y [Swicket](https://swicket.io).

## Qué implican las licencias para nuestro primer código

- **MIT, Revel:** permite copiar, modificar, distribuir y comercializar, conservando avisos de copyright y licencia. No impone publicar nuestras modificaciones. Revisar también dependencias, imágenes y datos incluidos; por ejemplo Revel identifica bases geográficas con atribución CC BY.
- **Apache-2.0, Eventyay:** permite modificaciones y comercialización sin una obligación general de publicar el derivado; se deben conservar los avisos aplicables, incluido NOTICE, e identificar cambios conforme a sus términos. Los plugins pueden tener otras licencias.
- **AGPL, Hi.Events/pretix/TiBillet:** permite vender servicios y usar el código comercialmente. Una versión cubierta modificada ofrecida por red debe ofrecer su código fuente correspondiente a sus usuarios. Esto no significa publicar credenciales ni bases de datos. El alcance de una obra combinada debe evaluarse; usar una API no resuelve por sí solo esa cuestión.
- **GPL-3.0, alf.io:** permite uso comercial. El uso de un servidor por red, por sí solo, no activa la obligación adicional de AGPL; distribuir software cubierto sí tiene obligaciones sobre código y licencia. Los componentes entregados al cliente requieren su propia revisión.
- **AAL, Attendize/Event Schedule:** permiten uso y modificaciones con obligaciones de atribución. No son MIT. Debe revisarse y conservarse el texto exacto de cada proyecto antes de redistribuir o cambiar su presentación.

En pretix, la excepción de ciertas obligaciones de interacción por red excluye SaaS y venta para terceros. Esto **no prohíbe** usar pretix para CaudalTickets: significa que esa excepción no nos libera de las obligaciones AGPL aplicables. Hi.Events añade atribución visible en páginas y correos, y sus directorios Enterprise tienen licencia separada.

## Detalle de los cinco proyectos iniciales

### Hi.Events

**Aporta:** páginas de eventos y organizador, múltiples tipos de entrada, promociones, PDF, escaneo QR con registros, roles, estadísticas, reembolsos, Stripe Connect, REST API y webhooks. Laravel/PHP, React/TypeScript, PostgreSQL y Redis son una base adecuada para personalizar interfaz y backend por separado.

**Límites:** el core exige AGPL y atribución. Butacas reservadas y taquilla están en módulos Enterprise de uso productivo comercial. La publicación observada v2.0.0-rc.2 sigue siendo preliminar; una numeración 2.0 no la convierte en estable.

**Seguridad y mantenimiento:** política de reporte, PHPUnit, Playwright E2E y Dependabot configurados. Sus advisories de 2026 publicaron y declararon correcciones para inyección SQL en ordenamiento, compra de tickets ocultos y XSS almacenado. Hay que elegir una revisión con esos parches y probar los permisos entre productores; esta revisión no certifica que estén resueltos todos los riesgos.

**Encaje:** finalista si queremos React/Laravel y aceptamos su esquema de licencias y funciones comerciales.

### pretix

**Aporta:** especialización en venta y control de accesos, panel administrativo, permisos por equipos y eventos, REST API, plugins, dispositivos de validación y documentación de idempotencia y concurrencia. Existe aplicación pretixSCAN separada. Python/Django con frontend integrado; no es de origen una aplicación React.

**Límites:** AGPL y atribución; varios plugins avanzados son comerciales. Crear una experiencia pública propia y el mercado creativo exige desarrollo adicional. Las opciones de reingreso/check-in deben configurarse para nuestro modelo.

**Seguridad y mantenimiento:** política de soporte de estable y dos versiones anteriores; pruebas con distintas versiones de Python y bases de datos, concurrencia, Playwright y generación de inventario SBOM. Su documentación declara un sistema de gestión ISO 27001 para la empresa y sus procesos; eso no certifica una futura instalación nuestra. Publica vulnerabilidades y correcciones: hubo fallas de autenticación, validación de checkout y exposición de registros de escaneo corregidas en 2026. La versión observada 2026.8.0 queda fuera de los rangos afectados de los tres ejemplos enlazados abajo.

**Encaje:** finalista cuando pesen más la trayectoria operativa, los dispositivos de acceso y el proceso de mantenimiento. No debe juzgarse negativamente por publicar más CVE que un proyecto pequeño: la transparencia y corrección son señales relevantes.

### Eventyay

**Aporta:** ticketing, organizadores, cuentas, agenda, ponentes, vídeo, API y extensiones. Su licencia principal Apache-2.0 facilita crear un derivado propio sin la obligación de apertura de AGPL. Combina Django, PostgreSQL, Redis/Celery y módulos Vue/Vite.

**Límites:** la plataforma unificada incorpora más componentes de los necesarios para el primer MVP. El escáner y algunas pasarelas son plugins separados. El README anuncia Django 5.2, pero el manifiesto dev exige Django >=6.0.8,<6.1 con Python 3.12; fijar la revisión y comprobar su instalación es necesario.

**Seguridad y mantenimiento:** Dependabot diario, lockfile y controles de build. No se encontró SECURITY.md en dev. Hay workflows antiguos con ramas/rutas previas a la reorganización; el workflow actual de recolección de tests usa `pytest --collect-only`, lo cual no equivale a ejecutar los tests. No afirmar que su suite de integración está pasando sin comprobar los trabajos correctos.

**Encaje:** alternativa permisiva si la prueba técnica confirma integración y calidad de la nueva base. Queda detrás de los tres finalistas por costo e incertidumbre de adaptación.

### alf.io

**Aporta:** reservas, tienda, backoffice, administración de asistentes y un ecosistema de check-in con aplicaciones y estaciones. Licencia GPL-3.0. La rama main actual requiere Java 25 y PostgreSQL; su arquitectura se aparta del enfoque React/Svelte más familiar para una interfaz muy personalizada.

**Límites:** su política soporta 2.0-M5 y recomienda una release publicada; main se considera trabajo en curso. Swicket es la oferta premium administrada, opcional para usar el core abierto.

**Seguridad y mantenimiento:** tiene política y advisories públicos. En septiembre de 2026 corrigió fallas de autorización entre organizaciones en la versión 2.0-M5-2609. Una de ellas permitía modificar metadatos financieros de otra organización; otra exponía datos de asistentes en escaneos de patrocinadores. Son ejemplos pertinentes para exigir aislamiento entre productores en nuestro prototipo.

**Encaje:** alternativa real si elegimos Java o necesitamos su operativa específica. No es el primer candidato para el desarrollo propuesto.

### Attendize

**Aporta:** múltiples organizadores, páginas de eventos, venta, QR y escáner de navegador, pagos, reembolsos, estadísticas y cargos de servicio.

**Límites:** su última actividad observada es de enero de 2023. El manifiesto develop sigue requiriendo PHP ^7.3 y Laravel ^6.5, además de dependencias antiguas. El esfuerzo de actualización sería considerable para una plataforma nueva que manejará pagos y datos personales. AAL exige atribución; existen ofertas comerciales de marca blanca.

**Encaje:** referencia de funcionalidades y flujos. Se descarta como base principal actual por antigüedad de la plataforma y falta de mantenimiento reciente observado.

## Nuevas alternativas con potencial

### Revel

**Repositorios:** [backend](https://github.com/letsrevel/revel-backend), [frontend](https://github.com/letsrevel/revel-frontend), [infraestructura](https://github.com/letsrevel/infra).

**Aporta:** múltiples organizaciones, paneles de organizador y comprador, eventos públicos/privados, membresías recurrentes, asientos, QR/PDF, Apple/Google Wallet, escaneo, reembolsos, listas de espera y Stripe Connect con cobro directo al organizador. Incluye español. Su orientación a comunidades, salas y artistas tiene afinidad con Caudal.

**Base técnica:** Django 5.2 LTS, Python 3.14, Django Ninja, PostgreSQL/PostGIS, Celery/Redis; frontend SvelteKit 2/Svelte 5 con TypeScript. Backend y frontend MIT. No exige adoptar su alojamiento ni su comisión para autoalojar.

**Seguridad observada:** política pública, Bandit, pip-audit, auditoría nocturna de dependencias y pruebas con un umbral configurado de cobertura de ramas de 90 %. Documenta 2FA TOTP y análisis ClamAV opcional de archivos. Estos son controles y políticas inspeccionados, no resultados que hayamos ejecutado nosotros ni una auditoría independiente.

**Límites:** proyecto joven, equipo/comunidad pequeños y clasificación Beta en el manifiesto, aunque tenga releases frecuentes. La política concentra correcciones en main, sin mantenimiento extendido de tags. La infraestructura incluye dependencias geográficas y servicios adicionales; no es un frontend pequeño listo para copiar sin operación de backend. Hay que demostrar aislamiento, concurrencia de aforo, pagos y validación QR.

**Encaje:** primer candidato para una prueba técnica si queremos una base moderna que permita desarrollo comercial propio sin copyleft. No se recomienda todavía como servicio listo para cobrar ventas reales.

### Event Schedule

**Repositorio:** [eventschedule/eventschedule](https://github.com/eventschedule/eventschedule).

**Aporta:** calendarios de sala, artista y curador, descubrimiento de eventos, seguidores, newsletters, venta de entradas, QR, butacas, equipos, API/webhooks y modo SaaS para terceros. Es una de las propuestas más cercanas a conectar artistas, salas y audiencias. El README declara autoalojamiento gratuito con todas las funciones incluidas y sin comisión de plataforma.

**Base técnica y licencia:** PHP/Laravel, Vue 3, Tailwind y MySQL/MariaDB; AAL con obligaciones de atribución.

**Límites concretos:** el lockfile fija Laravel 11.55.1, cuya rama terminó soporte de seguridad el 12 de marzo de 2026 según la política oficial. En el workflow inspeccionado, `composer audit` está comentado con un TODO. Sí hay pruebas, 2FA, registros de auditoría y webhooks HMAC, pero estas señales no compensan por sí solas una rama del framework fuera de soporte.

**Encaje:** prometedor para estudiar el modelo artista/sala/curador. No elegirlo para producción sin actualizar framework y revisar dependencias.

### TiBillet / Lespass

**Repositorio:** [TiBillet/Lespass](https://github.com/TiBillet/Lespass).

**Aporta:** ticketing QR, espacios y agendas federados, membresías, POS, tarjetas NFC, monedero compartido, monedas locales y moneda tiempo intercambiable por servicios. Este último concepto tiene especial afinidad con el intercambio creativo de Caudal, aunque no sea el mercado de perfiles/portafolios completo que queremos.

**Base técnica y licencia:** Django, Python, PostgreSQL, Redis/Celery y HTMX/Bootstrap, bajo AGPL-3.0. El proyecto declara uso en producción desde 2018; es una declaración de sus autores, no una comprobación independiente de esta investigación.

**Límites concretos:** el lockfile revisado usa Django 4.2.30, rama fuera de soporte desde abril de 2026. El README menciona PostgreSQL 13, también una versión antigua sin soporte vigente. Está unificando servicios en un monorepo y su documentación es principalmente francesa. La combinación de ticketing, POS y finanzas comunitarias agrega alcance operativo y técnico.

**Encaje:** referencia especialmente útil para comunidad, federación e intercambio. Para usarlo como base habría que asumir actualización de dependencias y mayor adaptación.

### Otras dos opciones revisadas y descartadas

- [Eventmie Lite](https://github.com/classiebit/eventmie): su edición MIT gratuita reserva la venta de eventos pagados a ediciones Pro comerciales y parte del escaneo a niveles superiores, según su tabla oficial. Vue 2.7 y dependencias antiguas reducen su atractivo. No confundir las funciones anunciadas del producto comercial con las del repositorio abierto.
- [Nosht](https://github.com/samuelcolvin/nosht): ticketing MIT real, pero último commit observado de octubre de 2021 y documentación Python 3.6/Create React App. La actualización no se justifica frente a candidatos activos.

## Seguridad: qué se ha comprobado y qué falta

No se clasifica ningún proyecto como seguro por ser popular, reciente o escrito con un framework moderno. Tampoco se compara seguridad contando avisos públicos: un proyecto que publica y corrige vulnerabilidades puede tener un proceso más transparente que otro sin avisos.

Para elegir una base, la siguiente prueba técnica debe verificar al menos:

1. **Aislamiento:** un productor no accede a eventos, asistentes, archivos, reportes o pagos de otro, tampoco cambiando identificadores en la API.
2. **Entradas y aforo:** no sobreventa con compras simultáneas; QR imposible de adivinar; dos escáneres concurrentes no admiten dos veces la misma entrada cuando la política prohíbe reingreso.
3. **Dinero:** firmas y reintentos de webhooks, idempotencia, importe calculado por servidor, confirmación de pago por proveedor, reembolsos y conciliación de comisiones.
4. **Cuentas y administración:** 2FA para productores/administración, recuperación de acceso, permisos de escaneo y cargas de archivos.
5. **Operación:** dependencias soportadas, instalación reproducible, copias restaurables, gestión de secretos, registro de cambios y actualización desde upstream sin perder personalizaciones.

Estas pruebas se proponen para la fase de selección técnica; no se ejecutaron como parte de la búsqueda documental.

## Selección propuesta

1. **Revel:** probar primero por MIT, stack actual y afinidad con comunidades/artistas. El riesgo principal es madurez y capacidad de mantenimiento de un proyecto joven.
2. **pretix:** comparar como motor de ticketing con mejor evidencia documental de operación y mantenimiento, aceptando AGPL y el esfuerzo de una experiencia Caudal propia.
3. **Hi.Events:** comparar si preferimos React/Laravel y su interfaz existente, verificando release/parches y separando funciones gratuitas de Enterprise.

Mantener Eventyay como alternativa Apache si los finalistas no encajan. Estudiar los conceptos de Event Schedule y TiBillet para perfiles y redes culturales, sin importar código con otra licencia de manera indiscriminada.

## Fuentes verificables de seguridad y versiones

- Revel: [README y tarifas propias](https://github.com/letsrevel/revel-backend/blob/main/README.md), [MIT backend](https://github.com/letsrevel/revel-backend/blob/main/LICENSE), [MIT frontend](https://github.com/letsrevel/revel-frontend/blob/main/LICENSE), [SECURITY](https://github.com/letsrevel/revel-backend/blob/main/SECURITY.md), [manifiesto](https://github.com/letsrevel/revel-backend/blob/main/pyproject.toml), [tests](https://github.com/letsrevel/revel-backend/blob/main/.github/workflows/test.yaml), [dependencias](https://github.com/letsrevel/revel-backend/blob/main/.github/workflows/deps.yaml), [auditoría nocturna](https://github.com/letsrevel/revel-backend/blob/main/.github/workflows/nightly-audit.yml).
- Hi.Events: [licencia core](https://github.com/HiEventsDev/Hi.Events/blob/develop/LICENCE), [licencia Enterprise](https://github.com/HiEventsDev/Hi.Events/blob/develop/backend/ee/LICENCE), [SECURITY](https://github.com/HiEventsDev/Hi.Events/blob/develop/SECURITY.md), [tests](https://github.com/HiEventsDev/Hi.Events/blob/develop/.github/workflows/tests.yml), [E2E](https://github.com/HiEventsDev/Hi.Events/blob/develop/.github/workflows/e2e.yml), [SQLi](https://github.com/HiEventsDev/Hi.Events/security/advisories/GHSA-2qcp-24fh-fx6p), [tickets ocultos](https://github.com/HiEventsDev/Hi.Events/security/advisories/GHSA-2h54-cprv-vj74), [XSS](https://github.com/HiEventsDev/Hi.Events/security/advisories/GHSA-2ggx-79g6-2jmj).
- pretix: [licencia](https://github.com/pretix/pretix/blob/master/LICENSE), [SECURITY](https://github.com/pretix/pretix/blob/master/SECURITY.md), [tests](https://github.com/pretix/pretix/blob/master/.github/workflows/tests.yml), [SBOM](https://github.com/pretix/pretix/blob/master/.github/workflows/sbom.yml), [política de divulgación](https://github.com/pretix/pretix-docs/blob/main/docs/trust/security/disclosure.md), [gestión ISO](https://github.com/pretix/pretix-docs/blob/main/docs/trust/security/isms.md), [Enterprise](https://github.com/pretix/pretix-docs/blob/main/docs/self-hosting/installation/enterprise.md).
- Ejemplos de avisos pretix corregidos: [CVE-2026-13602](https://github.com/CVEProject/cvelistV5/blob/main/cves/2026/13xxx/CVE-2026-13602.json), [CVE-2026-101266](https://github.com/CVEProject/cvelistV5/blob/main/cves/2026/101xxx/CVE-2026-101266.json), [CVE-2026-5600](https://github.com/advisories/GHSA-wr8q-c73g-m7gp).
- Eventyay: [licencia](https://github.com/fossasia/eventyay/blob/dev/LICENSE), [NOTICE](https://github.com/fossasia/eventyay/blob/dev/NOTICE), [manifiesto](https://github.com/fossasia/eventyay/blob/dev/app/pyproject.toml), [Dependabot](https://github.com/fossasia/eventyay/blob/dev/.github/dependabot.yml), [tests antiguos](https://github.com/fossasia/eventyay/blob/dev/.github/workflows/tests.yml), [recolección de pruebas](https://github.com/fossasia/eventyay/blob/dev/.github/workflows/test-collection.yml), [política visible en GitHub](https://github.com/fossasia/eventyay/security/policy).
- alf.io: [SECURITY](https://github.com/alfio-event/alf.io/blob/main/SECURITY.md), [licencia](https://github.com/alfio-event/alf.io/blob/main/LICENSE), [sitio oficial en su repositorio](https://github.com/alfio-event/alf.io/blob/main/website/content/en/_index.html), [metadatos financieros entre organizaciones, parche 2.0-M5-2609](https://github.com/alfio-event/alf.io/security/advisories/GHSA-wrjw-r3g5-6q6x), [escaneo entre organizaciones, mismo parche](https://github.com/alfio-event/alf.io/security/advisories/GHSA-3ffp-87rx-w9xc).
- Attendize: [README](https://github.com/Attendize/Attendize/blob/develop/README.md), [manifiesto](https://github.com/Attendize/Attendize/blob/develop/composer.json), [AAL](https://github.com/Attendize/Attendize/blob/develop/LICENSE).
- Event Schedule: [README](https://github.com/eventschedule/eventschedule/blob/main/README.md), [AAL](https://github.com/eventschedule/eventschedule/blob/main/LICENSE), [lockfile](https://github.com/eventschedule/eventschedule/blob/main/composer.lock), [workflow](https://github.com/eventschedule/eventschedule/blob/main/.github/workflows/test.yml), [política de soporte Laravel](https://github.com/laravel/docs/blob/12.x/releases.md#support-policy).
- TiBillet: [README](https://github.com/TiBillet/Lespass/blob/main/README.md), [AGPL](https://github.com/TiBillet/Lespass/blob/main/LICENSE), [manifiesto](https://github.com/TiBillet/Lespass/blob/main/pyproject.toml), [lockfile](https://github.com/TiBillet/Lespass/blob/main/poetry.lock).

Revisiones observadas de las nuevas candidatas: Revel backend `82ec0ba937cf3df0fcdbb78d9f1c0dbea132c100`, frontend `fcfa7bb2e0c1a4fade901af065f1be6eeade3ba4`; Event Schedule `a71c183de15338d54861115f45f11360d49fa400`; TiBillet `63635b30c182444f2bd484670f6171d527c63e8a`. Todas mostraban actividad el 16 de octubre de 2026. Los enlaces a ramas y los precios publicados pueden cambiar.
