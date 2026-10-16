# Validación de la primera prueba funcional

Ejecutada el 16 de octubre de 2026 en el entorno cloud actual, contra la base de Revel descrita en [UPSTREAM.md](../UPSTREAM.md). No se ha certificado un despliegue de producción ni la restauración en otra máquina.

## Resultado del recorrido

`bash scripts/smoke.sh` terminó con código **0**, con **11 comprobaciones aprobadas**. Utiliza la API HTTP que está corriendo, no respuestas simuladas.

1. Contraseña incorrecta rechazada e ingreso real de comprador y dos productores.
2. Eventos y tarifas consultables sin iniciar sesión.
3. Cada productor administra sus datos; no puede leer ni gestionar los del otro.
4. Tarifa válida en EUR editable por su dueño, con escritura rechazada para el otro productor.
5. Checkout gratuito que crea una entrada activa para el comprador.
6. PDF descargado por el dueño; QR leído desde una imagen rasterizada del PDF mediante Poppler y libzbar.
7. Primer escaneo admitido y segundo escaneo secuencial rechazado. Comprador y productor ajeno no pueden validar esa entrada.
8. Dos solicitudes HTTP simultáneas sobre otra entrada: exactamente una admisión y un rechazo.
9. Reserva de 10 EUR con pago en puerta; no se crea ni se simula un cobro bancario online.
10. Entradas presentes en la cuenta del comprador.
11. Correo de esa compra capturado en Mailpit, correlacionado con comprador, evento y UUID; adjunta `ticket.pdf` válido y `event.ics`.

La prueba se puede repetir y crea tres entradas adicionales por ejecución. No borra pedidos ni resetea la base. La configuración `live_emails=False` conserva el catchall de desarrollo de Revel; se verificó el destinatario original codificado y la captura local, sin entrega a buzones externos.

La evidencia privada está en `.local/smoke/resultado.json`, `email-result.json`, `entrada-gratuita.pdf`, `entrada-gratuita.png` y `entrada-email.pdf`. No se publica en GitHub. Las capturas visuales en `docs/screenshots/` contienen únicamente datos de demostración.

## Corrección de escaneo simultáneo

Se reprodujo una carrera del snapshot original con dos conexiones PostgreSQL reales: ambas validaciones devolvían éxito (`[200, 200]`). La prueba de regresión falló antes de modificar el servicio.

El parche añade una transacción y bloqueo de la fila de Ticket (`select_for_update(of=("self",))`) al servicio de check-in. El bloqueo no se aplica a los joins opcionales. Después del parche, la regresión pasó con `[200, 400]`; el smoke HTTP confirmó también una sola admisión. No hubo cambios de modelos o migraciones.

Se aprobaron **61 pruebas distintas** de las familias relacionadas: 59 existentes, el presupuesto de consultas ajustado y la nueva regresión de concurrencia. El límite de consultas se ajustó a 25 para incluir SAVEPOINT/RELEASE: la versión con prefetch usa 24 y retirarlo llega a 26, por lo que la aserción sigue detectando esa regresión de rendimiento.

## Instalación y frontend

| Verificación | Resultado |
| --- | --- |
| Backend `uv sync --frozen --group dev` | Instalado con lockfile; Python 3.14.8 y Django 5.2.18. |
| Migraciones | 335 aplicadas; comprobación de esquema y setup posterior sin migraciones pendientes. |
| PostgreSQL/PostGIS | PostgreSQL 16.15; imágenes de infraestructura fijadas por digest. Se conservó y restauró un dump al actualizar la imagen inicial. |
| Backend `make audit` | Código 0; no encontró vulnerabilidades conocidas en las dependencias revisadas. No es una auditoría del código completo. |
| Root `bash scripts/setup.sh` | Código 0; instalación repetida, traducciones, configuración, datos demo y build frontend. |
| Repetición de configuración | Conservó los bytes de ambos `.env`, credenciales y configuración de base; permanecen dos organizaciones demo. |
| Frontend instalación congelada y build final | Código 0 con pnpm 11.6.0; DOMPurify 3.4.16. |
| Tipos frontend | Sin errores; 394 advertencias heredadas documentadas por el runner. |
| Frontend pruebas seleccionadas | 21 pruebas de configuración/SEO y 7 pruebas de Markdown/sanitización/compatibilidad aprobadas en sus ejecuciones correspondientes. |
| Formato, lint y guards frontend | Aprobados para la integración revisada. |
| Chromium real | Portada, login del comprador, cookies Secure/HttpOnly, panel de entradas, listado y ficha de evento; sin errores JavaScript de página. |

La configuración SMTP inicial intentaba autenticarse en Mailpit. Se corrigieron usuario y contraseña SMTP a valores vacíos y se reinició la API para cargar el cambio. Se recuperaron las entregas pendientes con el mecanismo upstream; el smoke final verificó además la entrega de una compra nueva sin esa recuperación manual.

## Límites conocidos

- **Cobro online:** pendiente de cuenta y credenciales sandbox, país de operación y modelo de liquidación. No hay ventas reales validadas.
- **CLP:** no admitido por los esquemas de tarifas actuales de Revel; el recorrido usa EUR admitido por la API. La zona horaria de los eventos demo es America/Santiago.
- **Dependencias de compilación web:** quedan un aviso alto en `braces@3.0.3` y uno moderado en `postcss-selector-parser@6.1.4`, detallados en [frontend.md](frontend.md). El alto está excluido upstream y el parche anunciado no está publicado en el registro consultado. No interpretar una salida exitosa de audit con exclusiones como ausencia de avisos.
- **Identidad y textos:** es una adaptación inicial; quedan recursos y páginas secundarias de Revel. Revisar marca, condiciones y privacidad antes de una publicación comercial.
- **Operación:** esta configuración enlaza a loopback, usa DEBUG y correo local. Faltan despliegue de producción, TLS, operación de backups, carga, revisión integral de permisos/pagos y actualizaciones.
- **Ecosistema creativo:** perfiles, portafolios, contratación e intercambio de servicios no están implementados por esta importación.

Las verificaciones anteriores describen el resultado real de esta primera prueba; no constituyen una afirmación de ausencia de vulnerabilidades.
