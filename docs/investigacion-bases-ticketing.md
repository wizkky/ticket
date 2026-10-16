# Bases de software para CaudalTickets

Investigación realizada el 16 de octubre de 2026 mediante búsqueda de repositorios en GitHub y lectura de documentación, licencias, manifiestos y actividad publicados por cada proyecto.

Ampliación: ver [costos, licencias, seguridad y nuevas alternativas](costos-licencias-seguridad.md). La segunda revisión incorpora Revel, Event Schedule y TiBillet, y actualiza la selección de finalistas.

## Objetivo

Crear una plataforma de venta y validación de entradas con sitio público, área de compradores, administración para productores y perfiles creativos. A futuro, conectar eventos con oferta, contratación e intercambio de servicios creativos.

La evaluación parte de lo descrito en esta conversación. No se han consultado las conversaciones anteriores del proyecto de ChatGPT.

## Recomendación inicial

Tras ampliar la búsqueda, evaluar **Revel como primer candidato para un prototipo propio** por su licencia MIT, backend Django y frontend Svelte. Su madurez y sus garantías de aislamiento, pagos y validación deben comprobarse mediante una prueba técnica; no se ha certificado su seguridad.

Mantener **Hi.Events como candidato funcional**: combina una interfaz React con Laravel, venta de entradas, validación QR, roles y API. La decisión depende de aceptar sus términos AGPL o contratar una licencia comercial adecuada. Su versión 2.0 tiene publicaciones de tipo release candidate; no se considera validada para producción por este informe.

Mantener **pretix como candidato cuando pese más la trayectoria operativa del motor de ticketing**. Tiene prácticas de mantenimiento y respuesta a vulnerabilidades documentadas, pero también obligaciones AGPL y de atribución. Eventyay permanece como alternativa Apache-2.0, con mayor complejidad de componentes y documentación técnica que debe contrastarse con sus manifiestos.

Estas recomendaciones son documentales: no se han instalado ni probado estas aplicaciones.

## Comparación

| Proyecto | Funciones documentadas relevantes | Tecnología revisada | Licencia y condiciones | Encaje inicial |
| --- | --- | --- | --- | --- |
| [Hi.Events](https://github.com/HiEventsDev/Hi.Events) | Venta y tipos de entradas, promociones, tickets PDF, check-in QR con registros, páginas de organizador, roles, reportes, Stripe Connect, REST API y webhooks. | Laravel 13 / PHP 8.3+, React 19, TypeScript, PostgreSQL, Redis. | Núcleo AGPL-3.0 con atribución visible obligatoria. Directorios Enterprise bajo licencia separada. | Finalista por interfaz y funciones ya integradas. |
| [pretix](https://github.com/pretix/pretix) | Venta y administración de entradas, API REST, extensiones y aplicación pretixSCAN para validar entradas. | Python, Django, PostgreSQL y Redis. | AGPL-3.0 con términos adicionales, incluida atribución. Su excepción de la sección 13 no cubre una plataforma que venda eventos de terceros como CaudalTickets. | Candidato por trayectoria y especialización en ticketing. |
| [Eventyay](https://github.com/fossasia/eventyay) | Ticketing, productos adicionales, administración de organizadores, cuentas, API, plugins, agenda, ponentes y check-in mediante componente separado. | Python 3.12, PostgreSQL, Redis, Celery y módulos Vue 3 / Vite. El README dice Django 5.2, pero el manifiesto dev exige Django >=6.0.8,<6.1. | El repositorio declara Apache-2.0; conservar los avisos LICENSE/NOTICE y revisar las licencias de los plugins seleccionados. | Candidato si se prioriza flexibilidad de licencia; la unificación agrega complejidad. |
| [alf.io](https://github.com/alfio-event/alf.io) | Reservas y gestión de asistencia a eventos. | La rama main revisada requiere Java 25, Gradle y PostgreSQL. | GPL-3.0. | Alternativa para un equipo que prefiera Java; el README recomienda partir de una versión publicada, pues main puede contener código inestable. |
| [Attendize](https://github.com/Attendize/Attendize) | Múltiples organizadores, entradas QR, escáner en navegador, pagos, reembolsos y panel de gestión. | Laravel / PHP y MySQL; el README mantiene requisitos antiguos. | Attribution Assurance License; ofrece opciones comerciales de marca blanca. | Referencia funcional, con menor prioridad como base nueva por la antigüedad de la actividad observada. |

## Condiciones que afectan la elección

### Hi.Events

- La [licencia principal](https://github.com/HiEventsDev/Hi.Events/blob/main/LICENCE) exige mantener una atribución visible a Hi.Events en páginas y correos. Hay una opción comercial para retirarla.
- La AGPL permite uso comercial, pero una versión modificada ofrecida por red debe cumplir la obligación de ofrecer su código fuente correspondiente a los usuarios que interactúan con ella.
- Los [módulos Enterprise](https://github.com/HiEventsDev/Hi.Events/blob/main/backend/ee/LICENCE), como asientos numerados y taquilla, requieren licencia para eventos reales. La autorización para retirar la atribución no incluye necesariamente esas funciones.
- No se ha comprobado que Stripe Connect cubra el país, modelo de comisiones y liquidaciones que requiera CaudalTickets. Tampoco se ha confirmado una integración nativa con una pasarela local concreta.

### pretix

- Su [licencia](https://github.com/pretix/pretix/blob/master/LICENSE) permite modificar el texto de atribución para identificar un producto derivado, conservando el reconocimiento y enlace a pretix.
- Incluye una excepción a ciertas obligaciones de interacción por red, pero la propia licencia excluye de esa excepción los servicios SaaS y la venta de eventos o productos de terceros. CaudalTickets debe evaluarse conforme a las obligaciones AGPL aplicables o a términos comerciales acordados.
- El [escáner Android](https://github.com/pretix/pretixscan-android) es un proyecto separado, con licencia Apache; eso no cambia la licencia del servidor.

### Eventyay

- Su [README](https://github.com/fossasia/eventyay/blob/dev/README.rst), [LICENSE](https://github.com/fossasia/eventyay/blob/dev/LICENSE) y [NOTICE](https://github.com/fossasia/eventyay/blob/dev/NOTICE) declaran Apache-2.0.
- NOTICE identifica código histórico procedente de Open Event, pretix, pretalx y Venueless, con fechas de corte. No debe suponerse que incluya las funcionalidades actuales de todos esos proyectos.
- El README distingue main como rama de producción y dev como desarrollo. La documentación técnica leída corresponde a dev y no demuestra por sí sola qué versión publicada contiene cada función.
- El check-in y algunos proveedores de pago se integran como componentes o plugins: deben incluirse en una prueba funcional completa.

## Actividad observada

Son fechas de commits visibles en las ramas indicadas, no garantías de calidad ni de estabilidad de una versión.

| Proyecto | Rama observada | Último commit observado, UTC | Revisión |
| --- | --- | --- | --- |
| Hi.Events | develop | 2026-10-16 | `208c41c0523f28c594838acdd1382ee3e5f0e861` |
| pretix | master | 2026-10-16 | `e4b29f56a47788a52a606bdb5c71380b20da36f8` |
| Eventyay | dev | 2026-10-16 | `d46648640e79ce9fd2e37ffcf7614b19c6730c12` |
| alf.io | main | 2026-10-12 | `841c7a1fa40a5e287ff7429155debfe6b3e81da8` |
| Attendize | develop | 2023-01-26 | `9289acbab1583898fd85aeee66c7b613d8971deb` |

Las publicaciones más recientes que mostraban los feeds consultados fueron [Hi.Events v2.0.0-rc.2](https://github.com/HiEventsDev/Hi.Events/releases/tag/v2.0.0-rc.2), [pretix v2026.8.0](https://github.com/pretix/pretix/releases/tag/v2026.8.0) y [alf.io 2.0-M5-2609](https://github.com/alfio-event/alf.io/releases/tag/2.0-M5-2609). El feed de releases de Eventyay no mostró entradas en esta consulta.

## Qué tendría que aportar CaudalTickets

La documentación revisada no demuestra que alguno incluya el mercado de servicios creativos descrito. Debemos diseñar y desarrollar esa parte:

- Perfiles creativos con portafolio, especialidades y disponibilidad.
- Publicación, búsqueda, contratación e intercambio de servicios vinculados a eventos.
- Identidad y permisos consistentes para compradores, creativos, productores y administración.
- Comisiones, liquidaciones a productores y pagos a prestadores de servicios conforme al modelo comercial elegido.
- Experiencia de comprador con historial y acceso a sus entradas; un listado de asistentes del productor no equivale a ese espacio personal.

Una arquitectura a estudiar es usar uno de estos proyectos como motor de entradas y construir la experiencia y servicios de Caudal alrededor de sus API. La separación técnica por API no determina por sí sola las obligaciones de licencia de las piezas que se creen.

## Próxima evaluación técnica propuesta

En los candidatos finalistas, probar un recorrido completo: crear dos productores, publicar un evento, comprar una entrada de prueba, recibirla y validar el QR; intentar una segunda validación; comprobar que un productor no puede acceder a los datos del otro. Revisar también reembolsos, fallos de pago y conciliación antes de decidir una base para ventas reales.

Definir la pasarela y el país de operación, el modelo de comisiones y la preferencia sobre publicación del código o licencia comercial permitirá cerrar la selección. Estas decisiones no impiden continuar la evaluación documental.

## Fuentes consultadas

- [Búsqueda GitHub: event ticketing](https://github.com/search?q=event+ticketing&type=repositories).
- Hi.Events: [README](https://github.com/HiEventsDev/Hi.Events/blob/main/README.md), [backend](https://github.com/HiEventsDev/Hi.Events/blob/main/backend/composer.json), [frontend](https://github.com/HiEventsDev/Hi.Events/blob/main/frontend/package.json), [licencia](https://github.com/HiEventsDev/Hi.Events/blob/main/LICENCE), [Enterprise](https://github.com/HiEventsDev/Hi.Events/blob/main/backend/ee/LICENCE), [commits](https://github.com/HiEventsDev/Hi.Events/commits/develop), [releases](https://github.com/HiEventsDev/Hi.Events/releases).
- pretix: [README](https://github.com/pretix/pretix/blob/master/README.rst), [manifiesto](https://github.com/pretix/pretix/blob/master/pyproject.toml), [API](https://github.com/pretix/pretix/blob/master/doc/api/index.rst), [licencia](https://github.com/pretix/pretix/blob/master/LICENSE), [escáner Android](https://github.com/pretix/pretixscan-android), [commits](https://github.com/pretix/pretix/commits/master).
- Eventyay: [README](https://github.com/fossasia/eventyay/blob/dev/README.rst), [licencia](https://github.com/fossasia/eventyay/blob/dev/LICENSE), [NOTICE](https://github.com/fossasia/eventyay/blob/dev/NOTICE), [commits](https://github.com/fossasia/eventyay/commits/dev).
- alf.io: [README](https://github.com/alfio-event/alf.io/blob/main/README.md), [licencia](https://github.com/alfio-event/alf.io/blob/main/LICENSE), [commits](https://github.com/alfio-event/alf.io/commits/main).
- Attendize: [README](https://github.com/Attendize/Attendize/blob/master/README.md), [commits](https://github.com/Attendize/Attendize/commits/develop).

Los enlaces a ramas pueden cambiar. Las revisiones de la tabla permiten identificar los estados de las ramas de desarrollo observados durante la investigación; no todos los documentos se leyeron en esas mismas ramas.
