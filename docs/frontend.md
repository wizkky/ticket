# Frontend de la primera prueba

La aplicación está en `apps/web`, importada de Revel frontend bajo MIT. El `LICENSE` original permanece en esa carpeta. La portada, el nombre compartido y el pie se adaptaron a CaudalTickets; los flujos de compra, cuentas y administración siguen siendo los de Revel. Las traducciones nuevas se incluyen en los seis idiomas existentes.

## Desarrollo

Requiere Node >=22.22.2, pnpm11.6.0 y la API iniciada en `http://localhost:8000`.

```bash
cd apps/web
corepack pnpm install --frozen-lockfile
corepack pnpm paraglide:compile
corepack pnpm dev --host 0.0.0.0 --port 5173 --strictPort
```

La API pública se configura mediante `PUBLIC_API_URL` en `.env`, con fallback `http://localhost:8000`. Para llamadas SSR se puede añadir `INTERNAL_API_URL` apuntando a una dirección interna del mismo backend. El navegador debe poder alcanzar `PUBLIC_API_URL`; cambiar la URL pública también requiere autorizar su origen en la configuración CORS del backend. No cambiar sólo el puerto del frontend y asumir que la API ya es accesible externamente.

`PUBLIC_HIDE_SOLUTIONS_FOOTER=true` se conserva en el ejemplo para las superficies upstream que utilizan esa opción. El pie principal de Caudal ya no muestra los planes, contactos ni textos legales comerciales de Revel. Las páginas secundarias aún contienen textos y metadatos upstream: esta adaptación inicial no es la identidad final ni las políticas de una plataforma publicada.

## Comprobaciones

```bash
corepack pnpm check
corepack pnpm build
corepack pnpm exec vitest run src/lib/seo/types.test.ts src/lib/config/api.test.ts src/lib/seo/build.test.ts
corepack pnpm audit --prod --audit-level=high
```

El bundle de traducciones es generado e ignorado por Git. Debe compilarse antes de desarrollo, tipos o pruebas; `pnpm build` genera su variante propia. Si el entorno usa un proxy de red, Node24 requiere `NODE_USE_ENV_PROXY=1` para descargar los módulos Inlang desde jsDelivr. Sin ello el compilador puede avisar de un fallo de descarga y aun así devolver éxito con mensajes ausentes. Conservar la validación TLS y la autoridad de certificados suministrada por el entorno.

En este cloud las cachés deben ir bajo `/workspace` o `/tmp`. Para Corepack puede usarse `COREPACK_HOME=/workspace/.cache/corepack`; para instalar, `pnpm install --frozen-lockfile --store-dir /workspace/.cache/pnpm-store`. Otros comandos, como `licenses`, aceptan `--config.store-dir=/workspace/.cache/pnpm-store`. Una alternativa para herramientas auxiliares es `XDG_DATA_HOME` en un directorio escribible.

Esta prueba utiliza reservas gratuitas o pago en puerta. No hay un pago en línea procesado o simulado por la portada.

## Auditoría de dependencias de la instantánea inicial

El 16 de octubre de 2026, `pnpm audit --prod` informó cuatro avisos. Se repitió sobre una copia temporal del manifiesto y lockfile sin las exclusiones upstream para obtener sus identificadores; no se modificaron las dependencias de la aplicación.

| Paquete instalado | Aviso | Gravedad | Alcance observado | Parche anunciado |
| --- | --- | --- | --- | --- |
| `dompurify@3.4.13` | [GHSA-p98j-92pf-mc4p](https://github.com/advisories/GHSA-p98j-92pf-mc4p) | Baja | Runtime, mediante `isomorphic-dompurify`. Afecta limpieza `IN_PLACE` con hooks que eliminan nodos. | `>=3.4.16` |
| `dompurify@3.4.13` | [GHSA-6688-9rhm-gjv2](https://github.com/advisories/GHSA-6688-9rhm-gjv2) | Baja | Runtime. Afecta retorno de nodos con `IN_PLACE` y reinterpretación posterior como HTML. | `>=3.4.16` |
| `braces@3.0.3` | [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) | Alta | Dependencia opcional de compilación: `tailwind-variants → tailwindcss → chokidar/micromatch`. Agotamiento de pila con patrones profundamente anidados. | `>=3.0.4` |
| `postcss-selector-parser@6.1.4` | [GHSA-rj75-hqrm-r3gf](https://github.com/advisories/GHSA-rj75-hqrm-r3gf) | Moderada | Dependencia opcional de compilación del mismo Tailwind, directa y mediante `postcss-nested`. Consumo cuadrático de CPU con selectores preparados. | `>=7.1.6` |

`src/lib/utils/sanitize.ts` pasa cadenas a DOMPurify con una lista restrictiva de etiquetas y atributos. No usa `IN_PLACE` ni instala hooks. No encontramos en el código el patrón necesario para los dos avisos bajos; esto no equivale a una auditoría completa de seguridad.

El aviso alto está excluido en `pnpm-workspace.yaml` por una decisión heredada: se justificaba por su uso en compilación con patrones propios y por la inexistencia de parche. La API de auditoría anuncia `3.0.4` como parche, pero el registro oficial de npm no publica esa versión: la consulta de `https://registry.npmjs.org/braces` devuelve `latest=3.0.3` y no contiene `versions["3.0.4"]` ni su fecha. Se conserva la exclusión de compilación y se documenta esta discrepancia; no se instala una versión inexistente. No se debe interpretar la salida exitosa de `pnpm audit --audit-level=high` con esa exclusión como ausencia de avisos. El salto de `postcss-selector-parser` 6 a 7 requiere validar compatibilidad con Tailwind antes de forzar un override.

Se aplicó un parche focalizado de DOMPurify a `3.4.16`, publicado oficialmente el 23 de septiembre de 2026, manteniendo la cuarentena de 24 horas y la comprobación de integridad del lockfile. Se añadió un override dirigido y se comprobó que el lockfile no cambia ninguna otra versión. Tras la instalación congelada, los dos avisos bajos desaparecen; permanecen el moderado de `postcss-selector-parser` y el alto de `braces` excluido por el alcance de compilación y la ausencia del parche en npm.

Se añadieron tres pruebas en `sanitize.security.test.ts` que comprueban la eliminación de scripts, handlers, URLs ejecutables codificadas y documentos incrustados, conservando el formato y los enlaces HTTPS válidos. Estas pruebas y las existentes de renderizado Markdown y compatibilidad HTTP pasan: siete pruebas en tres archivos.

Para servir el build de producción local sin el costo de compilación inicial de Vite:

```bash
cd apps/web
HOST=127.0.0.1 PORT=5173 ORIGIN=http://localhost:5173 node --env-file=.env build
```

La portada en español responde HTTP 200 y explica que el cobro en línea sigue pendiente. Las cookies de autenticación conservan el atributo `Secure` de producción: usar `http://localhost:5173` para la prueba local o HTTPS para una publicación. Se verificó en Chromium real el inicio de sesión del comprador contra el backend, la redirección a `/dashboard`, la persistencia de ambas cookies `Secure` + `HttpOnly` y la navegación autenticada a `/dashboard/tickets`. El listado y una ficha de evento también responden HTTP 200, sin errores JavaScript de página. Las capturas de datos demo están en `docs/screenshots/`.

## Desarrollo con la portada Caudal

La identidad compartida y sus referencias están en
[identidad-visual-caudal.md](identidad-visual-caudal.md). La portada usa datos
reales de la API pública y conserva los estados sin eventos y de error de carga.

En el entorno en la nube, `bash scripts/dev.sh` sirve la compilación de
producción. Antes de recompilar, ejecuta `bash scripts/stop.sh`; después compila
en `apps/web` y vuelve a iniciar desde la raíz. Esto evita que el proceso
anterior lea archivos que Vite reemplaza durante la compilación. Para edición
continua también está disponible el servidor Vite documentado más arriba.
