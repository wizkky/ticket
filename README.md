# CaudalTickets · Plataforma en desarrollo

Base de desarrollo de una ticketera y comunidad para productores, compradores y creativos. Esta primera versión integra snapshots MIT de Revel v2.22.1, con identidad Caudal, recorridos de comprador, productor y administración, y datos de demostración propios.

## Administración en español

La revisión `feature/clp-admin-es-without-food`, basada en la versión CLP, traduce
la administración y retira la gestión de alimentos, restricciones y preferencias
alimentarias de la API, del administrador y de las pantallas de perfil/evento.
[Alcance, captura y actualización local](docs/administracion-es-sin-alimentacion.md).

## Inicio

Requisitos: Linux, Docker con Compose v2, Node.js 24 con Corepack, Python 3 y `uv`. El backend usa Python 3.14, instalado por `uv` según su versión fijada. También necesita las bibliotecas nativas de GDAL/GEOS, Pango y libmagic. La comprobación del QR usa `pdftoppm` (Poppler) y libzbar.

En Debian/Ubuntu, instalar las bibliotecas nativas con el administrador del sistema:

```bash
apt-get install -y gdal-bin libgdal-dev libpango-1.0-0 libpangoft2-1.0-0 libmagic1 poppler-utils zbar-tools
```

Desde la raíz del checkout existente:

```bash
bash scripts/setup.sh
bash scripts/dev.sh
```

El setup genera configuración privada una sola vez, instala con lockfiles congelados, levanta PostGIS/Redis/Mailpit, aplica migraciones, compila traducciones, prepara datos demo y construye el frontend. Preserva archivos `.env` existentes, contraseñas y datos de la base. No usar `make setup` de los snapshots: su flujo original reinicia volúmenes y sobrescribe configuración.

El arranque comprueba respuestas HTTP de ambos componentes y mantiene sus procesos supervisados. Para detener frontend y backend desde otra terminal:

```bash
bash scripts/stop.sh
```

Los contenedores conservan datos. Para detener también la infraestructura sin borrar volúmenes:

```bash
docker compose --env-file .local/stack.env stop
```

| Componente | Puerto local |
| --- | --- |
| Sitio web | 5173 |
| API y administración Django | 8000 |
| Bandeja de correo de prueba Mailpit | 8025 |
| PostgreSQL/PostGIS | 5432 |
| Redis | 6379 |

Todos los puertos de esta configuración se enlazan a loopback. No es una configuración de despliegue público.

## Datos para recorrer la demo

El setup crea dos productores con organizaciones y eventos separados, un comprador y un administrador. Las contraseñas aleatorias se guardan únicamente en `.local/demo-credentials.json` con permisos privados; los identificadores y rutas de eventos quedan en `.local/demo.json`. Estos archivos no se suben a GitHub.

Hay una entrada gratuita y una reserva con pago en puerta por evento: $5.000 CLP en el evento A y $5.500 CLP en el B. El comprador puede reservar y recibir un ticket PDF; el productor puede escanear su QR. El correo se entrega a Mailpit local, sin enviarlo a destinatarios reales. Los eventos de demostración están en Valdivia, Los Ríos, con zona `America/Santiago`. Las nuevas tarifas usan pesos chilenos (CLP), sin decimales y con punto de miles. Los registros históricos en EUR conservan su moneda; no se realiza conversión cambiaria.

El modo demo propio se habilita con `CAUDAL_DEMO=True`. El bypass de autenticación original de Revel permanece desactivado (`DEMO_MODE=False`): las cuentas acceden con contraseña real.

## Validación

Con la aplicación levantada:

```bash
bash scripts/smoke.sh
```

La prueba usa HTTP real para autenticarse, comprobar permisos, actualizar una tarifa válida, reservar entradas y consultar tickets. Descarga el PDF, rasteriza su QR y lo decodifica con libzbar para usar el código leído en el check-in. Comprueba el rechazo del segundo escaneo y que el productor de otra organización no pueda gestionar esa entrada.

Cada ejecución crea nuevas entradas de prueba; no borra órdenes anteriores. Los artefactos y resultados quedan en `.local/`, fuera de Git. El resultado de la ejecución actual y los límites conocidos se registran en [validación de la primera prueba](docs/validacion-prueba.md).

## Alcance actual

- Venta/reserva de demostración gratuita o con pago en puerta.
- Sistema visual Caudal compartido, catálogo de Los Ríos, espacio productor y administración general con acceso protegido. Consulta [los recorridos y límites de esta etapa](docs/experiencia-caudal-v3.md).
- Sin cuenta Stripe conectada: no se ha validado un cobro online ni liquidaciones a productores. No se debe presentar una reserva offline como un pago procesado.
- Apple/Google Wallet, Telegram, evaluación con IA y escaneo antivirus no forman parte de esta prueba. Las integraciones que requieren credenciales están desactivadas o sin configurar.
- Los perfiles y el mercado de servicios creativos todavía requieren diseño y desarrollo.

Para un servicio real faltan configuración de producción, dominio/HTTPS, correos propios, pasarela compatible con el país y modelo comercial, políticas legales, operación de copias/actualizaciones y pruebas de carga y seguridad del recorrido completo.

## Estructura y licencias

```text
apps/api/       Revel backend Django y su licencia MIT original
apps/web/       Revel frontend Svelte y su licencia MIT original
scripts/        Preparación, arranque, datos demo y comprobación funcional
compose.yaml    Infraestructura local persistente
docs/           Investigación, arquitectura y resultados
.local/         Configuración y artefactos privados, ignorados por Git
```

Las nuevas contribuciones de esta base se publican bajo MIT. Conservar [LICENSE](LICENSE), las licencias de cada snapshot y [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). [UPSTREAM.md](UPSTREAM.md) registra los repositorios, versiones y revisiones exactas; no se declara autoría propia sobre el código original.

Cada tarea cloud ya tiene un entorno aislado: trabajar sobre este checkout, sin crear un worktree adicional salvo petición explícita. La configuración reusable del entorno y los scripts deben reactivar servicios; no asumir que los procesos sobreviven al cierre de una tarea.

## Identidad visual

La segunda etapa adapta CaudalTickets al lenguaje de Caudal Creativo y sus
marcas hermanas. Consulta [la dirección visual y procedencia de activos](docs/identidad-visual-caudal.md).

[Portada de escritorio](docs/screenshots/caudal-v2-desktop.png) · [Vista móvil](docs/screenshots/caudal-v2-mobile.png)

## Recorridos y revisión de producto

La tercera etapa une catálogo territorial, cuenta y entradas, gestión del productor y
administración general. [Recorridos](docs/experiencia-caudal-v3.md) ·
[Validación y capturas de escritorio/móvil](docs/validacion-experiencia-v3.md).
