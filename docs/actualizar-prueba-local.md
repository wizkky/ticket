# Descargar o actualizar la prueba local

La revisión de Caudal Creativo está en la rama
`feature/caudal-creativo-platform`. Incluye el rediseño de `d2fabf1`, la moneda CLP
y los recorridos anteriores. Usar esa rama para actualizar esta prueba; todavía
no está fusionada en `main`. No hace falta un PR fusionado para descargarla.

Estos comandos corresponden al entorno Linux de desarrollo descrito en el
[README](../README.md): Docker con Compose v2, Node 24 con Corepack, `uv` y las
bibliotecas nativas de la API. No constituyen un despliegue de producción.

## Si ya tienes el repositorio

Reemplazar `/ruta/a/ticket` por la carpeta actual del proyecto. Revisar el estado
antes de cambiar de rama; guardar los cambios propios si aparecen archivos
modificados. No utilizar `reset --hard` ni borrar la configuración para actualizar.

```bash
cd /ruta/a/ticket
git status --short
bash scripts/stop.sh
git fetch origin
git switch feature/caudal-creativo-platform
git pull --ff-only origin feature/caudal-creativo-platform
```

`git switch` utiliza la rama local si existe; si no existe, la obtiene de la rama
remota recién descargada. `--ff-only` evita crear una mezcla automática cuando la
rama local tiene commits propios que divergen de GitHub.

La configuración existente se conserva. En `apps/api/.env`, establecer estas
variables si todavía tienen otro valor, manteniendo todas las demás:

```dotenv
SITE_NAME=Caudal Creativo
DEFAULT_TICKET_CURRENCY=CLP
```

No es necesario cambiar `DEFAULT_CURRENCY`: la moneda base de conversión de la
plataforma es independiente de la moneda por defecto de las entradas.

Para guardar una copia de la base antes de aplicar migraciones, con sus
contenedores existentes:

```bash
source scripts/common.sh
stack up -d --wait postgres
mkdir -p .local/backups
umask 077
backup_file=".local/backups/caudal-$(date +%Y%m%d-%H%M%S).dump"
stack exec -T postgres sh -c 'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$backup_file"
test -s "$backup_file"
```

Actualizar dependencias, migraciones, datos demo y build; después arrancar:

```bash
bash scripts/setup.sh
bash scripts/dev.sh
```

El setup preserva `.env`, credenciales y volúmenes existentes. El seed actualiza
las demostraciones identificadas: retira de la venta pública sus antiguas tarifas
EUR y utiliza las tarifas CLP, conservando los tickets anteriores. No convierte
el historial de euros a pesos. Los archivos subidos de una instalación existente
siguen en `apps/api/src/media/` y también deben conservarse.

El proceso de arranque queda abierto en esa terminal. Si utilizas un supervisor
propio para la web/API, detener y reiniciar esos procesos con tu supervisor al
reconstruir el frontend. `scripts/stop.sh` solo detiene los procesos iniciados por
los scripts de este repositorio.

## Primera descarga en otra carpeta

Ejecutar desde la carpeta donde quieras crear el checkout, usando un nombre de
destino que todavía no exista:

```bash
git clone --branch feature/caudal-creativo-platform --single-branch https://github.com/wizkky/ticket.git ticket
cd ticket
bash scripts/setup.sh
bash scripts/dev.sh
```

Esta opción crea una instalación nueva y sus propias cuentas demo; no copia la
base ni los archivos subidos de otra instalación. Si ya existe otra prueba en
este servidor usando los mismos puertos, detenerla antes de arrancar otra.

## Confirmar la revisión descargada

```bash
git branch --show-current
git log -2 --oneline
git rev-parse HEAD
git rev-parse origin/feature/caudal-creativo-platform
```

Después del `fetch` y el `pull`, ambos hashes deben coincidir. Esa comparación
verifica la revisión de código; la reconstrucción y el reinicio anteriores hacen
que el proceso local sirva esa revisión.

Los puertos de esta prueba están enlazados a loopback: web 5173, API/Django 8000
y Mailpit 8025. Para verla desde otro equipo, conservar o configurar el proxy o
túnel de tu servidor local; estos scripts no publican el sitio en la red.

Las credenciales demo se guardan en `.local/demo-credentials.json`. Mantenerlas
privadas. Para ejecutar la comprobación funcional existente, en otra terminal y
con la aplicación levantada:

```bash
bash scripts/smoke.sh
```

La comprobación agrega tickets de prueba y realiza check-in en la base local.
No borra los anteriores ni procesa cobros online. Los resultados y límites de la
revisión están en [validación de Caudal Creativo](validacion-caudal-creativo.md).
